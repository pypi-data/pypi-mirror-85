"""
    pyxperiment/devices/testdevice.py: Dummy device for test purposes

    This file is part of the PyXperiment project.

    Copyright (c) 2019 PyXperiment Developers

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in
    all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
    THE SOFTWARE.
"""

import random
import time

from pyxperiment.controller.device_options import ValueDeviceOption
from pyxperiment.controller.instrument import Instrument

class TestDevice(Instrument):

    def __init__(self, rm, resource):
        super().__init__('')
        self.last_value = 0
        self.last_value2 = 0
        self.options = []
        self.resource = resource if resource else 'Test address'

    @staticmethod
    def driver_name():
        return 'Test'

    def device_name(self):
        return 'Test device'

    @property
    def location(self):
        return self.resource

    def get_value(self):
        return str(self.last_value)

    def get_value2(self):
        self.last_value2 += 0.1
        #time.sleep(0.01)
        return str(self.last_value2)

    def set_value(self, value):
        self.last_value = value

    def get_random(self):
        #time.sleep(0.1)
        return str(random.triangular(-10, 10))

    value = ValueDeviceOption('Test', 'V', get_value, set_value)
    value2 = ValueDeviceOption('Test up', 'V', get_value2)
    rand = ValueDeviceOption('Random', 'V', get_random)
