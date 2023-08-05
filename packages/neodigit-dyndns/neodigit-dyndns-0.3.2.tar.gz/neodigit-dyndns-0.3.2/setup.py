# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['neodigit_dyndns']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.3.1,<6.0.0', 'requests>=2.24.0,<3.0.0']

setup_kwargs = {
    'name': 'neodigit-dyndns',
    'version': '0.3.2',
    'description': "A dynamic DNS client using Neodigit's API",
    'long_description': "# Dynamic Dns with Neodigit's API\n\n![GitHub](https://img.shields.io/github/license/educollado/neodigit-dyndns)\n![GitHub last commit](https://img.shields.io/github/last-commit/educollado/neodigit-dyndns)\n![GitHub repo size](https://img.shields.io/github/repo-size/educollado/neodigit-dyndns)\n![Twitter Follow](https://img.shields.io/twitter/follow/ecollado)\n![Mastodon Follow](https://img.shields.io/mastodon/follow/72314?domain=https%3A%2F%2Fmastodon.social&style=social)\n\n## TESTING PURPOSES ONLY\n\n## Links\n\n* Github: https://github.com/educollado/neodigit-dyndns\n* Pypi.org: https://pypi.org/project/neodigit-dyndns/\n\ndynamic_dns for Neodigit domains\n\nhttps://panel.neodigit.net\n\n## Configuration: \n\nYou need to configure the config.cfg and pass it the file as attribute \n\n* token: \n* my_domain: \n* my_subdomain: \n\nYou can obtain your own token Id from: https://panel.neodigit.net/api-consumers \n\nie: our token is 1234, and our subdomain is test.mydomain.com. This file is a YAML file.\n\n* token: 1234 \n* my_domain: mydomain.com \n* my_subdomain: test \n\n## Instalation from source\n\n```bash\ngit clone https://github.com/educollado/neodigit-dyndns.git\n```\n\nFor this script you need requests as you can see in the code: \n\n```bash\npip install requests\n```\n\nOr maybe you can use the requirements.txt file:\n\n```bash\npip install -r requirements.txt\n```\n\nOne interesting step is to add to your crontab: \n\n```bash\n0,15,30,45 * * * * python3 /path-to/neodigit-dyndns/neodigit_dyndns /url/to/config.cfg > /dev/null 2>&\n```\n\n## Instalation from PiP\n\n```bash\npip install neodigit-dyndns\n```\nhttps://pypi.org/project/neodigit-dyndns/\n\n## Neodigit API\nAPI Documentation: https://developers.neodigit.net/\n\n## License\n[GPL3](https://github.com/educollado/neodigit-dyndns/blob/main/LICENSE)\n",
    'author': 'Eduardo Collado',
    'author_email': 'edu@tecnocratica.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
