"""
Defines the command line interface.
Uses click to define a CLI around the ``main`` function.
"""
import pathlib
import sys
import traceback

import click
import tomli
import pathspec


@click.command(context_settings={"help_option_names": ["-h", "--help"]})
@click.option(
    "--extension",
    "-e",
    default="py,c,h,sh",
    show_default=True,
    help="Extensions of files that will be crawled. Should be a single string "
    "or a comma separated list (no spaces) and should NOT include a leading '.'",
)
@click.option(
    "--verbose/--quiet",
    "-v/-q",
    default=True,
    show_default=True,
    help="Print information during execution / Don't print",
)
@click.version_option()
@click.argument(
    "directory", type=click.Path(exists=True, file_okay=False, path_type=pathlib.Path)
)
def main(extension, verbose, directory):
    """
    Burocrata: Check and insert copyright and license notices into source code

    The license notice MUST be set in a 'pyproject.toml' file located in the
    current directory like so:

        [tool.burocrata]
        notice = '''
        # Copyright (c) YYYY Name of Developer.
        # Distributed under the terms of the BSD 3-Clause License.
        # SPDX-License-Identifier: BSD-3-Clause
        '''

    """
    reporter = Reporter(verbose)
    extensions = extension.split(",")
    try:

        config_file = pathlib.Path("./pyproject.toml")
        if not config_file.exists():
            reporter.error(
                "Missing pyproject.toml configuration file in the current directory."
            )
            sys.exit(1)
        with open(config_file, "rb") as file:
            config = tomli.load(file)
        if (
            "tool" not in config
            or "burocrata" not in config["tool"]
            or "notice" not in config["tool"]["burocrata"]
        ):
            reporter.error(
                "Missing license/copyright notice in pyproject.toml configuration file:"
            )
            reporter.error(config_file.read_text())
            sys.exit(1)
        notice = config["tool"]["burocrata"]["notice"].split("\n")

        gitignore = get_gitignore()

        missing_notice = []
        for ext in extensions:
            for path in directory.glob(f"**/*.{ext}"):
                if gitignore.match_file(path):
                    continue
                with open(path) as file:
                    for notice_line, file_line in zip(notice, file):
                        if notice_line != file_line:
                            missing_notice.append(path)
                            break

        print(missing_notice)

    except Exception:
        reporter.error("\nError encountered while processing:\n")
        reporter.error(traceback.format_exc())
        reporter.error("Oh no! Something went wrong. See the messages above.")
        sys.exit(1)


# The get_gitignore function is a modified version of the one present in Black
# and Harmonica, both available under the MIT License.
# https://github.com/psf/black
# https://github.com/fatiando/harmonica/tree/v0.6.0
def get_gitignore():
    """
    Return a PathSpec matching gitignore content if present.
    """
    gitignore = pathlib.Path(".") / ".gitignore"
    lines = []
    if gitignore.is_file():
        with gitignore.open() as gi_file:
            lines = gi_file.readlines()
    return pathspec.PathSpec.from_lines("gitwildmatch", lines)


# The Reporter class is originally from software Dependente:
# https://github.com/fatiando/dependente
# Copyright (c) 2021 Leonardo Uieda.
# Distributed under the terms of the MIT License.
class Reporter:
    """
    Small wrapper around click.echo to control verbosity.

    Use *echo* to print according to verbosity settings and *error* to always
    print regardless of settings.
    """

    def __init__(self, verbose):
        self.verbose = verbose

    def echo(self, message):
        """
        Print the message if verbosity is enabled.
        """
        if self.verbose:
            click.echo(message, err=True)

    def error(self, message):
        """
        Print the message regardless of verbosity settings.
        """
        click.echo(message, err=True)
