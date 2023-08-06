#!/usr/local/bin/python
import os
from typing import Optional

import typer

from repo_tools.commands.config import config_app
from repo_tools.commands.github import github_app
from repo_tools.commands.snippet import snippet_app
from repo_tools.common import utils
from repo_tools.common.help_texts import HelpText

app = typer.Typer()

app.add_typer(config_app, name="config", help="Configure repo_tools")
app.add_typer(github_app, name="gh", help="Interact with github")
app.add_typer(
    snippet_app, name="snippet", help="Run snippets (custom snippets can be registered)"
)


@app.command(help="Execute an arbitrary command", no_args_is_help=True)
def exec(
    command: str = typer.Argument(...),
    glob: Optional[str] = typer.Option(
        "",
        "--glob",
        "-g",
        help=HelpText.GLOB,
    ),
    feature: Optional[str] = typer.Option(
        "",
        "--feature",
        "-f",
        help=HelpText.FEATURE,
    ),
    include: Optional[str] = typer.Option("", "--include", "-i", help=HelpText.INCLUDE),
    exclude: Optional[str] = typer.Option("", "--exclude", "-e", help=HelpText.EXCLUDE),
):
    projects = utils.get_projects(feature, include, exclude, glob_pattern=glob)

    for project in projects:
        utils.execute_command_for_project(project, command)


@app.command(help="Display current version")
def version():
    version_file_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "VERSION")
    )
    with open(version_file_path) as f:
        v = f.readline()
    typer.echo(f"CLI Version: {v}")
    raise typer.Exit()
