# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ee_cli']

package_data = \
{'': ['*']}

install_requires = \
['pendulum>=2.1.2,<3.0.0',
 'pydantic>=1.6.1,<2.0.0',
 'pyperclip>=1.8.0,<2.0.0',
 'typer>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['ee = ee_cli.main:app']}

setup_kwargs = {
    'name': 'ee-cli',
    'version': '1.0.1',
    'description': 'A salve for timesmiths',
    'long_description': '# epoch-echo\n\nA minimal command line alternative to tools like [this](https://www.epochconverter.com).\n\nBuilt with ✨and [typer](https://github.com/tiangolo/typer).\n\n## About\n\nBorn from the grumblings of a crunchy shell-dweller, `ee-cli` is designed to fit nicely in a terminal-heavy workflow with tools like [tmux](https://github.com/tmux/tmux/wiki), [hub](https://github.com/github/hub), [fzf](https://github.com/junegunn/fzf), etc. (This and all my cli tools are inspired by these and others.)\n\n`ee` stands for "epoch echo" because that\'s sort of what the tool does.\n\nThe 2 commands both take inputs as either epoch timestamps or datetimes and print them back as the opposite. `ee` uses [pendulum](https://pendulum.eustace.io) for these conversions. By default, `ee` supports the [same datetime formats](https://pendulum.eustace.io/docs/#rfc-3339) as `pendulum.parse`.\n\nCopypasta your machine-flavored datetimes from the db or whatever into the `ee repl` interface, and ahhhh 😌 a nice human date right there for you in 0 clicks 🌚. Pass a whole long list of some ridiculous mixture of epoch dates and readable datetimes to `ee flip` and witness 🙀 the grand switcharoo 🎠\n\n## Installation\n\nThis is a Python project, so you install it from pip.\n\n```shell\npip install ee-cli\n```\n\nThe executable is `ee`\n\n```shell\nee --help # display help and list commands\n```\n\n# Usage\n\nInteractive (`ee -R`):\n\n![](./repl.gif)\n\nNon-interactive (`ee`):\n\n![](./flip.gif)\n\nGifs courtesy of [terminalizer](https://github.com/faressoft/terminalizer).\n\nSee [USAGE.md](./USAGE.md) for more\n',
    'author': 'Ainsley',
    'author_email': 'mcgrath.ainsley@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
