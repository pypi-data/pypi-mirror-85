#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from gwc import login

LOG_FILENAME = os.path.join(os.path.expanduser('~'), '.genedock/gwc/logs/gwc.log')
CONFIGFILE = os.path.join(os.path.expanduser('~'), '.genedock/gwc/configuration')

base_dir = os.path.dirname(LOG_FILENAME)
if not os.path.exists(base_dir):
    os.makedirs(base_dir)

_logger = login.init_logger(LOG_FILENAME)
