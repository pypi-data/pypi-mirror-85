# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['seaborn_image']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib-scalebar>=0.6.2,<0.7.0',
 'matplotlib>=3.2.2,<4.0.0',
 'palettable>=3.3.0,<4.0.0',
 'pooch>=1.2.0,<2.0.0',
 'scikit-image>=0.17.2,<0.18.0',
 'scipy>=1.5.1,<2.0.0']

extras_require = \
{':python_version < "3.8"': ['importlib_metadata>=1.7.0,<2.0.0']}

setup_kwargs = {
    'name': 'seaborn-image',
    'version': '0.4.0',
    'description': 'seaborn-image: image data visualization and processing like seaborrn using matplotlib, scipy and scikit-image',
    'long_description': '# seaborn-image: image data visualization\n\n[![Tests](https://github.com/SarthakJariwala/seaborn-image/workflows/Tests/badge.svg)](https://github.com/SarthakJariwala/seaborn-image/actions?workflow=Tests)\n[![Codecov](https://codecov.io/gh/SarthakJariwala/seaborn-image/branch/master/graph/badge.svg)](https://codecov.io/gh/SarthakJariwala/seaborn-image)\n[![PyPI](https://img.shields.io/pypi/v/seaborn-image.svg)](https://pypi.org/project/seaborn-image/)\n[![Documentation Status](https://readthedocs.org/projects/seaborn-image/badge/?version=latest)](https://seaborn-image.readthedocs.io/en/latest/?badge=latest)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\n\n<div class="row">\n\n  <a href="https://seaborn-image.readthedocs.io/en/latest/auto_examples/plot_image_hist.html">\n  <img src="./images/sphx_glr_plot_image_hist_001.png" height="120" width="170">\n  </a>\n\n  <a href="https://seaborn-image.readthedocs.io/en/latest/auto_examples/plot_filter.html">\n  <img src="./images/sphx_glr_plot_filter_001.png" height="120" width="130">\n  </a>\n\n  <a href="https://seaborn-image.readthedocs.io/en/latest/auto_examples/plot_fft.html">\n  <img src="./images/sphx_glr_plot_fft_001.png" height="120" width="120">\n  </a>\n\n  <a href="https://seaborn-image.readthedocs.io/en/latest/auto_examples/plot_filtergrid.html">\n  <img src="./images/sphx_glr_plot_filtergrid_001.png" height="120" width="120">\n  </a>\n\n  <a href="https://seaborn-image.readthedocs.io/en/latest/auto_examples/plot_image_robust.html">\n  <img src="./images/sphx_glr_plot_image_robust_001.png" height="120" width="260">\n  </a>\n\n</div>\n\n\n## Description\n\nSeaborn-image is a Python **image** visualization library based on matplotlib\nand provides a high-level API to **draw attractive and informative images quickly and effectively**.\n\nIt is heavily inspired by [seaborn](https://seaborn.pydata.org/), a high-level visualization library\nfor drawing attractive statistical graphics in Python.\n\n## Installation\n\nFor latest release\n```bash\npip install seaborn-image\n```\n\nFor latest commit\n```bash\npip install git+https://github.com/SarthakJariwala/seaborn-image\n```\n\n## Documentation\n\nRefer to the documentation [here](https://seaborn-image.readthedocs.io/).\n\n## Usage\n\nCheck out the [tutorial](https://seaborn-image.readthedocs.io/en/latest/tutorial.html) and [examples](https://seaborn-image.readthedocs.io/auto_examples/index.html).\n',
    'author': 'Sarthak Jariwala',
    'author_email': 'jariwala@uw.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/SarthakJariwala/seaborn-image',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
