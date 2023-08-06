# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pykg_spark', 'pykg_spark.hdfs_utilities', 'pykg_spark.pandas_udfs']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.1.4,<2.0.0']

setup_kwargs = {
    'name': 'pykg-spark',
    'version': '0.1.0',
    'description': 'ETL focused utilities library for PySpark',
    'long_description': None,
    'author': 'Agung Setiaji',
    'author_email': 'mragungsetiaji@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.9',
}


setup(**setup_kwargs)
