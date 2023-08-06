# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyvera']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.22.0']

setup_kwargs = {
    'name': 'pyvera',
    'version': '0.3.11',
    'description': 'Python API for talking to Veracontrollers',
    'long_description': '# PyVera\nA simple Python library to control devices via the Vera controller (http://getvera.com/).\n\nBased on https://github.com/jamespcole/home-assistant-vera-api\n\nAdditions to support subscriptions and some additional devices\n\nHow to use\n----------\n\n\n    >>> import pyvera\n\n    >>> controller = pyvera.VeraController("http://192.168.1.161:3480/")\n    >>> devices = controller.get_devices(\'On/Off Switch\')\n    >>> devices\n    [VeraSwitch (id=15 category=On/Off Switch name=Bookcase Uplighters), VeraSwitch (id=16 category=On/Off Switch name=Bookcase device)]\n\n    >>> devices[1]\n    VeraSwitch (id=15 category=On/Off Switch name=Bookcase Uplighters)\n\n    >>> devices[1].is_switched_on()\n    False\n\n    >>> devices[1].switch_on()\n    >>> devices[1].is_switched_on()\n    True\n\n    >>> devices[1].switch_off()\n\n\nExamples\n-------\n\nThere is some example code (that can also help with tracing and debugging) in the `examples` directory.\n\nThis will list your vera devices\n~~~~\n$ ./examples/list_devices.py -u http://192.168.1.161:3480\n~~~~\n\nThis will show you events on a particular device (get the id from the example above)\n~~~~\n$ ./examples/device_listener.py -u http://192.168.1.161:3480/  -i 26\n~~~~\n\nIf you have locks - this will show you information about them.\n~~~~\n$ ./examples/show_lock_info.py -u http://192.168.1.161:3480/\n~~~~\n\nDebugging\n-------\nYou may use the PYVERA_LOGLEVEL environment variable to output more verbose messages to the console.  For instance, to show all debug level messages using the list-devices implementation in the example directory, run something similar to:\n~~~~\n$ PYVERA_LOGLEVEL=DEBUG ./examples/list-devices.py -u http://192.168.1.161:3480\n~~~~\n\nDebugging inside home assistant\n-------\nIf you\'re running pyvera inside home assistant and need the debugging log traces, add the following to your `configuration.yaml`\n\n\n~~~~\nlogger:\n    logs:\n        pyvera: debug\n~~~~\n\nDeveloping\n-------\nSetup and builds are fully automated. You can run build pipeline locally by running.\n~~~~\n# Setup, build, lint and test the code.\n./scripts/build.sh\n~~~~\n\nLicense\n-------\nThe initial code was initially was written by James Cole and released under the BSD license. The rest is released under the MIT license.\n',
    'author': 'James Cole',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pavoni/pyvera',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
