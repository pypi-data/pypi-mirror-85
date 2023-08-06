# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['katcr', 'katcr.engines']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.7.2,<4.0.0',
 'cleo',
 'cutie>=0.2.2,<0.3.0',
 'feedparser>=6.0.2,<7.0.0',
 'telepot>=12.7,<13.0',
 'torrentmirror>=2.0,<3.0',
 'torrentstream>=0.2.1,<0.3.0']

entry_points = \
{'console_scripts': ['katcr = katcr:main']}

setup_kwargs = {
    'name': 'katcr',
    'version': '3.0.0',
    'description': 'KickassTorrents CLI and Telegram bot',
    'long_description': '.. image:: http://i.imgur.com/ofx75lO.png\n\nCLI client to torrent searches and streaming. Easily **search torrents** in\nmultiple providers such as KickAssTorrents and ThePirateBay.\n\n|pypi| |release| |downloads| |python_versions| |pypi_versions| |actions|\n\n.. |pypi| image:: https://img.shields.io/pypi/l/katcr\n.. |release| image:: https://img.shields.io/librariesio/release/pypi/katcr\n.. |downloads| image:: https://img.shields.io/pypi/dm/katcr\n.. |python_versions| image:: https://img.shields.io/pypi/pyversions/katcr\n.. |pypi_versions| image:: https://img.shields.io/pypi/v/katcr\n.. |actions| image:: https://travis-ci.org/XayOn/katcr.svg?branch=master\n    :target: https://travis-ci.org/XayOn/katcr\n\n\nCommand Line Interface\n----------------------\n\nkatcr comes with a simple but powerful command line interface\n\n.. image:: /docs/screenshot.gif?raw=True\n\n::\n\n   > poetry run katcr search ...\n\n   USAGE\n     katcr search [--pages\xa0<...>] [--token\xa0[<...>]] [--shortener\xa0[<...>]] [--engines\xa0<...>] [--interactive\xa0[<...>]] [--open\xa0[<...>]] <search>\n\n   ARGUMENTS\n     <search>               Search term\n\n   OPTIONS\n     --pages                Pages to search on search engines (default: "1")\n     --token                Token to use on URL shortener as AUTH\n     --shortener            URL Shortener\n     --engines              Engines (default: "Katcr,ThePirateBay,NyaaSi,Skytorrents")\n     --interactive          Allow the user to choose a specific magnet\n     --open                 Open selected magnet with xdg-open\n\n   GLOBAL OPTIONS\n     -h (--help)            Display this help message\n     -q (--quiet)           Do not output any message\n     -v (--verbose)         Increase the verbosity of messages: "-v" for normal output, "-vv" for more verbose output and "-vvv" for debug\n     -V (--version)         Display this application version\n     --ansi                 Force ANSI output\n     --no-ansi              Disable ANSI output\n     -n (--no-interaction)  Do not ask any interactive question\n\n\nInstallation\n------------\n\nThis is a python package available on pypi, just run::\n\n    sudo python3 -m pip install katcr\n\n\nFeatures\n--------\n\n- Display results in a nice utf-8 table\n- Optional interactive mode, choose and open torrent with a nice text user interface\n- Open torrent directly with your preferred client (via xdg-open)\n- Stream torrent with `torrentstream <https://github.com/XayOn/torrentstream>`_\n- Searches on all available engines until it gets results by default.\n- Search torrents in:\n\n  + Eztv\n  + `Jackett <https://github.com/Jackett/Jackett>`_\n  + Katcr\n  + NyaaSi\n  + Skytorrents\n  + ThePirateBay\n\n\nJackett Support\n---------------\n\nYou can easily use a `Jackett <https://github.com/Jackett/Jackett>`_ instance\nto search on all your configured provider.\n\nThis allows you to search on any jackett-supported site (that\'s about supported\n300 trackers).\n\nJackett is probably the best way to use katcr and katbot, as it has a more\nactive mantainance of the tracker sites that us.\n\nTo enable Jackett use, simply export your jackett URL and TOKEN as variables::\n\n   JACKETT_HOST=http://127.0.0.1:9117 JACKETT_APIKEY=<redacted> poetry run katcr --engines=\n\n\nNotes\n------\n\nThis project is made with the best of intentions.\n\nFor that times you need to search for somethink shared as a torrent on KAT\n(I.E, linux images). Logo is based on robot cat by\n`Arsenty <https://thenounproject.com/arsenty/>`_\n\nIf you like this project, show its appreciation by starring it, if you\'re using\nit and want to write to me personally, feel free to do so at\nopensource@davidfrancos.net. If you\'ve got a bug to report, please use the\ngithub ticketing system\n',
    'author': 'David Francos',
    'author_email': 'opensource@davidfrancos.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
