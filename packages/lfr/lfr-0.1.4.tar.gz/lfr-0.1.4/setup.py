# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lfr',
 'lfr.antlrgen',
 'lfr.compiler',
 'lfr.compiler.constraints',
 'lfr.compiler.distribute',
 'lfr.compiler.language',
 'lfr.fig',
 'lfr.netlistgenerator',
 'lfr.netlistgenerator.v2',
 'lfr.netlistgenerator.v2.gen_strategies']

package_data = \
{'': ['*']}

install_requires = \
['antlr4-python3-runtime>=4.8,<5.0',
 'argparse>=1.4.0,<2.0.0',
 'networkx>=2.5,<3.0',
 'pygraphviz>=1.6,<2.0',
 'pymint>=0.1.3,<0.2.0']

entry_points = \
{'console_scripts': ['lfr-compile = lfr.cmdline:main']}

setup_kwargs = {
    'name': 'lfr',
    'version': '0.1.4',
    'description': '',
    'long_description': None,
    'author': 'Radhakrishna Sanka',
    'author_email': 'rkrishnasanka@gmail.com',
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
