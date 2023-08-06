# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gera2ld',
 'gera2ld.socks',
 'gera2ld.socks.client',
 'gera2ld.socks.server',
 'gera2ld.socks.utils']

package_data = \
{'': ['*']}

install_requires = \
['async_dns>=1.1.3,<2.0.0', 'gera2ld-pyserve>=0.3.0,<0.4.0']

setup_kwargs = {
    'name': 'gera2ld.socks',
    'version': '0.4.4',
    'description': 'SOCKS client and server based on asyncio',
    'long_description': "# gera2ld.socks\n\n[![PyPI](https://img.shields.io/pypi/v/gera2ld.socks.svg)](https://pypi.org/project/gera2ld.socks/)\n\nThis is a SOCKS server and client package built with `asyncio` (requires Python 3.5+).\n\n## Installation\n\n``` sh\n$ pip3 install gera2ld.socks\n```\n\n## Usage\n\n* SOCKS server\n\n  shell command:\n  ``` sh\n  # Start a server\n  $ python3 -m gera2ld.socks.server -b 127.0.0.1:1080\n  ```\n\n  or python script:\n  ``` python\n  from gera2ld.pyserve import run_forever\n  from gera2ld.socks.server import Config, SOCKSServer\n\n  config = Config('127.0.0.1:1080')\n  run_forever(SOCKSServer(config).start_server())\n  ```\n\n* SOCKS client\n\n  ``` python\n  import asyncio\n  from gera2ld.socks.client import create_client\n\n  client = create_client('socks5://127.0.0.1:1080')\n  loop = asyncio.get_event_loop()\n  loop.run_until_complete(client.handle_connect(('www.google.com', 80)))\n  client.writer.write(b'...')\n  print(loop.run_until_complete(client.reader.read()))\n  ```\n\n* SOCKS handler for `urllib`\n\n  ``` python\n  from urllib import request\n  from gera2ld.socks.client.handler import SOCKSProxyHandler\n\n  handler = SOCKSProxyHandler('socks5://127.0.0.1:1080')\n\n  opener = request.build_opener(handler)\n  r = opener.open('https://www.example.com')\n  print(r.read().decode())\n  ```\n\n* SOCKS client for UDP\n\n  ``` python\n  import asyncio\n  from gera2ld.socks.client import create_client\n\n  async def main():\n      client = create_client('socks5://127.0.0.1:1080')\n      udp = await client.handle_udp()\n      udp.write_data(b'\\xc9\\xa7\\x01\\x00\\x00\\x01\\x00\\x00\\x00\\x00\\x00\\x00\\x03www\\x06google\\x03com\\x00\\x00\\xff\\x00\\x01', ('114.114.114.114', 53))\n      print(await udp.results.get())\n\n  loop = asyncio.get_event_loop()\n  loop.run_until_complete(main())\n  ```\n",
    'author': 'Gerald',
    'author_email': 'gera2ld@163.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/gera2ld/pysocks',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
