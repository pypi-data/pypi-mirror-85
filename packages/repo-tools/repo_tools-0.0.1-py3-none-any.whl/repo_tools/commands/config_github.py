import json
import os
from typing import Optional

import typer
import yaml
from tabulate import tabulate

from repo_tools.common import utils
from repo_tools.common.structs import OutputFormat

config_github_app = typer.Typer()


@config_github_app.command(
    help="Detects the github oauth_token from 'gh' tool (if exists)"
)
def detect(path: str = typer.Argument(""), overwrite: bool = typer.Option(False)):
    gh_host_config_path = os.path.join(os.path.expanduser("~/.config/gh/hosts.yml"))
    if path:
        gh_host_config_path = path

    with open(gh_host_config_path) as f:
        config = yaml.load(f, Loader=yaml.FullLoader)

    github_oauth_token = config.get("github.com", {}).get("oauth_token", "")

    if not github_oauth_token:
        utils.exit_cli(
            "Failed to detect github oauth token, use 'config gh setup' instead.",
            status_code=1,
        )
    utils.save_config({"github": {"oauth_token": github_oauth_token}}, overwrite)


@config_github_app.command(help="Setup multi to interact with github")
def setup(
    token: Optional[str] = typer.Option(
        None, prompt="Please input your GitHub API token"
    ),
    org: Optional[str] = typer.Option(
        None, prompt="Please input your GitHub organization/username"
    ),
    overwrite: bool = typer.Option(False),
):
    utils.save_config({"github": {"oauth_token": token, "org": org}}, overwrite)


@config_github_app.command(help="Show the current github configuration")
def show(
    fmt: OutputFormat = typer.Option(
        "table", "--format", "-fmt", help="show output as table or json"
    ),
):
    github_config_values = utils.get_config_value("github")
    if not github_config_values:
        utils.exit_cli(
            "Please use 'config gh detect' or 'config gh setup' to set github config.",
            status_code=1,
        )

    github_config = [[key, value] for key, value in github_config_values.items()]
    if fmt == OutputFormat.table:
        out = tabulate(github_config, headers=["Key", "Value"], colalign=("right",))
    if fmt == OutputFormat.json:
        out = json.dumps(
            github_config_values,
            indent=4,
            sort_keys=True,
        )
    typer.echo(out)
