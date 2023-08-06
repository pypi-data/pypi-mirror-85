# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['graia',
 'graia.application',
 'graia.application.event',
 'graia.application.interrupt',
 'graia.application.message',
 'graia.application.message.elements',
 'graia.application.message.parser',
 'graia.scheduler']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.6.2,<4.0.0',
 'croniter>=0.3.34,<0.4.0',
 'graia-broadcast>=0.4.0',
 'pydantic>=1.6.1,<2.0.0',
 'regex>=2020.7.14,<2021.0.0',
 'yarl>=1.4.2,<2.0.0']

extras_require = \
{':python_version < "3.7"': ['contextvars>=2.4,<3.0']}

setup_kwargs = {
    'name': 'graia-application-mirai',
    'version': '0.10.14',
    'description': '',
    'long_description': None,
    'author': 'GreyElaina',
    'author_email': 'GreyElaina@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
