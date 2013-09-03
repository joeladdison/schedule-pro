#!/usr/bin/env python
# Taken from http://stackoverflow.com/q/2710861
# Code is used to append the lib folder to the Python path, so modules in it
# can be loaded

import os
import sys

# credit:  Nick Johnson of Google
sys.path.append(os.path.join(os.path.dirname(__file__), 'lib'))