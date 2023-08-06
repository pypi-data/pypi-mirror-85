# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['katcr', 'katcr.engines']

package_data = \
{'': ['*']}

install_requires = \
['cleo>=0.7.4,<0.8.0',
 'cutie>=0.2.2,<0.3.0',
 'pygogo>=0.12.0,<0.13.0',
 'requests>=2.22,<3.0',
 'robobrowser>=0.5.3,<0.6.0',
 'telepot>=12.7,<13.0',
 'torrentmirror>=2.0,<3.0',
 'werkzeug==0.16.1']

entry_points = \
{'console_scripts': ['katcr = katcr:main']}

setup_kwargs = {
    'name': 'katcr',
    'version': '2.0.1',
    'description': 'KickassTorrents CLI and Telegram bot',
    'long_description': '.. image:: http://i.imgur.com/ofx75lO.png\n\nEasily **search torrents** in multiple providers such as KickAssTorrents and\nThePirateBay.\n\n\n.. image:: https://travis-ci.org/XayOn/katcr.svg?branch=master\n    :target: https://travis-ci.org/XayOn/katcr\n\n.. image:: https://coveralls.io/repos/github/XayOn/katcr/badge.svg?branch=master\n    :target: https://coveralls.io/github/XayOn/katcr?branch=master\n\n.. image:: https://badge.fury.io/py/katcr.svg\n    :target: https://badge.fury.io/py/katcr\n\n\nCommand Line Interface\n----------------------\n\nkatcr comes with a simple but powerful command line interface\n\n.. image:: /docs/screenshot.gif?raw=True\n\n::\n\n   > poetry run katcr search ...\n\n   USAGE\n     katcr search [--pages\xa0<...>] [--token\xa0[<...>]] [--shortener\xa0[<...>]] [--engines\xa0<...>] [--interactive\xa0[<...>]] [--open\xa0[<...>]] <search>\n\n   ARGUMENTS\n     <search>               Search term\n\n   OPTIONS\n     --pages                Pages to search on search engines (default: "1")\n     --token                Token to use on URL shortener as AUTH\n     --shortener            URL Shortener\n     --engines              Engines (default: "Katcr,ThePirateBay,NyaaSi,Skytorrents")\n     --interactive          Allow the user to choose a specific magnet\n     --open                 Open selected magnet with xdg-open\n\n   GLOBAL OPTIONS\n     -h (--help)            Display this help message\n     -q (--quiet)           Do not output any message\n     -v (--verbose)         Increase the verbosity of messages: "-v" for normal output, "-vv" for more verbose output and "-vvv" for debug\n     -V (--version)         Display this application version\n     --ansi                 Force ANSI output\n     --no-ansi              Disable ANSI output\n     -n (--no-interaction)  Do not ask any interactive question\n\n\nInstallation\n------------\n\nThis is a python package available on pypi, just run::\n\n    sudo python3 -m pip install katcr\n\n\nFeatures\n--------\n\n- Display results in a nice utf-8 table\n- Optional interactive mode, choose and open torrent with a nice text user interface\n- Open torrent directly with your preferred client (via xdg-open)\n- Searches on all available engines until it gets results by default.\n- Search torrents in:\n\n  + Katcr\n  + ThePirateBay\n  + Nyaa\n  + Skytorrents\n  + Digbt\n  + `Jackett <https://github.com/Jackett/Jackett>`_\n\n\nJackett Support\n---------------\n\nYou can easily use a `Jackett <https://github.com/Jackett/Jackett>`_ instance\nto search on all your configured provider.\n\nThis allows you to search on any jackett-supported site (that\'s about supported\n300 trackers).\n\nJackett is probably the best way to use katcr and katbot, as it has a more\nactive mantainance of the tracker sites that us.\n\nTo enable Jackett use, simply export your jackett URL and TOKEN as variables::\n\n   JACKETT_HOST=http://127.0.0.1:9117 JACKETT_APIKEY=<redacted> poetry run katcr --engines=\n\n\n\nKATBot - Kickasstorrents telegram bot\n--------------------------------------\n\nKatcr also comes with a telegram bot entry point.\nIt\'s a simple bot that replies with search results for each message it gets.\n\nIt returns magnet links with provided url shortener for the first page of\nresults, on the first available search engine.\n\n.. image:: http://i.imgur.com/7FxplBs.gif\n\n::\n\n    Run telegram bot.\n\n        Usage: katcr_bot [options]\n\n        Options:\n            --token=<BOT_TOKEN>             Telegram bot token\n            --token-file=<FILE>             Telegram bot token file\n            --shortener=<URL_SHORTENER>     Url shortener to use\n                                            [default: http://shortmag.net]\n\n\nNotes\n------\n\nThis project is made with the best of intentions.\n\nFor that times you need to search for somethink shared as a torrent on KAT\n(I.E, linux images). Logo is based on robot cat by\n`Arsenty <https://thenounproject.com/arsenty/>`_\n\nIf you like this project, show its appreciation by starring it, if you\'re using\nit and want to write to me personally, feel free to do so at\nopensource@davidfrancos.net. If you\'ve got a bug to report, please use the\ngithub ticketing system\nPending things\n--------------\n\n* Fix tests\n* Add information about seeds/leeches on each torrent\n* Add more search engines\n* Maybe direct search to the DHT?\n\n',
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
