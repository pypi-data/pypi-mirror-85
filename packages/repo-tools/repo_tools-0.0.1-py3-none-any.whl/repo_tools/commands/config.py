import json
from enum import Enum

import typer
import yaml

from repo_tools.commands.config_github import config_github_app
from repo_tools.commands.config_projects import config_projects_app
from repo_tools.common import utils

config_app = typer.Typer()

config_app.add_typer(
    config_projects_app, name="projects", help="Config options for projects"
)
config_app.add_typer(config_github_app, name="gh", help="Config options for github")


@config_app.command(
    help="Get the value of a config key (also nested keys e.g. github.org)"
)
def get(key: str = typer.Argument(...)):
    config_value = utils.get_config_value(key)
    if isinstance(config_value, str):
        typer.echo(config_value)
        return
    out = json.dumps(
        config_value,
        indent=4,
        sort_keys=True,
    )
    typer.echo(out)


@config_app.command(help="Set/Update a new config key with a value")
def set(key: str = typer.Argument(...), value: str = typer.Argument(...)):
    utils.save_config({key: value})
    typer.echo(utils.get_config_value(key))


class ConfigOutputFormat(Enum):
    yml = "yml"
    json = "json"


@config_app.command(help="Display the full repo_tools config file")
def show(
    fmt: ConfigOutputFormat = typer.Option(
        "yml", "--format", "-fmt", help="show output as yml or json"
    ),
):
    config_values = utils.read_config()
    if not config_values:
        utils.exit_cli(
            "No config detected.",
            status_code=1,
        )

    if fmt == ConfigOutputFormat.yml:
        out = config_values.dump()
    if fmt == ConfigOutputFormat.json:
        out = json.dumps(
            yaml.load(config_values.dump(), Loader=yaml.FullLoader),
            indent=4,
            sort_keys=True,
        )
    typer.echo(out)
