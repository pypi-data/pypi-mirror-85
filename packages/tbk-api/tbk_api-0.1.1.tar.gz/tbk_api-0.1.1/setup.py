# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tbk_api']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.7,<2']

setup_kwargs = {
    'name': 'tbk-api',
    'version': '0.1.1',
    'description': '淘宝客接口',
    'long_description': '# 淘宝客接口\n\n淘宝客共享接口\n\n## 注意:\n\n    这个接口仅仅是为了内部使用，虽然您可以获取它的源代码，但是请不要使用在您的项目中.\n    当前我并不对兼容性以及可用性做任何保证。(如果需要使用请联系开发者获取相应的授权)\n',
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
