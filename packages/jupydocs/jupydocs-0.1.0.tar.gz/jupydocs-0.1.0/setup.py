# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jupydocs']

package_data = \
{'': ['*']}

install_requires = \
['ipython>=7.19.0,<8.0.0', 'pandas>=1.1.4,<2.0.0', 'tabulate>=0.8.7,<0.9.0']

setup_kwargs = {
    'name': 'jupydocs',
    'version': '0.1.0',
    'description': 'Easy Python package documentation using markdown and jupyter',
    'long_description': '# jupydocs\n\nThe easiest way to document your python library with jupyter and markdown.\n\n- [GitHub](https://github.com/SamEdwardes/jupydocs)\n- [docs](https://jupydocs.netlify.app/)\n- [PyPi](https://pypi.org/project/jupydocs/)\n\n```\nPleaes note jupydocs is currently under active development. \nIt can be used for testing, but should not be used for deployment. \nIt will change!\n```\n\n\n## Installation\n\n```bash\npip install jupydocs\n```\n\n\n```python\n\n```\n',
    'author': 'SamEdwardes',
    'author_email': 'edwardes.s@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/SamEdwardes/jupydocs',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
