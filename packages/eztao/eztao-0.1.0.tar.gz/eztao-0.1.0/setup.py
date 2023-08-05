# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['eztao', 'eztao.carma', 'eztao.ts', 'eztao.viz']

package_data = \
{'': ['*']}

install_requires = \
['celerite>=0.4.0,<0.5.0',
 'matplotlib>=3.3.1,<4.0.0',
 'numba>=0.51.2,<0.52.0',
 'numpy>=1.19.1,<2.0.0',
 'scipy>=1.5.2,<2.0.0']

setup_kwargs = {
    'name': 'eztao',
    'version': '0.1.0',
    'description': 'A toolkit for Active Galactic Nuclei (AGN) time-series analysis.',
    'long_description': '![tests](https://github.com/ywx649999311/EzTao/workflows/tests/badge.svg)\n# EzTao (易道)\n**EzTao** is a toolkit for conducting AGN time-series/variability analysis, mainly utilizing the continuous-time auto-regressive moving average model (CARMA)\n\n## Installation\n```\npip install eztao\n```\n\n#### Dependencies\n>```\n>python = "^3.7"\n>numpy = "^1.19.1"\n>celerite = "^0.4.0"\n>matplotlib = "^3.3.1"\n>scipy = "^1.5.2"\n>numba = "^0.51.2"\n>```\n\n## Development\n`poetry` is used to solve dependencies and to build/publish this package. Below shows how setup the environment for development (assuming you already have `poetry` installed on your machine). \n\n1. Clone this repository, and enter the repository folder.\n2. Create a python virtual environment and activate it. \n    ```\n    python -m venv env\n    source env/bin/activate\n    ```\n3. Install dependencies and **EzTao** in editable mode.\n   ```\n   poetry install\n   ```\n\nNow you should be ready to start adding new features. Be sure to checkout the normal practice regarding how to use `poetry` on its website. When you are ready to push, also make sure the poetry.lock file is checked-in if any dependency has changed. \n',
    'author': 'Weixiang Yu',
    'author_email': 'wy73@drexel.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ywx649999311/EzTao',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
