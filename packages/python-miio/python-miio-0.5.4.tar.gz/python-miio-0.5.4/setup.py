# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['miio', 'miio.tests']

package_data = \
{'': ['*'], 'miio': ['data/*']}

install_requires = \
['appdirs>=1,<2',
 'attrs',
 'click>=7,<8',
 'construct>=2.10.56,<3.0.0',
 'croniter>=0,<1',
 'cryptography>=3,<4',
 'netifaces>=0,<1',
 'pytz',
 'tqdm>=4,<5',
 'zeroconf>=0,<1']

extras_require = \
{':python_version <= "3.7"': ['importlib_metadata>=1,<2'],
 'docs': ['sphinx>=3,<4',
          'sphinx_click>=2,<3',
          'sphinxcontrib-apidoc>=0,<1',
          'sphinx_rtd_theme>=0,<1']}

entry_points = \
{'console_scripts': ['miceil = miio.ceil_cli:cli',
                     'mieye = miio.philips_eyecare_cli:cli',
                     'miio-extract-tokens = miio.extract_tokens:main',
                     'miiocli = miio.cli:create_cli',
                     'miplug = miio.plug_cli:cli',
                     'mirobo = miio.vacuum_cli:cli']}

setup_kwargs = {
    'name': 'python-miio',
    'version': '0.5.4',
    'description': 'Python library for interfacing with Xiaomi smart appliances',
    'long_description': 'python-miio\n===========\n\n|Chat| |PyPI version| |Build Status| |Coverage Status| |Docs| |Black| |Hound|\n\nThis library (and its accompanying cli tool) can be used to interface with devices using Xiaomi\'s `miIO <https://github.com/OpenMiHome/mihome-binary-protocol/blob/master/doc/PROTOCOL.md>`__ and miOT protocols.\n\n\nGetting started\n---------------\n\nIf you already have a token for your device and the device type, you can directly start using `miiocli` tool.\nIf you don\'t have a token for your device, refer to `Getting started <https://python-miio.readthedocs.io/en/latest/discovery.html>`__ section of `the manual <https://python-miio.readthedocs.io>`__ for instructions how to obtain it.\n\nThe `miiocli` is the main way to execute commands from command line.\nYou can always use `--help` to get more information about the available commands.\nFor example, executing it without any extra arguments will print out options and available commands::\n\n    $ miiocli --help\n    Usage: miiocli [OPTIONS] COMMAND [ARGS]...\n\n    Options:\n      -d, --debug\n      -o, --output [default|json|json_pretty]\n      --help                          Show this message and exit.\n\n    Commands:\n      airconditioningcompanion\n      ..\n\nYou can get some information from any miIO/miOT device, including its device model, using the `info` command::\n\n    miiocli device --ip <ip> --token <token> info\n\n    Model: some.device.model1\n    Hardware version: esp8285\n    Firmware version: 1.0.1_0012\n    Network: {\'localIp\': \'<ip>\', \'mask\': \'255.255.255.0\', \'gw\': \'<ip>\'}\n    AP: {\'rssi\': -73, \'ssid\': \'<nnetwork>\', \'primary\': 11, \'bssid\': \'<bssid>\'}\n\nEach different device type is supported by their corresponding module (e.g., `vacuum` or `fan`).\nYou can get the list of available commands for any given module by passing `--help` argument to it::\n\n    $ miiocli vacuum --help\n\n    Usage: miiocli vacuum [OPTIONS] COMMAND [ARGS]...\n\n    Options:\n      --ip TEXT       [required]\n      --token TEXT    [required]\n      --id-file FILE\n      --help          Show this message and exit.\n\n    Commands:\n      add_timer                Add a timer.\n      ..\n\nAPI usage\n---------\nAll functionality is accessible through the `miio` module::\n\n    from miio import Vacuum\n\n    vac = Vacuum("<ip address>", "<token>")\n    vac.start()\n\nEach separate device type inherits from `miio.Device`\n(and in case of miOT devices, `miio.MiotDevice`) which provides common API.\n\nPlease refer to `API documentation <https://python-miio.readthedocs.io/en/latest/miio.html>`__ for more information.\n\n\nTroubleshooting\n---------------\nYou can find some solutions for the most common problems can be found in `Troubleshooting <https://python-miio.readthedocs.io/en/latest/troubleshooting.html>`__ section.\n\nIf you have any questions, or simply want to join up for a chat, check `our Matrix room <https://matrix.to/#/#python-miio-chat:matrix.org>`__.\n\nContributing\n------------\n\nWe welcome all sorts of contributions from patches to add improvements or fixing bugs to improving the documentation.\nTo ease the process of setting up a development environment we have prepared `a short guide <https://python-miio.readthedocs.io/en/latest/new_devices.html>`__ for getting you started.\n\n\nSupported devices\n-----------------\n\n-  Xiaomi Mi Robot Vacuum V1, S5, M1S\n-  Xiaomi Mi Home Air Conditioner Companion\n-  Xiaomi Mi Smart Air Conditioner A (xiaomi.aircondition.mc1, mc2, mc4, mc5)\n-  Xiaomi Mi Air Purifier\n-  Xiaomi Mi Air Humidifier\n-  Xiaomi Aqara Camera\n-  Xiaomi Aqara Gateway (basic implementation, alarm, lights)\n-  Xiaomi Mijia 360 1080p\n-  Xiaomi Mijia STYJ02YM (Viomi)\n-  Xiaomi Mi Smart WiFi Socket\n-  Xiaomi Chuangmi Plug V1 (1 Socket, 1 USB Port)\n-  Xiaomi Chuangmi Plug V3 (1 Socket, 2 USB Ports)\n-  Xiaomi Smart Power Strip V1 and V2 (WiFi, 6 Ports)\n-  Xiaomi Philips Eyecare Smart Lamp 2\n-  Xiaomi Philips RW Read (philips.light.rwread)\n-  Xiaomi Philips LED Ceiling Lamp\n-  Xiaomi Philips LED Ball Lamp (philips.light.bulb)\n-  Xiaomi Philips LED Ball Lamp White (philips.light.hbulb)\n-  Xiaomi Philips Zhirui Smart LED Bulb E14 Candle Lamp\n-  Xiaomi Philips Zhirui Bedroom Smart Lamp\n-  Xiaomi Universal IR Remote Controller (Chuangmi IR)\n-  Xiaomi Mi Smart Pedestal Fan V2, V3, SA1, ZA1, ZA3, ZA4, P5, P9, P10, P11\n-  Xiaomi Mi Air Humidifier V1, CA1, CA4, CB1, MJJSQ, JSQ001\n-  Xiaomi Mi Water Purifier (Basic support: Turn on & off)\n-  Xiaomi Mi Water Purifier D1, C1 (Triple Setting)\n-  Xiaomi PM2.5 Air Quality Monitor V1, B1, S1\n-  Xiaomi Smart WiFi Speaker\n-  Xiaomi Mi WiFi Repeater 2\n-  Xiaomi Mi Smart Rice Cooker\n-  Xiaomi Smartmi Fresh Air System VA2 (zhimi.airfresh.va2), VA4 (zhimi.airfresh.va4), T2017 (dmaker.airfresh.t2017)\n-  Yeelight lights (basic support, we recommend using `python-yeelight <https://gitlab.com/stavros/python-yeelight/>`__)\n-  Xiaomi Mi Air Dehumidifier\n-  Xiaomi Tinymu Smart Toilet Cover\n-  Xiaomi 16 Relays Module\n-  Xiaomi Xiao AI Smart Alarm Clock\n-  Smartmi Radiant Heater Smart Version (ZA1 version)\n-  Xiaomi Mi Smart Space Heater\n-  Xiaomiyoupin Curtain Controller (Wi-Fi) (lumi.curtain.hagl05)\n\n\n*Feel free to create a pull request to add support for new devices as\nwell as additional features for supported devices.*\n\n\nHome Assistant support\n----------------------\n\n-  `Xiaomi Mi Robot Vacuum <https://home-assistant.io/components/vacuum.xiaomi_miio/>`__\n-  `Xiaomi Philips Light <https://home-assistant.io/components/light.xiaomi_miio/>`__\n-  `Xiaomi Mi Air Purifier and Air Humidifier <https://home-assistant.io/components/fan.xiaomi_miio/>`__\n-  `Xiaomi Smart WiFi Socket and Smart Power Strip <https://home-assistant.io/components/switch.xiaomi_miio/>`__\n-  `Xiaomi Universal IR Remote Controller <https://home-assistant.io/components/remote.xiaomi_miio/>`__\n-  `Xiaomi Mi Air Quality Monitor (PM2.5) <https://home-assistant.io/components/sensor.xiaomi_miio/>`__\n-  `Xiaomi Aqara Gateway Alarm <https://home-assistant.io/components/alarm_control_panel.xiaomi_miio/>`__\n-  `Xiaomi Mi Home Air Conditioner Companion <https://github.com/syssi/xiaomi_airconditioningcompanion>`__\n-  `Xiaomi Mi WiFi Repeater 2 <https://www.home-assistant.io/components/device_tracker.xiaomi_miio/>`__\n-  `Xiaomi Mi Smart Pedestal Fan <https://github.com/syssi/xiaomi_fan>`__\n-  `Xiaomi Mi Smart Rice Cooker <https://github.com/syssi/xiaomi_cooker>`__\n-  `Xiaomi Raw Sensor <https://github.com/syssi/xiaomi_raw>`__\n\n\n.. |Chat| image:: https://matrix.to/img/matrix-badge.svg\n   :target: https://matrix.to/#/#python-miio-chat:matrix.org\n.. |PyPI version| image:: https://badge.fury.io/py/python-miio.svg\n   :target: https://badge.fury.io/py/python-miio\n.. |Build Status| image:: https://travis-ci.org/rytilahti/python-miio.svg?branch=master\n   :target: https://travis-ci.org/rytilahti/python-miio\n.. |Coverage Status| image:: https://coveralls.io/repos/github/rytilahti/python-miio/badge.svg?branch=master\n   :target: https://coveralls.io/github/rytilahti/python-miio?branch=master\n.. |Docs| image:: https://readthedocs.org/projects/python-miio/badge/?version=latest\n   :alt: Documentation status\n   :target: https://python-miio.readthedocs.io/en/latest/?badge=latest\n.. |Hound| image:: https://img.shields.io/badge/Reviewed_by-Hound-8E64B0.svg\n   :alt: Hound\n   :target: https://houndci.com\n.. |Black| image:: https://img.shields.io/badge/code%20style-black-000000.svg\n    :target: https://github.com/psf/black\n',
    'author': 'Teemu R',
    'author_email': 'tpr@iki.fi',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/rytilahti/python-miio',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6.5,<4.0.0',
}


setup(**setup_kwargs)
