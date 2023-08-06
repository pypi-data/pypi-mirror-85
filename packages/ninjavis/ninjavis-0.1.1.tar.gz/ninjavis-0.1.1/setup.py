# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['ninjavis']
install_requires = \
['Jinja2>=2.10,<3.0']

entry_points = \
{'console_scripts': ['ninjavis = ninjavis:main']}

setup_kwargs = {
    'name': 'ninjavis',
    'version': '0.1.1',
    'description': 'Generate visualization from Ninja build logs.',
    'long_description': '# ninjavis #\n[![Build Status](https://travis-ci.org/chagui/ninjavis.png)](https://travis-ci.org/chagui/ninjavis)\n[![PyPI version](https://badge.fury.io/py/ninjavis.svg)](https://badge.fury.io/py/ninjavis)\n\n## Introduction ##\nGenerate visualization from [Ninja](https://github.com/ninja-build/ninja) build logs. Ninjavis parse the ninja build\nlogs and for each item of the build extract its target, starting and end time.\nIt output those information in a template containing a simple timeline ; the visualization is done by [vis.js](http://visjs.org/).\n\nInspired by [buildbloat](https://github.com/nico/buildbloat).\n\n## Usage ##\n```bash\nusage: ninjavis --title "my build" ninja_build.log build_profile.html\n```\n:warning: Run ``ninja -t recompact`` first ot make sure that no duplicate entries are in the build log.\n\n## Example ##\nProfile of Ninja 1.8.2 build\n![Ninja 1.8.2 build profile](docs/example-ninja_build_1.8.2.png)\n',
    'author': 'Guilhem Charles',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/chagui/ninjavis',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
