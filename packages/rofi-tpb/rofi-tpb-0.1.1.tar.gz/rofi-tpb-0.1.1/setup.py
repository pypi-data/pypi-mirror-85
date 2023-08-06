# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rofi_tpb']

package_data = \
{'': ['*']}

install_requires = \
['dynmen>=0.1.5,<0.2.0',
 'lxml>=4.6.1,<5.0.0',
 'tpblite>=0.6,<0.7',
 'traitlets>=5.0.4,<6.0.0']

entry_points = \
{'console_scripts': ['rofi-tpb = rofi_tpb.cli:main']}

setup_kwargs = {
    'name': 'rofi-tpb',
    'version': '0.1.1',
    'description': 'Dynamic menu interface for TPB, built with rofi in mind.',
    'long_description': "# rofi-tpb\n\nDynamic menu interface for The Pirate Bay, built with [`rofi`](https://github.com/davatorium/rofi) in mind.\n\n# Install\n\n```shell\npip install rofi-tpb\n```\n\nConsider using [`pipx`](https://github.com/pipxproject/pipx):\n```shell\npipx install rofi-tpb\n```\n\n# Usage\n\nPrompt to either search tpb or browse tpb's top torrents:\n```shell\nrofi-tpb\n```\n\nPrompt for search query:\n```shell\nrofi-tpb search\n```\n\nSearch for ubuntu related torrents:\n```shell\nrofi-tpb search ubuntu\n```\n\nBrowse tpb's top torrents across all categories:\n```shell\nrofi-tpb top all\n```\n\nBrowse tpb's recent top torrents across all categories in the last 48h:\n```shell\nrofi-tpb top all -r\n```\n\nCheck the help for details:\n```shell\nrofi-tpb --help\n...\nrofi-tpb search --help\n...\nrofi-tpb top --help\n...\n```\n\n# Dependencies\n\n* `python >= 3.7`\n* `tpblite`\n* `dynmen`\n* `lxml`\n* `traitlets` (undeclared dependency of `dynmen`)\n\n\n# Configuration\n\n`rofi-tpb` stores its config in `$XDG_CONFIG_HOME/rofi-tpb/config.ini`.\n\nThe default configuration is the following:\n\n```ini\n[menu]\ncommand = rofi -dmenu -i\ntorrent_format = {title:<70} 📁{filesize:<10} 🔽{seeds:<4} 🔼{leeches:<4}\nuse_tpb_proxy = True\ntpb_url = https://thepiratebay0.org\ncategories = All, APPLICATIONS, AUDIO, GAMES, OTHER, PORN, VIDEO\ncategories_48h = True\n\n[actions]\nadd = xdg-open '{magnetlink}'\nopen = xdg-open '{url}'\n```\n\n * `menu.command`: the dynamic menu command which should read from `stdin` and output to `stdout`, if you want to use `dmenu` instead of `rofi` then adjust this command accordingly.\n * `menu.torrent_format`: text representation of a torrent in the dynamic menu, **accepts torrent string format keys.**\n * `menu.use_tpb_proxy`: if True will use the first tpb url as found on https://piratebayproxy.info/.\n * `menu.tpb_url`: tpb url, if `use_tpb_proxy` is True acts as a fallback url in case https://piratebayproxy.info/ is unavailable or the parsing fails.\n * `menu.categories`: comma separated list of tpb categories, when browsing the top torrents.\n * `menu.categories_48h`: add last 48h top torrent categories.\n * `actions.*`: commands to run on the selected torrent, **accepts torrent string format keys.**\n\nAvailable torrent string format keys:\n * `{title}`: torrent title\n * `{filesize}`: torrent file size\n * `{seeds}`: number of seeders\n * `{leeches}`: number of leechers\n * `{uploader}`: torrent uploader\n * `{upload_date}`: upload date\n * `{url}`: torrent's tpb url\n * `{magnetlink}`: torrent magnet link\n\nIf the `menu.command` uses `rofi`, `rofi-tpb` will use `rofi`'s `-multiple-select` flag to allow for selecting multiple torrents.\n",
    'author': 'Loic Coyle',
    'author_email': 'loic.coyle@hotmail.fr',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/loiccoyle/rofi-tpb',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
