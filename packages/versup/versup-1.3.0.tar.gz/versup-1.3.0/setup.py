# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['versup']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.0,<8.0',
 'colorama>=0.4.3,<0.5.0',
 'gitpython>=3.0,<4.0',
 'semver>=2.8,<3.0']

entry_points = \
{'console_scripts': ['versup = versup.__main__:main']}

setup_kwargs = {
    'name': 'versup',
    'version': '1.3.0',
    'description': 'Version up your project with ease.',
    'long_description': '# versup\n\n[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)\n[![Documentation Status](https://readthedocs.org/projects/versup/badge/?version=latest)](https://versup.readthedocs.io/en/latest/?badge=latest)\n[![PyPI version](https://badge.fury.io/py/versup.svg)](https://badge.fury.io/py/versup)\n[![Build Status](https://travis-ci.com/Svenito/versup.svg?branch=master)](https://travis-ci.com/Svenito/versup)\n[![Coverage Status](https://coveralls.io/repos/github/Svenito/versup/badge.svg?branch=master)](https://coveralls.io/github/Svenito/versup?branch=master)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\nBump your project version, update version numbers in your files, create a changelog,\nmake a commit, and tag it, all in one easy step. versup is also quite configurable.\n\n# Install\n\nInstall with either poetry\n\n`poetry install`\n\nor pip\n\n`pip install .`\n\n# Quick start\n\nTo get started all versup needs to know is the new version increment or number.\nYou can provide it with a valid semantic version increase such as `patch`, `minor`,\n`major` etc, or an entirely new semantic version like `1.2.5`.\n\nIf you specifiy a version number, then versup will take that version and apply\nit to the current project as is. If you provide an increment, it will get the\nlast version number from either the latest git tag that has a valid version,\nor from the default version in the config file.\n\n# Configuration\n\nVersup has a default configuration which is shown below\n\n```\n{\n    "force": False,  # Force the command without prompting the user\n    "silent": False,  # Minimize the amount of logs\n    "files": {},  # A map of `relativeFilePath: [regex, replacement, regexFlags?] | [regex, replacement, regexFlags?][]`\n    "version": {\n        "enabled": True,  # Bump the version number\n        "initial": "0.0.0",  # Initial version\n        "increments": [\n            "major",\n            "minor",\n            "patch",\n            "prerelease",\n            "build",\n        ],  # List of available increments to pick from\n    },\n    "changelog": {\n        "enabled": True,  # Enable changelog auto-updates\n        "create": False,  # Create the changelog file if it doesn"t exist\n        "open": True,  # Open the changelog file after bumping\n        "file": "CHANGELOG.md",  # Name of the changelog file\n        "version": "### Version [version]",  # Template for the version line\n        "commit": "- [message]",  # Template for the commit line\n        "separator": "\\n",  # Template for the separator between versions sections\n    },\n    "commit": {\n        "enabled": True,  # Commit the changes automatically\n        "message": "Update version to [version]",  # Template for the commit message\n        "mainbranch": "master",  # name of the main development or release branch\n    },\n    "tag": {\n        "enabled": True,  # Tag the bump commit\n        "name": "v[version]",  # Template for the name of the tag in the tag message\n    },\n    "tokens": {\n        "date": {\n            "format": "%Y-%m-%d"  # Python datetime format to use when generating the `[date]` token\n        },\n        "version_date": {\n            "format": "%Y-%m-%d"  # Python datetime format to use when generating the `[version_date]` token\n        },\n    },\n    "scripts": {\n        "prebump": "",  # Script to execute before bumping the version\n        "postbump": "",  # Script to execute after bumping the version\n        "prechangelog": "",  # Script to execute before updating the changelog\n        "postchangelog": "",  # Script to execute after updating the changelog\n        "precommit": "",  # Script to execute before committing\n        "postcommit": "",  # Script to execute after committing\n        "pretag": "",  # Script to execute before tagging\n        "posttag": "",  # Script to execute after tagging\n    },\n}\n\n```\n\nIf you want to override any settings, you can do this by creating a `~/.config/versup.json`\nfile or a `.versup.json` in your local project. Versup will read its default settings,\nthen merge in the global config (`~/.config/versup.json`), and finally\nmerge in the project level config.\n\n# Template tags\n\nIn various places you can define what text to use for commit messages, or tags etc.\nThese support tag fields that are replaced with relevant information. Known fields are:\n\n- version: The new version\n- message: The new commit message\n- date: Today\'s date formatted according to `tokens/date/format` in the config\n- version_date: Today\'s date formatted according to `tokens/version_date/format` in the config\n- hash: The new commit hash, full length\n- hash4: The new commit hash, first four characters\n- hash7: The new commit hash, first seven characters\n- hash8: The new commit hash, first eight characters\n- author_name: The author name from the git config\n- author_email: The author email from the git config\n\n# Updating files\n\nversup can update versions in files. The way this works is by configuring a regex\nfor each file that you want to update. So for example:\n\n```\n"files": {\n    "README.rst": [\n      ["Version ([\\\\d\\\\.]+) ", "Version [version] "],\n      ["Version is ([\\\\d\\\\.]+)", "Version is [version]"]\n    ]\n  },\n```\n\nHere the file `README.rst` is updated by matching a regex `Version ([\\\\d\\\\.]+)`\nwhich will match any text like `Version 1.3` or `Version 1.3.7`. They are standard\nregular expressions. The text that is matched is then replaced with the next argument\n`Version [version]` where `[version]` is the new version. You can regex and replace on\nanything really.\n\nThe supported increments are those supported by [Python Semver](https://python-semver.readthedocs.io/en/latest/usage.html#raising-parts-of-a-version)\n\n- major\n- minor\n- patch\n- prerelease\n- build\n\n# Scripts\n\nThere are a number of pre and post scripts that can be executed at various\nstages of the bump process. These are under the `scripts` section. They are\ncalled as-is and receive the new version number as the only argument. They\ncan be anything, shell scripts, python scripts, etc, but they must be\nexecutable in a regular shell, as they will be invoked as such.\n\nFull Read The Docs can be found at [https://versup.readthedocs.io](https://versup.readthedocs.io)\n',
    'author': 'Sven Steinbauer',
    'author_email': 'sven@unlogic.co.uk',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/unlogic/versup',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
