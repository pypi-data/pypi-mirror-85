# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pykg', 'pykg.providers', 'pykg.providers.gcp', 'pykg.providers.gcp.operators']

package_data = \
{'': ['*']}

install_requires = \
['google-cloud-dataproc==2.0.2',
 'google-cloud-storage==1.32.0',
 'loguru==0.5.3']

setup_kwargs = {
    'name': 'pykg',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'Agung Setiaji',
    'author_email': 'mragungsetiaji@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<3.10',
}


setup(**setup_kwargs)
