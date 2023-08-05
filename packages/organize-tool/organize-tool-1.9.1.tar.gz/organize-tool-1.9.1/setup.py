# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['organize', 'organize.actions', 'organize.filters']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.1,<6.0',
 'Send2Trash>=1.5,<2.0',
 'appdirs>=1.4,<2.0',
 'colorama>=0.4.1,<0.5.0',
 'docopt>=0.6.2,<0.7.0',
 'exifread>=2.1,<3.0',
 'pendulum>=2.0.5,<3.0.0',
 'textract>=1.6.3,<2.0.0']

extras_require = \
{':python_version < "3.4"': ['pathlib2==2.3.0'],
 ':python_version < "3.5"': ['typing>=3.6,<4.0', 'pathlib2>=2.3.3,<3.0.0']}

entry_points = \
{'console_scripts': ['organize = organize.cli:main']}

setup_kwargs = {
    'name': 'organize-tool',
    'version': '1.9.1',
    'description': 'The file management automation tool',
    'long_description': '<p align="center">\n <img width="623" height="168" src="https://github.com/tfeldmann/organize/raw/master/docs/images/organize.svg?sanitize=true" alt="organize logo">\n</p>\n\n<div align="center">\n\n  [![GitHub Issues](https://travis-ci.org/tfeldmann/organize.svg?branch=master)](https://travis-ci.org/tfeldmann/organize)\n  [![Documentation Status](https://readthedocs.org/projects/organize/badge/?version=latest)](https://organize.readthedocs.io/en/latest/?badge=latest)\n  [![License](https://img.shields.io/badge/license-MIT-blue.svg)](/LICENSE)\n</div>\n\n---\n\n<p align="center"> <b>organize</b> - The file management automation tool\n<br>\n<a href="https://organize.readthedocs.io/" target="_blank">Full documentation at Read the docs</a>\n</p>\n\n- [About](#about)\n- [Getting started](#getting-started)\n  - [Installation](#installation)\n  - [Creating your first rule](#creating-your-first-rule)\n- [Example rules](#example-rules)\n- [Advanced usage](#advanced-usage)\n- [Command line interface](#command-line-interface)\n\n## About\nYour desktop is a mess? You cannot find anything in your downloads and\ndocuments? Sorting and renaming all these files by hand is too tedious?\nTime to automate it once and benefit from it forever.\n\n**organize** is a command line, open-source alternative to apps like Hazel (macOS)\nor File Juggler (Windows).\n\n\n## Getting started\n### Installation\nPython 3.5+ is needed. Install it via your package manager or from [python.org](https://python.org).\n\nInstallation is done via pip. Note that the package name is `organize-tool`:\n```bash\npip3 install -U organize-tool\n``` \nThis command can also be used to update to the newest version. Now you can run `organize --help` to check if the installation was successful.\n\n### Creating your first rule\nIn your shell, **run ``organize config``** to edit the configuration:\n\n```yaml\nrules:\n  - folders: ~/Downloads\n    subfolders: true\n    filters:\n      - extension: pdf\n    actions:\n      - echo: "Found PDF!"\n```\n\n> If you have problems editing the configuration you can run ``organize config --open-folder`` to reveal the configuration folder in your file manager. You can then edit the `config.yaml` in your favourite editor.\n> \n> Alternatively you can run ``organize config --path`` to see the full path to\nyour ``config.yaml``)\n\n\n**Save your config file and run `organize run`.**\n\nYou will see a list of all `.pdf` files you have in your downloads folder (+ subfolders). For now we only show the text `Found PDF!` for each file, but this will change soon...\n(If it shows ``Nothing to do`` you simply don\'t have any pdfs in your downloads folder).\n\nRun ``organize config`` again and add a `copy`-action to your rule:\n```yaml\n    actions:\n      - echo: "Found PDF!"\n      - move: ~/Documents/PDFs/\n```\n\n**Now run `organize sim` to see what would happen without touching your files**. You will see that your pdf-files would be moved over to your `Documents/PDFs` folder.\n\nCongratulations, you just automated your first task. You can now run `organize run` whenever you like and all your pdfs are a bit more organized. It\'s that easy.\n\n> There is so much more. You want to rename / copy files, run custom shell- or python scripts, match filenames with regular expressions or use placeholder variables? organize has you covered. Have a look at the advanced usage example below!\n\n\n## Example rules\nHere are some examples of simple organization and cleanup rules. Modify to your needs!\n\nMove all invoices, orders or purchase documents into your documents folder:\n```yaml\nrules:\n  # sort my invoices and receipts\n  - folders: ~/Downloads\n    subfolders: true\n    filters:\n      - extension: pdf\n      - filename:\n          contains:\n            - Invoice\n            - Order\n            - Purchase\n          case_sensitive: false\n    actions:\n      - move: ~/Documents/Shopping/\n```\n\nMove incomplete downloads older than 30 days into the trash:\n```yaml\nrules:\n  # move incomplete downloads older > 30 days into the trash\n  - folders: ~/Downloads\n    filters:\n      - extension:\n          - download\n          - crdownload\n          - part\n      - lastmodified:\n          days: 30\n          mode: older\n    actions:\n      - trash\n```\n\nDelete empty files from downloads and desktop:\n```yaml\nrules:\n  # delete empty files from downloads and desktop\n  - folders: \n      - ~/Downloads\n      - ~/Desktop\n    filters:\n      - filesize: 0\n    actions:\n      - trash\n```\n\nMove screenshots into a "Screenshots" folder on your desktop:\n```yaml\nrules:\n  # move screenshots into "Screenshots" folder\n  - folders: ~/Desktop\n    filters:\n      - filename:\n          startswith: \'Screen Shot\'\n    actions:\n      - move: ~/Desktop/Screenshots/\n```\n\nOrganize your font downloads:\n```yaml\nrules:\n  # organize your font files but keep the folder structure:\n  #   "~/Downloads/favourites/helvetica/helvetica-bold.ttf"\n  #     is moved to\n  #   "~/Documents/FONTS/favourites/helvetica/helvetica-bold.ttf"\n  - folders: ~/Downloads/**/*.ttf\n    actions:\n      - Move: \'~/Documents/FONTS/{relative_path}\'\n```\n\nYou\'ll find many more examples in the <a href="https://organize.readthedocs.io/" target="_blank">full documentation</a>.\n\n\n## Advanced usage\nThis example shows some advanced features like placeholder variables, pluggable\nactions, recursion through subfolders and glob syntax:\n\n```yaml\nrules:\n  - folders: ~/Documents/**/*\n    filters:\n      - extension:\n          - pdf\n          - docx\n      - created\n    actions:\n      - move: \'~/Documents/{extension.upper}/{created.year}{created.month:02}/\'\n      - shell: \'open "{path}"\'\n```\n\nGiven we have two files in our ``~/Documents`` folder (or any of its subfolders)\nnamed ``script.docx`` from january 2018 and ``demo.pdf`` from december 2016 this will\nhappen:\n\n- ``script.docx`` will be moved to ``~/Documents/DOCX/2018-01/script.docx``\n- ``demo.pdf`` will be moved to ``~/Documents/PDF/2016-12/demo.pdf``\n- The files will be opened (``open`` command in macOS) *from their new location*.\n- Note the format syntax for `{created.month}` to make sure the month is prepended with a zero.\n\n\n## Command line interface\n```\nThe file management automation tool.\n\nUsage:\n    organize sim [--config-file=<path>]\n    organize run [--config-file=<path>]\n    organize config [--open-folder | --path | --debug] [--config-file=<path>]\n    organize list\n    organize --help\n    organize --version\n\nArguments:\n    sim             Simulate a run. Does not touch your files.\n    run             Organizes your files according to your rules.\n    config          Open the configuration file in $EDITOR.\n    list            List available filters and actions.\n    --version       Show program version and exit.\n    -h, --help      Show this screen and exit.\n\nOptions:\n    -o, --open-folder  Open the folder containing the configuration files.\n    -p, --path         Show the path to the configuration file.\n    -d, --debug        Debug your configuration file.\n\nFull documentation: https://organize.readthedocs.io\n```\n',
    'author': 'Thomas Feldmann',
    'author_email': 'mail@tfeldmann.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/tfeldmann/organize',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
