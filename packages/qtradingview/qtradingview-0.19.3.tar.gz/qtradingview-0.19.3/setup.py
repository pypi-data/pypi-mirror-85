# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['qtradingview',
 'qtradingview.alarms',
 'qtradingview.base',
 'qtradingview.debug',
 'qtradingview.markets',
 'qtradingview.models',
 'qtradingview.portfolio',
 'qtradingview.ui']

package_data = \
{'': ['*'], 'qtradingview': ['i18n/*']}

install_requires = \
['PyQtWebEngine>=5.15.1,<6.0.0',
 'beautifulsoup4>=4.9.3,<5.0.0',
 'cached-property>=1.5.2,<2.0.0',
 'ccxt>=1.37.52,<2.0.0',
 'coloredlogs>=14.0,<15.0',
 'docopt>=0.6.2,<0.7.0',
 'html5lib>=1.1,<2.0',
 'peewee>=3.14.0,<4.0.0',
 'pyqt5-notificator>=1.0.12,<2.0.0',
 'toml>=0.10.2,<0.11.0']

entry_points = \
{'console_scripts': ['qtradingview = qtradingview.main:run']}

setup_kwargs = {
    'name': 'qtradingview',
    'version': '0.19.3',
    'description': 'PyQt App for TradingView',
    'long_description': '# QTradingView\n\nPyQt App for TradingView.\n\nRecommends simple login to autosave your draws. \n\n\n![Image not found](icons/screenshots/demo.png)  \n\n---\n---\n\n## **Index**\n\n\n- [Features](#Features)\n- [Installation](#Installation)\n- [Usage](#Usage)\n\n---\n---\n***\n\n  \n### **Features**\n\n- Includes the most cryptocurrencies exchanges available in tradingview.\n- Complete lists of available markets, with symbol filter.\n- Favorite and margin lists.\n- Portfolio.\n- Ads remove.\n\n--- \n\n\n### **Installation**\n\nQTradingView needs an environment with Python3 and Qt5\n\n#### ___Prepare environment___\n\n    \n- Install [Anaconda](https://docs.anaconda.com/anaconda/install/)\n\n- Create and active environment.\n    ```\n    conda create -n env_name python=3.7\n    conda activate env_name\n    ```\n\n- Install PyQt5\n    ```\n    conda install -c anaconda pyqt\n    ```\n\n\n#### __QTradingView from source code__\n\n```\n    pip install poetry\n    git clone https://github.com/katmai1/qtradingview\n    cd qtradingview\n\n```\n\n---\n\n### **Usage**\n---\n---\n\n\n#### Install PyQt5 libs using anaconda\n\nCreate and active environment.\n```\nconda create -n env_name python=3.7\nconda activate env_name\n```\n\nInstall PyQt5 and dependencies\n```\nconda install -c anaconda pyqt\n```\n\ninstall\n```\npip install qtradingview\n```\n\n---\n\n## Running from source using Anaconda\n\nCreate and active environment.\n```\nconda create -n env_name python=3.7\nconda activate env_name\n```\n\nInstall PyQt5 and dependencies\n```\nconda install -c anaconda pyqt\npip install -r requirements.txt\n```\n\nRun\n```\npython apprun.py\n```\n\n\n*Can be install without Anaconda if install all PyQt5 dependencies manually.\n\n\n---\n\n\n#### Troubleshot\n\n##### Database issues after an update\n\nProbably the last update does changes into database and this changes are not applied automatically. You can try update tables manually.\n    \n\n```\n- If running from source:\n    python apprun.py --updatedb\n\n- If running compiled release:\n    qtradingview --updatedb\n\n* This function works fine whe running from source code, with a compiled version sometimes not update correctly.\n```\n\nIf issue persist you can delete database to force his create again.\n\n```\n- If running from source:\n    python apprun.py --deletedb\n\n- If running compiled release:\n    qtradingview --deletedb\n```\n\n\n',
    'author': 'katmai',
    'author_email': 'katmai.mobil@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
