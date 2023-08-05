# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pluploader',
 'pluploader.confluence',
 'pluploader.confluence.jobs',
 'pluploader.mpac',
 'pluploader.upm',
 'pluploader.util']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.3.1,<6.0.0',
 'beautifulsoup4>=4.9.3,<5.0.0',
 'click_default_group>=1.2.2,<2.0.0',
 'colorama>=0.4.3,<0.5.0',
 'coloredlogs>=14.0,<15.0',
 'configargparse>=1.2.3,<2.0.0',
 'debugpy>=1.1.0,<2.0.0',
 'furl>=2.1.0,<3.0.0',
 'html5lib>=1.1,<2.0',
 'importlib-metadata>=1.7.0,<2.0.0',
 'lxml>=4.5.2,<5.0.0',
 'packaging>=20.4,<21.0',
 'pydantic>=1.6.1,<2.0.0',
 'requests>=2.24.0,<3.0.0',
 'tqdm>=4.48.2,<5.0.0',
 'typer>=0.3.2,<0.4.0']

extras_require = \
{':python_version < "3.7"': ['dataclasses']}

entry_points = \
{'console_scripts': ['pluploader = pluploader.main:main']}

setup_kwargs = {
    'name': 'pluploader',
    'version': '0.6.0',
    'description': 'CLI Confluence/Jira Plugin uploader',
    'long_description': None,
    'author': 'Fabian Siegel',
    'author_email': 'fabian@livelyapps.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
