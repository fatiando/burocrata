# Copyright (c) 2024 The Burocrata Developers.
# Distributed under the terms of the MIT License.
# SPDX-License-Identifier: MIT
# This code is part of the Fatiando a Terra project (https://www.fatiando.org).
"""
Defines the command line interface.
Uses click to define a CLI around the ``main`` function.
"""

import pathlib
import sys
import traceback

import click
import pathspec
import tomli


@click.command(context_settings={"help_option_names": ["-h", "--help"]})
@click.option(
    "--extension",
    "-e",
    default="py",
    show_default=True,
    help="Extensions of files that will be crawled. Should be a single string "
    "or a comma separated list (no spaces) and should not include a leading '.'",
)
@click.option(
    "--check",
    "-c",
    default=False,
    is_flag=True,
    show_default=True,
    help="Only check for the presence of a notice and report which files are missing it.",
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
def main(extension, check, verbose, directory):
    """
    Burocrata: Check and insert copyright and license notices into source code

    The license notice MUST be set in a 'pyproject.toml' file located in the
    current directory that specifies the license notice.

    By default, will crawl the given directory and add the license notice to
    every file with the given extensions that doesn't already have it.
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
        amount = 0
        for ext in extensions:
            for path in directory.glob(f"**/*.{ext}"):
                if gitignore.match_file(path):
                    continue
                amount += 1
                with open(path) as file:
                    for notice_line, file_line in zip(notice, file):
                        # Use [:-1] to strip the newline from the end
                        if notice_line != file_line[:-1]:
                            missing_notice.append(path)
                            break
        reporter.echo(
            f"Found {amount} file(s) in '{str(directory)}' ending in {extension}."
        )

        if missing_notice:
            print(f"Found {len(missing_notice)} file(s) without the license notice:")
            for path in missing_notice:
                print(f"  {str(path)}")
            if check:
                sys.exit(1)
        else:
            print("No files found with a missing license notice")
            sys.exit(0)

        for path in missing_notice:
            source_code = notice.copy()
            source_code.extend(path.read_text().split("\n"))
            with open(path, "w") as output:
                output.write("\n".join(source_code))
        print(f"Successfully added the license notice to {len(missing_notice)} files.")
        sys.exit(0)

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

    def echo(self, message=""):
        """
        Print the message if verbosity is enabled.
        """
        if self.verbose:
            click.echo(message, err=True)

    def error(self, message=""):
        """
        Print the message regardless of verbosity settings.
        """
        click.echo(message, err=True)
