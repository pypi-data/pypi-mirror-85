import os
from collections import OrderedDict
from typing import Optional

import typer
from tabulate import tabulate

from repo_tools.common import utils
from repo_tools.common.help_texts import HelpText

snippet_app = typer.Typer()

SNIPPETS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../snippets"))


@snippet_app.command(help="List all available snippets")
def ls():
    snippets = _get_snippets()
    table_data = []
    for index, snippet in enumerate(snippets.items()):
        if snippet[1].get("builtin"):
            table_data.append([index + 1, snippet[0], "built-in"])
        else:
            table_data.append([index + 1, snippet[0], "custom"])
    typer.echo(tabulate(table_data, headers=["#", "name", "type"]))
    return snippets


@snippet_app.command(help="Execute a snippet")
def run(
    name: str = typer.Argument(""),
    args: str = typer.Argument("", help="Extra arguments to pass to the script"),
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
    snippet_name = None
    snippets = _get_snippets()

    if not name:
        ls()
        snippet_id = int(typer.prompt("ID of the snippet you want to execute")) - 1
        snippet_name = [name for name in snippets.keys()][snippet_id]
        if not args:
            args = str(
                typer.prompt(
                    "Type extra arguments to pass to the snippet",
                    default="",
                    show_default=True,
                )
            )

    if name and name not in snippets:
        utils.exit_cli(
            f"Snippet '{name}' does not exist. See 'snippet list' for available snippets",
            status_code=1,
        )
    if name and name in snippets:
        snippet_name = name

    if snippet_name is None:
        utils.exit_cli(
            "Failed to execute command. Check 'snippet --help' for usage",
            status_code=1,
        )

    snippet_path = snippets[snippet_name].get("path")

    command = f"{snippet_path}"
    if args:
        command += f" {args}"

    projects = utils.get_projects(feature, include, exclude, glob_pattern=glob)
    for project in projects:
        utils.execute_command_for_project(project, command)


@snippet_app.command(
    help="Register snippet(s) to repo_tools (path to file/path to dir)"
)
def register(path: str = typer.Argument(...)):
    snippets_config = utils.get_config_value("snippets")
    config = OrderedDict() if not snippets_config else snippets_config

    if os.path.isdir(path):
        files = os.listdir(path)
        for file in files:
            snippet_path = os.path.abspath(os.path.join(path, file))
            if _check_shebang(snippet_path):
                config[file] = snippet_path
            else:
                typer.echo(f"Snippet {path} does not have a shebang as first line.")

    if os.path.isfile(path):
        filename = path.rsplit("/", 1)[-1]
        if _check_shebang(path):
            config[filename] = os.path.abspath(path)
        else:
            typer.echo(f"Snippet {path} does not have a shebang as first line.")

    utils.save_config({"snippets": config})


@snippet_app.command(help="Unregister a snippet from repo_tools")
def unregister(name: str = typer.Argument("")):
    snippet_name = None
    snippets = _get_snippets()

    if not name:
        ls()
        snippet_id = int(typer.prompt("ID of the snippet you want to unregister")) - 1
        snippet_name = [name for name in snippets.keys()][snippet_id]

    if name and name not in snippets:
        utils.exit_cli(
            f"Snippet '{name}' does not exist. See 'snippet list' for available snippets",
            status_code=1,
        )
    if name and name in snippets:
        snippet_name = name

    if snippet_name is None:
        utils.exit_cli(
            "Failed to execute command. Check 'snippet --help' for usage",
            status_code=1,
        )

    if snippets.get(snippet_name)["builtin"]:
        utils.exit_cli(
            "Built-in snippets cannot be unregistered. Check 'snippet --help' for usage",
            status_code=1,
        )

    snippets_config = utils.get_config_value("snippets")
    del snippets_config[snippet_name]
    utils.save_config({"snippets": snippets_config})

    typer.echo(f"Unregistered {snippet_name}")


def _check_shebang(path: str) -> bool:
    with open(path) as f:
        first_line = f.readline()
    return "#!" in first_line


def _get_snippets() -> OrderedDict:
    snippets = OrderedDict()
    # built-in snippets
    built_in_snippets = os.listdir(SNIPPETS_DIR)
    for snippet in built_in_snippets:
        snippets[snippet] = {
            "path": os.path.abspath(os.path.join(SNIPPETS_DIR, snippet)),
            "builtin": True,
        }
    # from config
    custom_snippets = utils.get_config_value("snippets")
    for snippet_name, path in custom_snippets.items():
        snippets[snippet_name] = {"path": path, "builtin": False}

    return snippets
