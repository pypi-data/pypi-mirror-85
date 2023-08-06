# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['roonapi']

package_data = \
{'': ['*']}

install_requires = \
['ifaddr>=0.1.0', 'requests>=2.0', 'six>=1.10.0', 'websocket_client>=0.57.0']

setup_kwargs = {
    'name': 'roonapi',
    'version': '0.0.27',
    'description': 'Provides a python interface to interact with Roon',
    'long_description': '# python-roon\npython library to interface with the Roon API (www.roonlabs.com)\n\nFull documentation will follow asap\nSee the tests folder for some more code examples.\n\n\nSome example code:\n\n```\nfrom roonapi import RoonApi\nappinfo = {\n        "extension_id": "python_roon_test",\n        "display_name": "Python library for Roon",\n        "display_version": "1.0.0",\n        "publisher": "marcelveldt",\n        "email": "mygreat@emailaddress.com"\n    }\n\n# host can be None if you want to use discovery - but this sometimes returns the local machine, not the real roon server\nhost = "192.168.1.x"\n\n# Can be None if you don\'t yet have a token\ntoken = open(\'mytokenfile\').read()\n\nroonapi = RoonApi(appinfo, token)\n\n# get all zones (as dict)\nprint(roonapi.zones)\n\n# get all outputs (as dict)\nprint(roonapi.outputs)\n\n# receive state updates in your callback\nroonapi.register_state_callback(my_state_callback)\n\n\n# save the token for next time\nwith open(\'mytokenfile\', \'w\') as f:\n    f.write(roonapi.token)\n',
    'author': 'Marcel van der Veldt',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pavoni/pyroon',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
