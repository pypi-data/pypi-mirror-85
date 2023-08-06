#! /usr/bin/env python3

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

"""CLI to manage DBnomics fetchers."""


import logging

import daiquiri
import typer
from dotenv import load_dotenv

from . import app_args, constants, loaders
from .commands.configure import configure_command
from .commands.list import list_command

# Do this before calling os.getenv().
load_dotenv()

logger = daiquiri.getLogger(__name__)

app = typer.Typer()
app.command(name="configure")(configure_command)
app.command(name="list")(list_command)


@app.callback()
def callback(
    ctx: typer.Context,
    debug: bool = typer.Option(False, "-d", "--debug", help="Display DEBUG log messages"),
    verbose: bool = typer.Option(False, "-v", "--verbose", help="Display INFO log messages"),
    fetchers_yml: str = typer.Option(
        constants.FETCHERS_YML_URL, envvar="FETCHERS_YML_URL", help="Path or URL to fetchers.yml", show_default=True
    ),
):
    """Manage DBnomics fetchers."""
    daiquiri.setup(level=logging.DEBUG if debug else logging.INFO if verbose else logging.WARNING)

    app_args.app_args = app_args.AppArgs(
        debug=debug, fetchers_metadata=loaders.load_fetchers_from_yaml(fetchers_yml), verbose=verbose,
    )


def main():
    app()


if __name__ == "__main__":
    main()
