"""
    pyxperiment/devices/oxford/ps120_10.py:
    Support for Oxford PS120-10 magnet power supply

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

import re
from decimal import Decimal

from pyxperiment.controller import VisaInstrument
from pyxperiment.controller.device_options import (
    ValueDeviceOption, StateDeviceOption, BooleanDeviceOption
)

class OxfordPS126Supply(VisaInstrument):
    """
    Oxford PS126 magnet power supply support
    """

    def __init__(self, rm, resource):
        super().__init__(rm, resource)
        self.inst.write_termination = '\n\r'
        self.write('Q2')
        self.query('C3')
        for _ in range(100):
            try:
                match = re.match("X([0-9])A([0-9])C([0-9])H([0-9])M([0-9])P([0-9])", self.__read_state())
                if match != None:
                    break
            except Exception:
                pass
        self.set_options([
            ValueDeviceOption(
                'Target field', 'A', self.get_target_field,
                self.set_target_field),
            ValueDeviceOption(
                'Ramp rate', 'A/min', self.get_ramp_rate,
                self.set_ramp_rate),
            BooleanDeviceOption(
                'Switch heater', self.get_pswitch,
                self.set_pswitch),
            StateDeviceOption(
                'State', self.get_state),
            ValueDeviceOption(
                'Voltage', 'V', self.get_volt),
            ValueDeviceOption(
                'Current', 'A', self.get_curr),
            ])

    @staticmethod
    def driver_name():
        return 'Oxford PS126 magnet power supply'

    def device_name(self):
        return 'Oxford PS126 magnet power supply'

    def __read_state(self):
        return self.query('X')

    def set_pswitch(self, value):
        self.query('H' + ('1' if value else '0'))

    def get_pswitch(self):
        match = re.match("X([0-9])A([0-9])C([0-9])H([0-9])M([0-9])P([0-9])", self.__read_state())
        return match.group(4) == '1'

    def set_target_field(self, value):
        self.write('I' + str(int(Decimal(value)*Decimal('100'))))

    def get_target_field(self):
        return str(Decimal(self.query('R5')[1:])/Decimal('100'))

    def get_curr(self):
        return str(Decimal(self.query('R0')[1:])/Decimal('100'))

    def get_volt(self):
        return str(Decimal(self.query('R1')[1:])/Decimal('100'))

    def get_heater_volt(self):
        return str(Decimal(self.query('R2')[1:])/Decimal('100'))

    def get_ramp_rate(self):
        return str(Decimal(self.query('R6')[1:])/Decimal('100'))

    def set_ramp_rate(self, value):
        self.write('S' + str(int(Decimal(value)*Decimal('100'))))

    def start_ramp(self):
        self.write('A1')# up
        self.write('A2')# down

    def pause_ramp(self):
        self.write('A0')# stop

    state_values = [
        'HOLDING',
        'SWEEPING UP',
        'SWEEPING DOWN',
        'TRIPPED',
        'AR120 CHANGE OVER',
        'SWEEP UP AFTER CHANGE OVER',
        'SWEEP DOWN AFTER CHANGE OVER'
    ]

    def get_state(self):
        match = re.match("X([0-9])A([0-9])C([0-9])H([0-9])M([0-9])P([0-9])", self.__read_state())
        return match.group(1) == '1'

    def set_value(self, value):
        self.set_target_field(str(value))
        self.start_ramp()

    def get_value(self):
        return self.get_curr()

    def check_values(self, values):
        """Проверить что такие значения могут быть установлены с текущими настройками устройства"""
        values = [x for x in values if abs(Decimal(x)) > Decimal('120')]
        return len(values) == 0

    def finished(self):
        return self.get_state() != self.state_values[0]
