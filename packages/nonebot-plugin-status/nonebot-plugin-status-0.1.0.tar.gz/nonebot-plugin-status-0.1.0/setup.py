# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '..'}

packages = \
['nonebot_plugin_status']

package_data = \
{'': ['*'], 'nonebot_plugin_status': ['dist/*']}

install_requires = \
['nonebot2>=2.0.0-alpha.4,<3.0.0', 'psutil>=5.7.2,<6.0.0']

setup_kwargs = {
    'name': 'nonebot-plugin-status',
    'version': '0.1.0',
    'description': 'Check your server status (CPU, Memory, Disk Usage) via nonebot',
    'long_description': None,
    'author': 'yanyongyu',
    'author_email': 'yanyongyu_1@126.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
