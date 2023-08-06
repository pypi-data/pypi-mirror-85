# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['konfik']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.3.1,<6.0.0',
 'Pygments>=2.7.2,<3.0.0',
 'python-dotenv>=0.15.0,<0.16.0',
 'toml>=0.10.2,<0.11.0']

entry_points = \
{'console_scripts': ['konfik = konfik:cli_entrypoint']}

setup_kwargs = {
    'name': 'konfik',
    'version': '2.0.3',
    'description': 'The Strangely Familiar Config Parser',
    'long_description': '<div align="center">\n\n<img src="https://user-images.githubusercontent.com/30027932/95400681-0a8b1f00-092d-11eb-9868-dfa8ff496565.png" alt="konfik-logo">\n\n<strong>>> <i>The Strangely Familiar Config Parser</i> <<</strong>\n<br></br>\n![Codecov](https://img.shields.io/codecov/c/github/rednafi/konfik?color=pink&style=flat-square&logo=appveyor)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square&logo=appveyor)](https://github.com/python/black)\n[![MIT license](https://img.shields.io/badge/License-MIT-blue.svg?style=flat-square&logo=appveyor)](./LICENSE)\n<br></br>\n\n\n**Konfik** is a simple configuration parser that helps you access your config variables using dot (.) notation.\nThis lets you to do this —\n\n```python\nfoo_bar_bazz = config.FOO.BAR.BAZZ\n```\n\n— instead of this —\n\n```python\nfoo_bar_bazz = config["FOO"]["BAR"]["BAZZ"]\n```\n\nKonfik currently supports **TOML**, **YAML**, **DOTENV** and **JSON** configuration formats.\n</div>\n\n## ⚙️ Installation\n\nInstall Konfik via pip:\n\n```\npip install konfik\n```\n\n\n## 💡 Usage\n\nLet\'s see how you can parse a TOML config file and access the configuration variables. For demonstration, we\'ll be using the following `config.toml` file:\n\n```toml\n# Contents of `config.toml`\n\ntitle = "TOML Example"\n\n[owner]\nname = "Tom Preston-Werner"\ndob = 1979-05-27T07:32:00-08:00 # First class dates\n\n[servers]\n  [servers.alpha]\n  ip = "10.0.0.1"\n  dc = "eqdc10"\n\n  [servers.beta]\n  ip = "10.0.0.2"\n  dc = "eqdc10"\n\n[clients]\ndata = [ ["gamma", "delta"], [1, 2] ]\n```\n\nLoad the above config file and access the variables using dot notation:\n\n```python\nfrom pathlib import Path\nfrom konfik import Konfik\n\n# Define the config path\nBASE_DIR = Path(__file__).parent\nCONFIG_PATH_TOML = BASE_DIR / "config.toml"\n\n# Initialize the konfik class\nkonfik = Konfik(config_path=CONFIG_PATH_TOML)\n\n# Print the config file as a Python dict\nkonfik.show_config()\n\n# Get the config dict from the konfik class\nconfig = konfik.config\n\n# Access and print the variables\nprint(config.title)\nprint(config.owner)\nprint(config.owner.dob)\nprint(config.database.ports)\nprint(config.servers.alpha.ip)\nprint(config.clients)\n```\n\nThe `.show_config()` method will print your entire config file as a colorized Python dictionary object like this:\n\n```python\n{\n    \'title\': \'TOML Example\',\n    \'owner\': {\n        \'name\': \'Tom Preston-Werner\',\n        \'dob\': datetime.datetime(1979, 5, 27, 7, 32, tzinfo=<toml.tz.TomlTz object at\n0x7f2dfca308b0>)\n    },\n    \'database\': {\n        \'server\': \'192.168.1.1\',\n        \'ports\': [8001, 8001, 8002],\n        \'connection_max\': 5000,\n        \'enabled\': True\n    },\n    \'servers\': {\n        \'alpha\': {\'ip\': \'10.0.0.1\', \'dc\': \'eqdc10\'},\n        \'beta\': {\'ip\': \'10.0.0.2\', \'dc\': \'eqdc10\'}\n    },\n    \'clients\': {\'data\': [[\'gamma\', \'delta\'], [1, 2]]}\n}\n```\n\nKonfik also exposes a few command-line options for you to introspect your config file and variables. Run:\n\n```\nkonfik --help\n```\n\nThis will reveal the options associated with the CLI tool:\n\n```\nKonfik -- The strangely familiar config parser ⚙️\n\nusage: konfik [-h] [--path PATH] [--show] [--show-literal] [--var VAR] [--version]\n\noptional arguments:\n  -h, --help      show this help message and exit\n  --path PATH     add config file path\n  --show          print config as a dict\n  --show-literal  print config file content literally\n  --var VAR       print config variable\n  --version       print konfik-cli version number\n```\n\nTo inspect the value of a specific variable in a `./config.toml` file you can run:\n\n```\nkonfik --path=config.toml --var=servers.alpha.ip\n```\n\n<div align="center">\n<i> 🍰 </i>\n</div>\n',
    'author': 'rednafi',
    'author_email': 'redowan.nafi@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/rednafi/konfik',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
