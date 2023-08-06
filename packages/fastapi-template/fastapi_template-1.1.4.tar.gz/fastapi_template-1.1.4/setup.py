# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['template',
 'template.hooks',
 'template.{{cookiecutter.project_name}}',
 'template.{{cookiecutter.project_name}}.migrations',
 'template.{{cookiecutter.project_name}}.migrations.versions',
 'template.{{cookiecutter.project_name}}.src',
 'template.{{cookiecutter.project_name}}.src.api',
 'template.{{cookiecutter.project_name}}.src.api.dummy_db',
 'template.{{cookiecutter.project_name}}.src.api.httpbin',
 'template.{{cookiecutter.project_name}}.src.api.redis_api',
 'template.{{cookiecutter.project_name}}.src.models',
 'template.{{cookiecutter.project_name}}.src.services',
 'template.{{cookiecutter.project_name}}.src.services.db',
 'template.{{cookiecutter.project_name}}.src.services.elastic',
 'template.{{cookiecutter.project_name}}.src.services.httpbin',
 'template.{{cookiecutter.project_name}}.tests']

package_data = \
{'': ['*'], 'template.{{cookiecutter.project_name}}': ['envs/*', 'systemd/*']}

install_requires = \
['cookiecutter>=1.7.2,<2.0.0',
 'pre-commit>=2.8.2,<3.0.0',
 'pygit2>=1.4.0,<2.0.0',
 'termcolor>=1.1.0,<2.0.0']

entry_points = \
{'console_scripts': ['fastapi_template = main:main']}

setup_kwargs = {
    'name': 'fastapi-template',
    'version': '1.1.4',
    'description': 'Feature-rich robust FastAPI template',
    'long_description': None,
    'author': 'Pavel Kirilin',
    'author_email': 'win10@list.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
