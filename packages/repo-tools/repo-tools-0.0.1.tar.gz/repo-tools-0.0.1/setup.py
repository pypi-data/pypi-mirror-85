# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['repo_tools', 'repo_tools.commands', 'repo_tools.common']

package_data = \
{'': ['*'], 'repo_tools': ['snippets/*']}

install_requires = \
['GitPython>=3.1,<4.0',
 'PyGithub==1.53',
 'PyYAML>=5.3,<6.0',
 'confuse>=1.3,<2.0',
 'tabulate>=0.8,<0.9',
 'typer[all]>=0.3,<0.4']

entry_points = \
{'console_scripts': ['multi = repo_tools.main:app', 'rt = repo_tools.main:app']}

setup_kwargs = {
    'name': 'repo-tools',
    'version': '0.0.1',
    'description': 'A multi-repo CLI to help operating on multiple repos at the same time.',
    'long_description': '# repo-tools\n\n[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)\n[![CircleCI](https://circleci.com/gh/lightspeed-hospitality/repo-tools.svg?style=svg&circle-token=fbdf038d40feb74aec465d01c7aa15b7ee74062a)](https://app.circleci.com/pipelines/github/lightspeed-hospitality/repo-tools)\n\n<p align="center">\n  <a href="#development">Development</a> •\n  <a href="#architecture--documentation">Documentation</a> •\n  <a href="#how-to-contribute">Contribute</a> •\n  <a href="#support--feedback">Support</a>\n</p>\n\nThis is a small Multi Repo CLI that allows you to apply changes to multiple projects at the same time.\n\n---\n\n## Use it!\n\n```console\npip install repo-tools\n```\n\n```console\n$ rt --help\nUsage: rt [OPTIONS] COMMAND [ARGS]...\n\nOptions:\n  --install-completion  Install completion for the current shell.\n  --show-completion     Show completion for the current shell, to copy it or\n                        customize the installation.\n\n  --help                Show this message and exit.\n\nCommands:\n  config   Configure repo_tools\n  exec     Execute an arbitrary command\n  gh       Interact with github\n  snippet  Run snippets (custom snippets can be registered)\n```\n\n### Required Setup\n\n* Display your config:\n```console\nrt config show\n```\n\n* Create your Github config:\n```console\nrt config gh setup\n```\n_Note_:\nTo create your config you will need to have a Personal Github Oauth Token, that can be created [here](https://github.com/settings/tokens).\nMake sure to give it `repo:all` permissions.\n\n\n* Register Projects\n```console\nrt config projects detect ./<your-projects-dir>\n```\n\n* Register Snippets\n```console\nrt snippet register <path-to-snippet-file> | <path-to-dir-with-snippets>\n```\n\n## Development\n\n### Setup\n\nThis project uses poetry for dependency management, let\'s install it:\n```console\npip install poetry\n```\n\n### Run\n\nYou can use poetry to install all dependencies and use the current state of the CLI as follows:\n```console\npoetry install\npoetry shell # opens new shell in virtual env\n> rt config show\n> ...\n```\n\n## How to Contribute\n\nIn order to contribute you just have to have Python installed on your machine. In case you do not have it installed get it from [python.org](https://www.python.org/downloads/).\n\n#### Linting Tool\n\nThis project is using [pre-commit](https://pre-commit.com/) to enable linting and auto-formatting as a pre-commit hook.\nThe hooks are configured in [.pre-commit-config.yaml](./.pre-commit-config.yaml).\n\nTo install the hooks you have to run the following command (only once):\n```bash\npip install pre-commit\npre-commit install\n```\n\nThen you can trigger all the hooks manually by running:\n```bash\npoetry install\npoetry run pre-commit run --all-files\n```\n\nAdditionally on every `git commit` the hooks will be triggered and have to pass.\n\n#### How to run tests\n\nYou can run all the tests, by simply running:\n```bash\npoetry install\npoetry run pytest -vv\n```\n\n## Support & Feedback\n\nYour contribution is very much appreciated. Feel free to create a PR or an Issue with your suggestions for improvements.\n',
    'author': 'Lightspeed Hospitality',
    'author_email': 'pt.hospitality.dev@lightspeedhq.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
