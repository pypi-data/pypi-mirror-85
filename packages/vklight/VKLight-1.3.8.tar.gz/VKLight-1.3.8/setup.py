# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['vklight']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.24.0,<3.0.0']

setup_kwargs = {
    'name': 'vklight',
    'version': '1.3.8',
    'description': "VKLight - Light wrapper for VK's API",
    'long_description': '# VKLight\n Легкая обёртка для работы с VK API.\n\n# Установка\n```\npip install vklight\n```\n\n\n# Пример использования\n\n```python\nfrom vklight import VKLight, VKLightError\n\napi = VKLight({\n\t"access_token": "...",\n\t"v": "5.150",\n\t"lang": "ru",\n\t"host": "api.vk.me"\n})\n```\n```python\ntry:\n\tapi.call("users.get", { "user_id": 1})\nexcept VKLightError as e:\n\tprint(e) \n# {\'response\': [{\'id\': 1, \'first_name\': \'Павел\', \'last_name\': \'Дуров\', \'is_closed\': False, \'can_access_closed\': True}]}\n```\nили \n```python\napi("users.get", {"user_id": 1})\n# {\'response\': [{\'id\': 1, \'first_name\': \'Павел\', \'last_name\': \'Дуров\', \'is_closed\': False, \'can_access_closed\': True}]}\n```\n\nИспользование execute-методов\n```python\napi.execute(r"return API.users.get({\'user_id\': 1});")\n# {\'response\': [{\'id\': 1, \'first_name\': \'Павел\', \'last_name\': \'Дуров\', \'is_closed\': False, \'can_access_closed\': True}]}\n```\n\n# Лицензия\nMIT License',
    'author': 'Ivan',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
