import fnmatch
import os
import shlex
import subprocess
import sys
from collections import OrderedDict
from typing import Dict, List, Union

import confuse
import typer

from repo_tools.common.structs import ProjectInfo, ProjectFeatures

APP_NAME = "repo_tools"


def save_config(config_values: Dict, overwrite: bool = False) -> None:
    config = read_config()
    config_dir = config.config_dir()
    config_filename = confuse.CONFIG_FILENAME

    if overwrite or not config.exists():
        config.clear()
        config.add(config_values)
    else:
        existing_config_values = config.get()
        existing_config_values.update(config_values)
        config.clear()
        config.add(existing_config_values)

    config_full_path = os.path.join(config_dir, config_filename)
    with open(config_full_path, "w") as file:
        file.seek(0)
        file.write(config.dump())
        file.truncate()

    exit_cli(message=f"Configuration File updated at {config_full_path}", status_code=0)


def read_config() -> confuse.Configuration:
    return confuse.Configuration(APP_NAME)


# HELPERS


def get_github_oauth_token():
    return get_config_value("github.oauth_token")


def get_github_org():
    return get_config_value("github.org")


def get_config_value(key: str) -> Union[str, OrderedDict]:
    configuration = read_config().flatten()

    keys = key.split(".")

    config_value = ""
    try:
        for key in keys:
            config_value = configuration.get(key, {})
            configuration = config_value
        config_value = config_value
        return config_value
    except (confuse.ConfigValueError, confuse.NotFoundError):
        exit_cli(f"Please use 'config set' and add a value for '{key}'", status_code=1)


def exit_cli(message: str, status_code: int) -> None:
    status_symbol = "✅" if status_code == 0 else "❌"
    typer.echo(f"{status_symbol}  {message}")
    sys.exit(status_code)


def get_projects(
    feature: str = "", include: str = "", exclude: str = "", glob_pattern: str = ""
) -> List:
    projects = _get_projects_list()
    return _filter_projects(projects, feature, glob_pattern, include, exclude)


def _get_projects_list() -> List[ProjectInfo]:
    configuration = read_config()
    try:
        config = configuration["projects"].get()
        projects = [
            ProjectInfo(
                name=name,
                abs_path=project["abs_path"],
                features=ProjectFeatures(**project["features"]),
            )
            for name, project in config.items()
        ]
        return projects
    except confuse.exceptions.NotFoundError:
        return []


def _filter_projects(
    projects: List[ProjectInfo],
    feature: str = "",
    glob_pattern: str = "",
    include: str = "",
    exclude: str = "",
) -> List[ProjectInfo]:
    excluded_projects = exclude.lower().split(",") if exclude else []
    included_projects = include.lower().split(",") if include else []

    if feature:
        projects = list(filter(lambda p: getattr(p.features, feature), projects))

    if excluded_projects:
        projects = list(
            filter(lambda p: p.name.lower() not in excluded_projects, projects)
        )

    if included_projects:
        projects = list(filter(lambda p: p.name.lower() in included_projects, projects))

    if glob_pattern:
        if glob_pattern.startswith("!"):
            projects = list(
                filter(
                    lambda p: not fnmatch.fnmatch(
                        p.name.lower(), glob_pattern.lstrip("!")
                    ),
                    projects,
                )
            )
        else:
            projects = list(
                filter(
                    lambda p: fnmatch.fnmatch(p.name.lower(), glob_pattern), projects
                )
            )

    projects = sorted(projects, key=lambda p: p.name)

    return projects


def execute_command(command: str, cwd: str):
    try:
        status_code = 0
        out = subprocess.check_output(
            shlex.split(command), cwd=cwd, stderr=subprocess.STDOUT
        )
        out = out.decode("utf-8")
    except subprocess.CalledProcessError as exc:
        status_code = exc.returncode
        out = exc.output.decode("utf-8")
    except Exception as exc:
        status_code = 1
        out = f"An unexpected error occurred: {exc}"
    return out, status_code


def execute_command_for_project(project: ProjectInfo, command: str):
    out, status = execute_command(command, cwd=project.abs_path)
    display_command_output(project.name, out, status)


def display_command_output(header: str, message: str, status_code: int):
    color = typer.colors.GREEN if status_code == 0 else typer.colors.RED
    typer.echo(typer.style(f"{header}:", fg=color, bold=True))
    typer.echo(_format_output(message))


def _format_output(message: str) -> str:
    message = [" " * 4 + line for line in message.splitlines()]
    return "\n".join(message)
