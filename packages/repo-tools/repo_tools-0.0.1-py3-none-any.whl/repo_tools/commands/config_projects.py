import json
import os
from collections import OrderedDict
from copy import deepcopy
from dataclasses import asdict
from typing import Optional

import typer
from tabulate import tabulate

from repo_tools.common import utils
from repo_tools.common.help_texts import HelpText
from repo_tools.common.structs import ProjectInfo, OutputFormat

config_projects_app = typer.Typer()

FEATURES = ["git", "circleci", "helm", "js", "python", "mvn", "docker"]
HEADERS = ["Project"] + FEATURES


@config_projects_app.command(
    help="Detect and register projects (with its features) that multi should act on"
)
def detect(
    path: Optional[str] = typer.Argument("."), overwrite: bool = typer.Option(False)
):
    cwd = os.path.abspath(os.path.join(os.getcwd(), path))
    typer.echo(f"Scanning for git repos in '{cwd}'...")

    projects = OrderedDict()

    for directory in sorted(os.listdir(cwd)):
        if directory.startswith("."):
            # dot directories are not interesting
            continue

        path = os.path.join(cwd, directory)
        if os.path.isdir(path):
            if ".git" not in os.listdir(path):
                # Top-level is not a git repository
                continue

        project = deepcopy(ProjectInfo())

        for (dir_path, dirs, files) in os.walk(path):
            if ".git" in dirs:
                project.abs_path = os.path.abspath(dir_path)
                project.name = project.abs_path.rsplit("/", 1)[-1]
                typer.echo(f"✅  Git repo found: {project.name}")
                project.features.git = True

            if ".circleci" in dirs:
                project.features.circleci = True

            if "charts" in dirs:
                project.features.helm = True

            if "package.json" in files or "manifest.json" in files:
                project.features.js = True

            if (
                "requirements.txt" in files
                or "setup.py" in files
                or "pyproject.toml" in files
            ):
                project.features.python = True

            if "pom.xml" in files or "mvnw" in files:
                project.features.maven = True

            if "Dockerfile" in files:
                project.features.docker = True

        projects[project.name] = asdict(project)

    config = {"projects": projects}
    utils.save_config(config, overwrite)


@config_projects_app.command(
    help="Show the currently registered projects with its detected features"
)
def show(
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
    fmt: OutputFormat = typer.Option(
        "table", "--format", "-fmt", help="show output as table or json"
    ),
):
    projects = utils.get_projects(feature, include, exclude, glob_pattern=glob)
    if not projects:
        utils.exit_cli(
            "Please use 'config detect' to scan for projects.", status_code=1
        )

    projects_display = [
        [project.name] + project.features.get_list() for project in projects
    ]
    if fmt == OutputFormat.table:
        out = tabulate(projects_display, headers=HEADERS, colalign=("right",))
    if fmt == OutputFormat.json:
        out = json.dumps(
            [json.loads(project.to_json()) for project in projects],
            indent=4,
            sort_keys=True,
        )
    typer.echo(out)
