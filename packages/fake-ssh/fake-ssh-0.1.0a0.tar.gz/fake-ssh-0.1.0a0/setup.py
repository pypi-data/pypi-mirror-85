# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fake_ssh', 'fake_ssh.demo']

package_data = \
{'': ['*']}

install_requires = \
['Logbook>=1.5.3,<2.0.0', 'paramiko>=2.4,<3.0']

entry_points = \
{'console_scripts': ['echo_server = fake_ssh.demo.echo_server:main']}

setup_kwargs = {
    'name': 'fake-ssh',
    'version': '0.1.0a0',
    'description': 'Fakes an SSH Server',
    'long_description': None,
    'author': 'David Sternlicht',
    'author_email': 'dsternlicht@infinidat.com',
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
