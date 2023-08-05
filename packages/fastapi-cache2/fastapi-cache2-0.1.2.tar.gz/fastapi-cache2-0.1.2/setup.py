# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fastapi_cache', 'fastapi_cache.backends']

package_data = \
{'': ['*']}

install_requires = \
['fastapi', 'python-dateutil', 'uvicorn']

extras_require = \
{'all': ['aioredis', 'aiomcache'],
 'memcache': ['aiomcache'],
 'redis': ['aioredis']}

setup_kwargs = {
    'name': 'fastapi-cache2',
    'version': '0.1.2',
    'description': 'Cache for FastAPI',
    'long_description': '# fastapi-cache\n\n![pypi](https://img.shields.io/pypi/v/fastapi-cache2.svg?style=flat)\n![license](https://img.shields.io/github/license/long2ice/fastapi-cache)\n![workflows](https://github.com/long2ice/fastapi-cache/workflows/pypi/badge.svg)\n![workflows](https://github.com/long2ice/fastapi-cache/workflows/ci/badge.svg)\n\n## Introduction\n\n`fastapi-cache` is a tool to cache fastapi response and function result, with backends support `redis` and `memcache`.\n\n## Features\n\n- Support `redis` and `memcache` and `in-memory` backends.\n- Easily integration with `fastapi`.\n- Support http cache like `ETag` and `Cache-Control`.\n\n## Requirements\n\n- `asyncio` environment.\n- `redis` if use `RedisBackend`.\n- `memcache` if use `MemcacheBackend`.\n\n## Install\n\n```shell\n> pip install fastapi-cache2\n```\n\nor\n\n```shell\n> pip install fastapi-cache2[redis]\n```\n\nor\n\n```shell\n> pip install fastapi-cache2[memcache]\n```\n\n## Usage\n\n### Quick Start\n\n```python\nimport aioredis\nfrom fastapi import FastAPI\nfrom starlette.requests import Request\nfrom starlette.responses import Response\n\nfrom fastapi_cache import FastAPICache\nfrom fastapi_cache.backends.redis import RedisBackend\nfrom fastapi_cache.decorator import cache\n\napp = FastAPI()\n\n\n@cache()\nasync def get_cache():\n    return 1\n\n\n@app.get("/")\n@cache(expire=60)\nasync def index(request: Request, response: Response):\n    return dict(hello="world")\n\n\n@app.on_event("startup")\nasync def startup():\n    redis = await aioredis.create_redis_pool("redis://localhost", encoding="utf8")\n    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")\n\n```\n\n### Use `cache` decorator\n\nIf you want cache `fastapi` response transparently, you can use `cache` as decorator between router decorator and view function and must pass `request` as param of view function.\n\nAnd if you want use `ETag` and `Cache-Control` features, you must pass `response` param also.\n\nYou can also use `cache` as decorator like other cache tools to cache common function result.\n\n### Custom coder\n\nBy default use `JsonCoder`, you can write custom coder to encode and decode cache result, just need inherit `fastapi_cache.coder.Coder`.\n\n```python\n@app.get("/")\n@cache(expire=60,coder=JsonCoder)\nasync def index(request: Request, response: Response):\n    return dict(hello="world")\n```\n\n### Custom key builder\n\n```python\ndef my_key_builder(\n    func,\n    namespace: Optional[str] = "",\n    request: Request = None,\n    response: Response = None,\n    *args,\n    **kwargs,\n):\n    prefix = FastAPICache.get_prefix()\n    cache_key = f"{prefix}:{namespace}:{func.__module__}:{func.__name__}:{args}:{kwargs}"\n    return cache_key\n\n@app.get("/")\n@cache(expire=60,coder=JsonCoder,key_builder=my_key_builder)\nasync def index(request: Request, response: Response):\n    return dict(hello="world")\n```\n\n### InMemoryBackend\n\n`InMemoryBackend` only support in single node instead of distributed environment.\n\n## License\n\nThis project is licensed under the [Apache-2.0](https://github.com/long2ice/fastapi-cache/blob/master/LICENSE) License.\n',
    'author': 'long2ice',
    'author_email': 'long2ice@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/long2ice/fastapi-cache',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
