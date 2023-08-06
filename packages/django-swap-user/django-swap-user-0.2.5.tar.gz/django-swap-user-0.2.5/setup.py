# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['swap_user',
 'swap_user.email',
 'swap_user.email.migrations',
 'swap_user.managers',
 'swap_user.named_email',
 'swap_user.named_email.migrations',
 'swap_user.tests']

package_data = \
{'': ['*']}

install_requires = \
['django>=2.2,<2.3']

setup_kwargs = {
    'name': 'django-swap-user',
    'version': '0.2.5',
    'description': '(Beta) Simple and flexible way to swap default Django User',
    'long_description': '# django-swap-user\n\n# архитектура\nприложение swap_user засплитовано на еще 2 приложения:\n  - email\n  - named_email\n  \nпотому что, если оставить их в одном аппе - то они вдвоем создают миграции и таблицы.\nесли их оставить, они будут считаться как 2 кастомные модели в пределах одного приложения, что вызывает\nнедоумение и когнитивную нагрузку.\n\nпри такой архитектуре (когда есть общий апп, который содержит внутренние аппы) - пользователь\nподключает только ту кастомную модель юзера, которая ему больше подходит.',
    'author': 'Artem Innokentiev',
    'author_email': 'artinnok@protonmail.com',
    'maintainer': 'Artem Innokentiev',
    'maintainer_email': 'artinnok@protonmail.com',
    'url': 'http://github.com/artinnok/django-swap-user',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
