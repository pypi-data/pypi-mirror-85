"""
    pyxperiment/devices/rs8043.py:
    Support for Rohde & Schwarz power source

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

from decimal import Decimal

from pyxperiment.controller import VisaInstrument
from pyxperiment.controller.device_options import (
    ValueDeviceOption, ListDeviceOption, TimeoutOption
)

class RS8043PowerSource(VisaInstrument):
    """
    Rohde&Schwarz 804x power source support
    """

    channels_num = 1

    def __init__(self, rm, resource):
        super().__init__(rm, resource)
        self.inst.write_termination = '\n'
        self.inst.read_termination = '\n'
        self.write('*CLS')
        self.idn = self.query_id().split(',')
        self.set_options(
            self.voltage + self.current
            )

    @staticmethod
    def driver_name():
        return 'Rohde&Schwarz 804x power source'

    def device_name(self):
        return self.idn[0].title() + ' ' + self.idn[1] + ' power source'

    def set_volt(self, channel, value):
        self.write('INST:NSEL ' + str(channel) + '\nVOLT ' + str(value))

    def set_curr(self, channel, value):
        self.write('INST:NSEL ' + str(channel) + '\nCURR ' + str(value))

    def get_volt(self, channel):
        return self.query('INST:NSEL ' + str(channel) + '\nVOLT?')

    def get_curr(self, channel):
        return self.query('INST:NSEL ' + str(channel) + '\nCURR?')

    voltage = [
        ValueDeviceOption(
            'VOLT CH ' + str(i), 'V',
            lambda x, ch=i: x.get_volt(ch),
            lambda x, val, ch=i: x.set_volt(ch, val)
        )  for i in range(1, 4)]

    current = [
        ValueDeviceOption(
            'CURR CH ' + str(i), 'V',
            lambda x, ch=i: x.get_curr(ch),
            lambda x, val, ch=i: x.set_curr(ch, val)
        )  for i in range(1, 4)]
