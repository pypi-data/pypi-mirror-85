#!/usr/bin/env python3

import logging
logging.getLogger().setLevel(logging.DEBUG)

from iot_device import device_registry
device_registry.main()
