# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ream']

package_data = \
{'': ['*']}

install_requires = \
['lark-parser>=0.11.1,<0.12.0', 'pandas>=1.1.4,<2.0.0']

entry_points = \
{'console_scripts': ['ream = ream.commandline:main']}

setup_kwargs = {
    'name': 'ream',
    'version': '0.1.3.4',
    'description': 'parser/dumper for REAM files',
    'long_description': '# ream-python\n\nA parser/dumper for REAM files written in Pythom.\n\nSee [ream-lang](https://github.com/chmlee/ream-lang#) to learn more about the specs for REAM.\n\n## Installation\n\nream-python is available on [pypi](#) for Python version 3.7 and newer and can be installed with pip:\n\n```shell\npip install ream\n```\n\n### dependence\n\n- [lark-parser](https://github.com/lark-parser/lark): A modern parsing library for Python, implementing Earley & LALR(1). Future versions will drop the dependence.\n\n\n## Licence\n\nThis project is licensed under MIT license.\n\n## Test\n\nupdate\n\n',
    'author': 'Chih-Ming Louis Lee',
    'author_email': 'louis@chihminglee.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/chmlee/ream-python',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
