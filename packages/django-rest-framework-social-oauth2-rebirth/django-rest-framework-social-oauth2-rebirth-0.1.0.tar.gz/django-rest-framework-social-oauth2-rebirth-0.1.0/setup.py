# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['django_rest_framework_social_oauth2_rebirth',
 'django_rest_framework_social_oauth2_rebirth.commands']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'django-rest-framework-social-oauth2-rebirth',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'ashdaily',
    'author_email': 'ashishsinghbardhan@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
