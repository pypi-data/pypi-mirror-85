# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dtk_api']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.7,<4',
 'pydantic>=1.7,<2',
 'requests>=2.24,<3',
 'tbk_api>=0.1.1,<0.2']

setup_kwargs = {
    'name': 'dtk-api',
    'version': '0.6.3',
    'description': '大淘客接口',
    'long_description': '# 大淘客接口\n\n这个项目里面是大淘客的接口信息(当前仅仅生成 Python 的代码)\n\n## 注意:\n\n    这个接口仅仅是为了内部使用，虽然您可以获取它的源代码，但是请不要使用在您的项目中.\n    当前我并不对兼容性以及可用性做任何保证。(如果需要使用请联系开发者获取相应的授权)\n',
    'author': 'dev',
    'author_email': 'dev@qiyutech.tech',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
