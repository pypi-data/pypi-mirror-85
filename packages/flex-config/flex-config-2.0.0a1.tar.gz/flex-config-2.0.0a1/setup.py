# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['flex_config']

package_data = \
{'': ['*']}

install_requires = \
['autoflake>=1.4,<2.0', 'flake8>=3.8.4,<4.0.0', 'pydantic>=1.7.2,<2.0.0']

extras_require = \
{'all': ['boto3>=1.13.1,<2.0.0', 'pyyaml>=5.3.1,<6.0.0'],
 'aws': ['boto3>=1.13.1,<2.0.0'],
 'yaml': ['pyyaml>=5.3.1,<6.0.0']}

setup_kwargs = {
    'name': 'flex-config',
    'version': '2.0.0a1',
    'description': 'Easily configure Python apps via environment variables, YAML, and AWS SSM Param Store.',
    'long_description': '# Flex Config\n[![triaxtec](https://circleci.com/gh/triaxtec/flex-config.svg?style=svg)](https://app.circleci.com/pipelines/github/triaxtec/flex-config?branch=master)\n[![codecov](https://codecov.io/gh/triaxtec/flex-config/branch/master/graph/badge.svg?token=3utvPfZSLB)](https://codecov.io/gh/triaxtec/flex-config)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![Generic badge](https://img.shields.io/badge/type_checked-mypy-informational.svg)](https://mypy.readthedocs.io/en/stable/introduction.html)\n[![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](https://lbesson.mit-license.org/)\n\n\nConfigure your applications as easily as possible.\n\n## Main Features\n### Load config from wherever\n1. Comes with built in support for loading from dicts, environment variables, YAML files, and AWS SSM Parameter Store.\n2. Super easy to set up a custom source and load from anywhere.\n\n### Path-like lookups for nested values\n```python\nfrom flex_config import FlexConfig\n\nflex_config = FlexConfig()\nflex_config["app/env"] = "local"\nassert flex_config["app"]["env"] == "local"\nassert flex_config["app/env"] == "local"\n```\n\n### Basic type inference\nIf the value FlexConfig gets is a string (like you get from SSM and Env), it will try to parse it to a few other types.\n1. Strings that are digits become ints\n1. Numbers with decimals `.` become floats\n1. Strings contained with `{` and `}` will be parsed as JSON\n1. Failing any of the above you just get your string back\n\n## Installation\nBasic install: `poetry install flex_config`\nWith all optional dependencies: `poetry install flex_config -E all`\n\nFor a full tutorial and API docs, check out the [hosted documentation]\n\n\n[hosted documentation]: https://triaxtec.github.io/flex-config\n',
    'author': 'Dylan Anthony',
    'author_email': 'danthony@triaxtec.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/triaxtec/flex-config',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
