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
    'version': '0.1.1',
    'description': 'Check your server status (CPU, Memory, Disk Usage) via nonebot',
    'long_description': '<!--\n * @Author         : yanyongyu\n * @Date           : 2020-11-15 14:40:25\n * @LastEditors    : yanyongyu\n * @LastEditTime   : 2020-11-15 14:52:23\n * @Description    : None\n * @GitHub         : https://github.com/yanyongyu\n-->\n\n<p align="center">\n  <a href="https://v2.nonebot.dev/"><img src="https://raw.githubusercontent.com/nonebot/nonebot2/master/docs/.vuepress/public/logo.png" width="200" height="200" alt="nonebot"></a>\n</p>\n\n<div align="center">\n\n# nonebot-plugin-status\n\n_✨ NoneBot 服务器状态（CPU, Memory, Disk Usage）查看插件 ✨_\n\n</div>\n\n<p align="center">\n  <a href="https://raw.githubusercontent.com/cscs181/QQ-Github-Bot/master/LICENSE">\n    <img src="https://img.shields.io/github/license/cscs181/QQ-Github-Bot.svg" alt="license">\n  </a>\n  <a href="https://pypi.python.org/pypi/nonebot-plugin-status">\n    <img src="https://img.shields.io/pypi/v/nonebot-plugin-status.svg" alt="pypi">\n  </a>\n  <img src="https://img.shields.io/badge/python-3.7+-blue.svg" alt="python">\n</p>\n\n## 使用方式\n\n- 发送 Command `状态`\n- 向机器人发送戳一戳表情\n- 双击机器人头像戳一戳\n',
    'author': 'yanyongyu',
    'author_email': 'yanyongyu_1@126.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/cscs181/QQ-GitHub-Bot/tree/master/src/plugins/nonebot_plugin_status',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
