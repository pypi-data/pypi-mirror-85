# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['shared_memory_dict', 'shared_memory_dict.caches']

package_data = \
{'': ['*']}

extras_require = \
{'aiocache': ['aiocache>=0.11.1,<0.12.0'],
 'all': ['django>=3.0.8,<4.0.0', 'aiocache>=0.11.1,<0.12.0'],
 'django': ['django>=3.0.8,<4.0.0']}

setup_kwargs = {
    'name': 'shared-memory-dict',
    'version': '0.4.0',
    'description': 'A very simple shared memory dict implementation',
    'long_description': '# Shared Memory Dict\nA very simple [shared memory](https://docs.python.org/3/library/multiprocessing.shared_memory.html) dict implementation.\n\n**Requires**: Python >= 3.8\n\n```python\n>> from shared_memory_dict import SharedMemoryDict\n>> smd = SharedMemoryDict(name=\'tokens\', size=1024)\n>> smd[\'some-key\'] = \'some-value-with-any-type\'\n>> smd[\'some-key\']\n\'some-value-with-any-type\'\n```\n\n> The arg `name` defines the location of the memory block, so if you want to share the memory between process use the same name\n\n## Installation\nUsing `pip`:\n```shell\npip install shared-memory-dict\n```\n\n## Locks\nTo use [multiprocessing.Lock](https://docs.python.org/3.8/library/multiprocessing.html#multiprocessing.Lock) on write operations of shared memory dict set environment variable `SHARED_MEMORY_USE_LOCK=1`.\n\n## Django Cache Implementation\nThere\'s a [Django Cache Implementation](https://docs.djangoproject.com/en/3.0/topics/cache/) with Shared Memory Dict:\n\n```python\n# settings/base.py\nCACHES = {\n    \'default\': {\n        \'BACKEND\': \'shared_memory_dict.caches.django.SharedMemoryCache\',\n        \'LOCATION\': \'memory\',\n        \'OPTIONS\': {\'MEMORY_BLOCK_SIZE\': 1024}\n    }\n}\n```\n\n**Install with**: `pip install "shared-memory-dict[django]"`\n\n### Caveat\nWith Django cache implementation the keys only expire when they\'re read. Be careful with memory usage\n\n\n## AioCache Backend\nThere\'s also a [AioCache Backend Implementation](https://aiocache.readthedocs.io/en/latest/caches.html) with Shared Memory Dict:\n\n```python\nFrom aiocache import caches\n\ncaches.set_config({\n    \'default\': {\n        \'cache\': \'shared_memory_dict.caches.aiocache.SharedMemoryCache\',\n        \'size\': 1024,\n    },\n})\n```\n\n> This implementation is very based on aiocache [SimpleMemoryCache](https://aiocache.readthedocs.io/en/latest/caches.html#simplememorycache)\n\n**Install with**: `pip install "shared-memory-dict[aiocache]"`\n',
    'author': 'Arquitetura LuizaLabs',
    'author_email': 'arquitetura@luizalabs.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/luizalabs/shared-memory-dict',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
