# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['synth_a_py']

package_data = \
{'': ['*']}

install_requires = \
['returns>=0.14.0,<0.15.0']

extras_require = \
{':python_version >= "3.6" and python_version < "3.7"': ['contextvars>=2.4,<3.0']}

setup_kwargs = {
    'name': 'synth-a-py',
    'version': '1.0.0',
    'description': 'Project configuration as code',
    'long_description': '# synth-a-py\n\n![Build](https://github.com/eganjs/synth-a-py/workflows/ci/badge.svg)\n\nProject configuration as code\n\n# Updating project config\n\nTo do this make edits to the `.projenrc.js` file in the root of the project and run `npx projen` to update existing or generate new config. Please also use `npx prettier --trailing-comma all --write .projenrc.js` to format this file.\n',
    'author': 'Joseph Egan',
    'author_email': 'joseph.s.egan@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/eganjs/synth-a-py',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
