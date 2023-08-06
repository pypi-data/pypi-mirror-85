# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sphinx_scylladb_theme', 'sphinx_scylladb_theme.extensions']

package_data = \
{'': ['*'],
 'sphinx_scylladb_theme': ['static/*',
                           'static/css/*',
                           'static/css/doc/*',
                           'static/css/doc/ext/*',
                           'static/fonts/*',
                           'static/img/*',
                           'static/js/*',
                           'static/js/foundation/*',
                           'static/js/vendor/*']}

install_requires = \
['Sphinx>=2.4.4,<3.0.0',
 'pyyaml>=5.3,<6.0',
 'recommonmark==0.5.0',
 'sphinx-copybutton>=0.2.8,<0.3.0',
 'sphinx-multiversion-scylla>=0.2.4,<0.3.0',
 'sphinx-notfound-page>=0.5,<0.6',
 'sphinx-tabs>=1.1.13,<2.0.0']

setup_kwargs = {
    'name': 'sphinx-scylladb-theme',
    'version': '0.1.15',
    'description': 'A Sphinx Theme for ScyllaDB projects documentation',
    'long_description': '==========================\nScylla Documentation Theme\n==========================\n\nThe base Sphinx theme for ScyllaDB documentation projects.\n\n`Read More. <https://github.com/scylladb/sphinx-scylladb-theme#scylla-documentation-theme>`_\n',
    'author': 'David García',
    'author_email': 'dgarcia360@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
