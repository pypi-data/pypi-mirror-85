#!python

import logging
logging.getLogger().setLevel(logging.INFO)

from iot_device import device_registry
device_registry.main()
