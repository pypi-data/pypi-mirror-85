# dbnomics-fetcher-ops -- Manage DBnomics fetchers
# By: Christophe Benz <christophe.benz@cepremap.org>
#
# Copyright (C) 2020 Cepremap
# https://git.nomics.world/dbnomics/dbnomics-fetcher-ops
#
# dbnomics-fetcher-ops is free software; you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# dbnomics-fetcher-ops is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import re
import urllib.parse
from dataclasses import dataclass
from typing import Optional

import daiquiri
import gitlab
import typer
from gitlab.v4.objects import VISIBILITY_PUBLIC, DeployKey, Project, ProjectPipelineSchedule, ProjectTrigger

from .. import constants, loaders, ssh

logger = daiquiri.getLogger(__name__)

fetchers_group_name = "dbnomics-fetchers"
source_data_group_name = "dbnomics-source-data"
json_data_group_name = "dbnomics-json-data"
fetcher_pipeline_project_name = "dbnomics/dbnomics-fetcher-pipeline"
data_model_project_name = "dbnomics/dbnomics-data-model"
solr_project_name = "dbnomics/dbnomics-solr"
CI_JOBS_KEY = "CI jobs"
JOB = "JOB"
RUN_FETCHER = "Run fetcher"
SSH_PRIVATE_KEY = "SSH_PRIVATE_KEY"


def configure_command(
    provider_slug: str,
    gitlab_url: str = typer.Option(
        constants.GITLAB_URL, envvar="GITLAB_URL", help="Base URL of GitLab instance", show_default=True,
    ),
    gitlab_private_token: str = typer.Option(
        ...,
        envvar="GITLAB_PRIVATE_TOKEN",
        help="Private access token used to authenticate to GitLab API",
        show_default=True,
    ),
    debug_gitlab: bool = typer.Option(False, help="Show logging debug messages of Python GitLab"),
    dry_run: bool = typer.Option(False, "-n", "--dry-run", help="Do not perform deletions"),
    schedule_cron: Optional[str] = typer.Option(None, help="Cron expression of the pipeline schedule of fetcher",),
    schedule_cron_timezone: Optional[str] = typer.Option(
        None, help="Cron timezone of the pipeline schedule of fetcher", show_default=True,
    ),
):
    """Configure a fetcher."""
    # Defer import to let the cli.callback function write the variable and avoid importing None.
    from ..app_args import app_args

    assert app_args is not None

    if dry_run:
        logger.info("Dry run mode enabled: modifications will not be performed")

    if provider_slug != provider_slug.lower():
        logger.error("Invalid PROVIDER_SLUG %r: must be lowercase", provider_slug)
        raise typer.Exit(1)

    fetcher_metadata = app_args.fetchers_metadata.get(provider_slug)

    if fetcher_metadata is None:
        logger.error("Provider %r was not found in fetchers.yml, exit", provider_slug)
        raise typer.Exit(1)

    if fetcher_metadata.get("legacy_pipeline"):
        logger.error(
            "Provider %r still declares `legacy_pipeline: true` in fetchers.yml, exit", provider_slug,
        )
        raise typer.Exit(1)

    if gitlab_url.endswith("/"):
        gitlab_url = gitlab_url[:-1]

    # Create GitLab client.
    gl = gitlab.Gitlab(gitlab_url, private_token=gitlab_private_token, api_version=4)
    gl.auth()
    if debug_gitlab:
        gl.enable_debug()

    # Get data model and solr projects.
    data_model_project = gl.projects.get(data_model_project_name)
    solr_project = gl.projects.get(solr_project_name)

    # Get data model project trigger.
    data_model_triggers = data_model_project.triggers.list()
    assert len(data_model_triggers) == 1, data_model_triggers
    data_model_trigger = data_model_triggers[0]

    # Get solr project trigger.
    solr_triggers = solr_project.triggers.list()
    assert len(solr_triggers) == 1, solr_triggers
    solr_trigger = solr_triggers[0]

    ctx = Context(
        dry_run=dry_run,
        gitlab_url=gitlab_url,
        gl=gl,
        provider_slug=provider_slug,
        schedule_cron=schedule_cron,
        schedule_cron_timezone=schedule_cron_timezone,
        solr_project=solr_project,
        data_model_project=data_model_project,
        solr_trigger=solr_trigger,
        data_model_trigger=data_model_trigger,
    )

    fetcher_project = gl.projects.get(f"{fetchers_group_name}/{provider_slug}-fetcher")

    source_data_project_name = f"{provider_slug}-source-data"
    try:
        source_data_project = gl.projects.get(f"{source_data_group_name}/{source_data_project_name}")
    except gitlab.exceptions.GitlabGetError:
        logger.info("Source data project does not exist, creating...")
        source_data_description = f"Source data as downloaded from provider {provider_slug}"
        source_data_project = create_project(
            source_data_group_name, source_data_project_name, source_data_description, ctx
        )

    json_data_project_name = f"{provider_slug}-json-data"
    try:
        json_data_project = gl.projects.get(f"{json_data_group_name}/{json_data_project_name}")
    except gitlab.exceptions.GitlabGetError:
        logger.info("JSON data project does not exist, creating...")
        json_data_description = "Data following DBnomics data model, converted from provider data"
        json_data_project = create_project(json_data_group_name, json_data_project_name, json_data_description, ctx)

    # Remove legacy stuff.
    delete_triggers(fetcher_project, ctx)
    delete_webhooks(source_data_project, ctx)

    # Switch to new CI conf.
    ensure_new_ci_conf(fetcher_project, ctx)
    ensure_pipeline_schedule(fetcher_project, ctx)
    ensure_ssh_key_pair(fetcher_project, source_data_project, json_data_project, ctx)
    ensure_json_data_webhooks(json_data_project, ctx)


@dataclass
class Context:
    gitlab_url: str
    dry_run: bool
    gl: gitlab.Gitlab
    provider_slug: str
    schedule_cron: Optional[str]
    schedule_cron_timezone: Optional[str]
    solr_project: Project
    data_model_project: Project
    solr_trigger: ProjectTrigger
    data_model_trigger: ProjectTrigger

    @property
    def gitlab_api_base_url(self):
        return f"{self.gitlab_url}/api/v4"


def get_deploy_key_title(ctx: Context):
    return f"{ctx.provider_slug} {CI_JOBS_KEY}"


def find_variable_by_name(project: Project, name: str) -> Optional[str]:
    try:
        return project.variables.get(SSH_PRIVATE_KEY)
    except gitlab.exceptions.GitlabGetError:
        return None


def find_deploy_key_by_title(project: Project, title: str) -> Optional[DeployKey]:
    for key in project.keys.list(as_list=False):
        if key.title == title:
            return key
    return None


def delete_env_variable(project: Project, name: str, ctx: Context):
    logger.info("Deleting environment variable %r of %r...", name, project)
    try:
        variable = project.variables.get(name)
    except gitlab.exceptions.GitlabGetError:
        logger.info("%r was not found in %r", name, project)
        return
    if not ctx.dry_run:
        variable.delete()
        logger.info("%r deleted from %r", variable, project)


def delete_deploy_keys(project: Project, ctx: Context):
    logger.info("Deleting deploy keys of %r...", project)
    for key in project.keys.list(as_list=False):
        if key.title != get_deploy_key_title(ctx):
            logger.warning("%r ignored, title: %r", key, key.title)
            continue
        if not ctx.dry_run:
            key.delete()
            logger.info("%r deleted from %r", key, project)
    else:
        logger.info("No deploy key found for %r", project)


def ensure_ssh_key_pair(
    fetcher_project: Project, source_data_project: Project, json_data_project: Project, ctx: Context,
):
    """Checks that the SSH key pair is configured, otherwise configure a new one.

    In particular ensure that the fetcher project has a SSH_PRIVATE_KEY masked variable,
    and that source-data and json-data projects have a deploy key.
    """
    ssh_private_key_variable = find_variable_by_name(fetcher_project, SSH_PRIVATE_KEY)
    deploy_key_title = get_deploy_key_title(ctx)
    source_data_deploy_key = find_deploy_key_by_title(source_data_project, deploy_key_title)
    json_data_deploy_key = find_deploy_key_by_title(json_data_project, deploy_key_title)
    if not ssh_private_key_variable or not source_data_deploy_key or not json_data_deploy_key:
        # Do some cleanup.
        delete_env_variable(fetcher_project, SSH_PRIVATE_KEY, ctx)
        delete_deploy_keys(source_data_project, ctx)
        delete_deploy_keys(json_data_project, ctx)

        # Generate a new SSH key pair, set private key to a fetcher project variable,
        # and create a deploy key from SSH public key used by both source-data
        # and json-data projects.
        ssh_public_key, ssh_private_key = ssh.generate_ssh_key_pair(ctx.provider_slug)
        if not ctx.dry_run:
            fetcher_project.variables.create({"key": SSH_PRIVATE_KEY, "value": ssh_private_key})
            # Do not display private key value.
            logger.info("%r added to %r", SSH_PRIVATE_KEY, fetcher_project)
            deploy_key = source_data_project.keys.create(
                {"title": deploy_key_title, "key": ssh_public_key, "can_push": True}
            )
            logger.info("%r enabled for %r", deploy_key, source_data_project)
            json_data_project.keys.enable(deploy_key.id)
            json_data_project.keys.update(deploy_key.id, {"can_push": True})
            logger.info("%r enabled for %r", deploy_key, json_data_project)
    else:
        logger.info("SSH key pair is already configured for this fetcher")


def ensure_new_ci_conf(project: Project, ctx: Context):
    def is_shared_pipeline(include) -> bool:
        return include["project"] == fetcher_pipeline_project_name and include["file"] == ".gitlab-ci.template.yml"

    def replace_provider_slug(text: str) -> str:
        provider_slug_regex = r"(PROVIDER_SLUG: *).*"
        return re.sub(provider_slug_regex, rf"\1{ctx.provider_slug}", text)

    def get_shared_pipeline_file_content():
        fetcher_pipeline_project = ctx.gl.projects.get(fetcher_pipeline_project_name)
        return replace_provider_slug(
            fetcher_pipeline_project.files.get(file_path="examples/fetcher-gitlab-ci.yml", ref="master")
            .decode()
            .decode("utf-8")
        )

    try:
        gitlab_ci_file = project.files.get(file_path=".gitlab-ci.yml", ref="master")
    except gitlab.exceptions.GitlabGetError:
        logger.info("GitLab CI file not found, creating it from the shared pipeline template...")
        if not ctx.dry_run:
            gitlab_ci_file = project.files.create(
                {
                    "file_path": ".gitlab-ci.yml",
                    "branch": "master",
                    "content": get_shared_pipeline_file_content(),
                    "author_email": "dbnomics-fetcher-ops@localhost",
                    "author_name": "dbnomics-fetcher-ops",
                    "commit_message": "Add shared pipeline",
                }
            )
            logger.info(".gitlab-ci.yml file %r created in %r", gitlab_ci_file, project)
        return

    logger.info("Checking that fetcher repo uses the new .gitlab-ci.yml template...")
    gitlab_ci_yml = gitlab_ci_file.decode().decode("utf-8")
    gitlab_ci_conf = loaders.yaml.load(gitlab_ci_yml)

    if any(filter(is_shared_pipeline, gitlab_ci_conf.get("include", []))):
        logger.info(".gitlab-ci.yml already includes the shared pipeline template")
        new_gitlab_ci_yml = replace_provider_slug(gitlab_ci_yml)
        if gitlab_ci_yml != new_gitlab_ci_yml:
            logger.info(".gitlab-ci.yml does not mention the right provider slug, replacing it...")
    else:
        logger.info("Replacing .gitlab-ci.yml by the shared pipeline template...")
        new_gitlab_ci_yml = get_shared_pipeline_file_content()

    if new_gitlab_ci_yml != gitlab_ci_yml:
        gitlab_ci_file.content = new_gitlab_ci_yml
        if not ctx.dry_run:
            gitlab_ci_file.save(branch="master", commit_message="Use new shared CI pipeline")
            logger.info(".gitlab-ci.yml file %r updated in %r", gitlab_ci_file, project)


def ensure_json_data_webhooks(project: Project, ctx: Context):
    if not ctx.dry_run:
        solr_trigger_url = (
            f"{ctx.gitlab_api_base_url}/projects/{ctx.solr_project.id}/ref/master/trigger/pipeline?"
            + urllib.parse.urlencode({"token": ctx.solr_trigger.token, "variables[PROVIDER_SLUG]": ctx.provider_slug})
        )
        validate_trigger_url = (
            f"{ctx.gitlab_api_base_url}/projects/{ctx.data_model_project.id}/ref/master/trigger/pipeline?"
            + urllib.parse.urlencode(
                {"token": ctx.data_model_trigger.token, "variables[PROVIDER_SLUG]": ctx.provider_slug}
            )
        )
        hook_urls = [hook.url for hook in project.hooks.list(as_list=False)]
        if solr_trigger_url not in hook_urls:
            create_push_webhook(project, ctx, url=solr_trigger_url)
        if validate_trigger_url not in hook_urls:
            create_push_webhook(project, ctx, url=validate_trigger_url)


def create_push_webhook(project: Project, ctx: Context, *, branch_filter: str = "master", url: str):
    hook = project.hooks.create({"url": url, "push_events": 1, "push_events_branch_filter": branch_filter})
    logger.info("%r created for %r", hook, project)


def delete_triggers(project: Project, ctx: Context):
    logger.info("Deleting triggers of %r...", project)
    for trigger in project.triggers.list(as_list=False):
        if trigger.description != CI_JOBS_KEY:
            logger.warning("%r ignored, description: %r", trigger, trigger.description)
            continue
        if not ctx.dry_run:
            trigger.delete()
            logger.info("%r deleted from %r", trigger, project)
    else:
        logger.info("No trigger found for %r", project)


def update_pipeline_schedule(schedule: ProjectPipelineSchedule, project: Project, ctx: Context):
    dirty = set()
    if schedule.description != RUN_FETCHER:
        dirty.add("description")
        schedule.description = RUN_FETCHER
    if ctx.schedule_cron is not None and schedule.cron != ctx.schedule_cron:
        dirty.add("cron")
        schedule.cron = ctx.schedule_cron
    if ctx.schedule_cron_timezone is not None and schedule.cron_timezone != ctx.schedule_cron_timezone:
        dirty.add("cron_timezone")
        schedule.cron_timezone = ctx.schedule_cron_timezone
    if dirty:
        logger.info(
            "Updating %r attributes of %r of %r...", dirty, schedule, project,
        )
        if not ctx.dry_run:
            schedule.save()
            logger.info("%r of %r saved", schedule, project)


def delete_variable_from_schedule(schedule: ProjectPipelineSchedule, project: Project, ctx: Context):
    try:
        if not ctx.dry_run:
            schedule.variables.delete(JOB)
            logger.info(
                "Legacy variable %r deleted from %r of %r", JOB, schedule, project,
            )
    except gitlab.exceptions.GitlabDeleteError:
        logger.info(
            "Legacy variable %r was not found in %r of %r", JOB, schedule, project,
        )


def create_pipeline_schedule(project: Project, ctx: Context):
    logger.info("No schedule found for %r, creating one...", project)
    if not ctx.dry_run:
        schedule = project.pipelineschedules.create(
            {
                "active": True,
                "description": RUN_FETCHER,
                "ref": "master",
                "cron": ctx.schedule_cron if ctx.schedule_cron is not None else constants.SCHEDULE_CRON,
                "cron_timezone": ctx.schedule_cron_timezone
                if ctx.schedule_cron_timezone is not None
                else constants.SCHEDULE_CRON_TIMEZONE,
            }
        )
        logger.info(
            "%r created for %r", schedule, project,
        )


def ensure_pipeline_schedule(project: Project, ctx: Context):
    logger.info(
        "Ensuring that %r has at least one pipeline schedule...", project,
    )
    schedules = project.pipelineschedules.list()
    if len(schedules) == 0:
        create_pipeline_schedule(project, ctx)
    elif len(schedules) == 1:
        delete_variable_from_schedule(schedules[0], project, ctx)
        update_pipeline_schedule(schedules[0], project, ctx)
    else:
        logger.warning(
            "%d schedules found for %r, manual migration required at %s",
            len(schedules),
            project,
            f"{project.web_url}/-/pipeline_schedules",
        )


def delete_webhooks(project: Project, ctx: Context):
    logger.info("Deleting webhooks of %r...", project)
    for hook in project.hooks.list(as_list=False):
        if not ctx.dry_run:
            hook.delete()
            logger.info("%r deleted from %r", hook, project)
    else:
        logger.info("No webhook found for %r", project)


def create_project(group_name: str, project_name: str, description: str, ctx: Context):
    gl = ctx.gl
    groups = gl.groups.list(search=group_name)
    assert len(groups) == 1, groups
    group = groups[0]

    if not ctx.dry_run:
        project = gl.projects.create(
            {
                "name": project_name,
                "namespace_id": group.id,
                "description": description,
                "visibility": VISIBILITY_PUBLIC,
            }
        )
        logger.info("Project created: %r", project)
    return project
