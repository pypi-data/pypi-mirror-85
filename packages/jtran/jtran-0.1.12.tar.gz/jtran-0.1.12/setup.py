# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jtran']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'jtran',
    'version': '0.1.12',
    'description': 'Japanese kana-latin transliteration tables',
    'long_description': '# Japanese Kana-Latin Transliteration Tables\n[![PyPI](https://img.shields.io/pypi/v/jtran.svg)](https://pypi.python.org/pypi/jtran)\n[![Build Status](https://travis-ci.com/kateabr/jtran.svg?token=2iwzrCfZDArjbexpKxss&branch=master)](https://travis-ci.com/kateabr/jtran)\n\n\n## Install\n\n```\npip install jtran\n```\n',
    'author': 'Ekaterina Biryukova',
    'author_email': 'kateabr@yandex.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/kateabr/jtran',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
