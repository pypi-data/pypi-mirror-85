# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['synth_a_py']

package_data = \
{'': ['*']}

install_requires = \
['returns>=0.14.0,<0.15.0', 'toml>=0.10.1,<0.11.0']

extras_require = \
{':python_version >= "3.6" and python_version < "3.7"': ['contextvars>=2.4,<3.0']}

setup_kwargs = {
    'name': 'synth-a-py',
    'version': '1.3.1',
    'description': 'Project configuration as code',
    'long_description': '# synth-a-py\n\n![Build](https://github.com/eganjs/synth-a-py/workflows/ci/badge.svg)\n\nProject configuration as code\n\n## Example usage\n\n```python\n#!/usr/bin/env python\nfrom textwrap import dedent\n\nfrom synth_a_py import Dir, Project, SimpleFile, TomlFile\n\nproject_name = "sample-project"\nproject_version = "0.1.0"\nproject_import = project_name.lower().replace("-", "_")\n\nspec = Project()\nwith spec:\n    with Dir(".github"):\n        with Dir("workflows"):\n            SimpleFile(\n                "ci.yml",\n                dedent(\n                    """\\\n                    ...\n                    """\n                ),\n            )\n            SimpleFile(\n                "publish.yml",\n                dedent(\n                    """\\\n                    ...\n                    """\n                ),\n            )\n\n    TomlFile(\n        "pyproject.toml",\n        {\n            "build-system": {\n                "requires": ["poetry>=0.12"],\n                "build-backend": "poetry.masonry.api",\n            },\n            "tool": {\n                "poetry": {\n                    "name": project_name,\n                    "version": project_version,\n                    "description": "A sample project generated using synth-a-py",\n                    "authors": ["Joseph Egan"],\n                    "dependencies": {\n                        "python": "^3.6",\n                    },\n                    "dev-dependencies": {\n                        "pytest": "^6",\n                        "pyprojroot": "^0.2.0",\n                    },\n                },\n            },\n        },\n    )\n\n    SimpleFile(\n        "Makefile",\n        dedent(\n            """\\\n            .PHONEY: test\n            test:\n            \\tpoetry install\n            \\tpoetry run pytest\n            """\n        ),\n    )\n\n    with Dir(project_import):\n        SimpleFile(\n            "__init__.py",\n            dedent(\n                f"""\\\n                __version__ = "{project_version}"\n                """\n            ),\n        )\n\n    with Dir("tests"):\n        SimpleFile(\n            "test_version.py",\n            dedent(\n                f"""\\\n\t\timport toml\n\t\tfrom pyprojroot import here\n\n\t\tfrom {project_import} import __version__\n\n\n\t\tdef test_version() -> None:\n\t\t    pyproject = toml.load(here("pyproject.toml"))\n\t\t    pyproject_version = pyproject["tool"]["poetry"]["version"]\n\n\t\t    assert __version__ == pyproject_version\n                """\n            ),\n        )\n\nspec.synth()\n```\n\n## Goals\n\n- [ ] Use synth-a-py to manage project configs\n  - Add support for:\n    - [x] LICENSE\n    - [x] TOML (for pyproject.toml)\n    - [ ] YAML (for GitHub Actions config)\n      - [ ] GitHub Action workflow?\n    - [ ] INI (for flake8/mypy config)\n    - [ ] Makefile\n    - [ ] .gitignore\n  - Add ./synth.py\n- Templates:\n  - [ ] Poetry\n  - [ ] setup.py\n  - [ ] Pipenv\n- In-repo examples:\n  - [ ] Minimal\n  - [ ] Monorepo\n\n## Updating project config\n\nTo do this make edits to the `.projenrc.js` file in the root of the project and run `npx projen` to update existing or generate new config. Please also use `npx prettier --trailing-comma all --write .projenrc.js` to format this file.\n',
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
