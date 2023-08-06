# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['lark_shell']
install_requires = \
['lark-parser>=0.8.0,<1.0.0', 'urwid>=2.1.2,<3.0.0']

entry_points = \
{'console_scripts': ['lark_shell = lark_shell:main']}

setup_kwargs = {
    'name': 'lark-shell',
    'version': '0.1.1',
    'description': 'A terminal Lark IDE',
    'long_description': '# Lark-shell\n<!-- TOC depthFrom:1 depthTo:6 withLinks:1 updateOnSave:1 orderedList:0 -->\n\n- [Lark_shell](#larkshell)\n\t- [Background](#background)\n\t- [How to use](#how-to-use)\n\n<!-- /TOC -->\n<p align="center">\n    <a href="https://saythanks.io/to/bryan.hu.2020@gmail.com">\n        <img src="https://img.shields.io/badge/Say%20Thanks-!-1EAEDB.svg" alt="Say Thanks!">\n    </a>\n    <a href="https://github.com/psf/black">\n        <img src="https://img.shields.io/badge/code%20style-black-000000.svg" alt="Code style: black">\n    </a>\n    <a href="https://gitmoji.carloscuesta.me">\n        <img src="https://img.shields.io/badge/gitmoji-%20😜%20😍-FFDD67.svg?style=flat-square" alt="Gitmoji">\n    </a>\n</p>\n\nA terminal version of the [online IDE][1].\n\n## Background\n\nI love using the online IDE for playing with Lark (and experimenting with grammars) but it\'s really minimal\nand it\'s not offline. So I decided to bring those features right into my terminal.\n\n## How to use\n\nInstall it via pip:\n\n```bash\n$ python3 -m pip install lark-shell\n🍰✨\n```\nand invoke the command\n```bash\n$ lark-shell\n```\nand start hacking away!\n\n## Credits\n\nCredits to [**@erezsh**][2] for his wonderful [Lark][3] parsing library.\n\n\n[1]: https://lark-parser.github.io/lark/ide/app.html\n[2]: https://github.com/erezsh\n[3]: https://github.com/lark-parser/lark\n',
    'author': 'Bryan Hu',
    'author_email': 'bryan.hu.2020@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ThatXliner/lark_shell/',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
