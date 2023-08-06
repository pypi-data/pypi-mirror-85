"""
    pyxperiment/devices/srs/dc205.py:
    Support for SRS DC205 programmable DC source

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
import wx
from pyxperiment.controller import VisaInstrument
from pyxperiment.controller.device_options import (
    ListDeviceOption, ValueDeviceOption, StateDeviceOption, BooleanOption
)

class SRSDC205Source(VisaInstrument):
    """
    DC205 programmable DC source support
    """

    def __init__(self, rm, resource):
        super().__init__(rm, resource)
        if hasattr(self.inst, 'baud_rate'):
            self.inst.baud_rate = 115200
        self.inst.write_termination = '\n'
        self.inst.read_termination = '\r\n'
        self.write('*CLS')
        self.idn = self.query_id().split(',')
        if self.idn[0] != 'Stanford_Research_Systems':
            raise ValueError('Invalid manufacturer: ' + self.idn[0])
        if self.idn[1].upper() != 'DC205':
            raise ValueError('Invalid model: ' + self.idn[1])
        self.idn[0] = self.idn[0].replace('_', ' ')
        self.write('TOKN 0')

        self.set_options([
            self.output_on,
            self.four_wire,
            self.output_float,
            self.volt_range,
            ValueDeviceOption('Value', 'V', self.get_value, self.set_value),
        ])

    @staticmethod
    def driver_name():
        return 'SRS DC205 programmable DC source'

    def device_name(self):
        return self.idn[0] + ' ' + self.idn[1] + ' DC source'

    overload = BooleanOption(
        'Overload',
        get_func=lambda instr: instr.query('OVLD?'),
    )

    def get_value(self):
        if self.overload.get_value():
            return 'Inf'
        return self.query('VOLT?')

    def set_value(self, value):
        self.write('VOLT ' + str(value))

    def check_values(self, values):
        """
        Проверить что такие значения могут быть установлены с текущими настройками устройства
        """
        current_range = self.get_range()[1]
        values = [x for x in values if abs(Decimal(x)) > current_range[1] or divmod(Decimal(x), current_range[2])[1] > 0]
        return len(values) == 0

    def set_output(self, value):
        dlg = wx.MessageDialog(
            None,
            'Warning! you are trying to modify a' +
            'critical parameter (output on/off).' +
            'Such modification is potentially dangerous to the connected load. Please check twice before proceeding.',
            'Modification of a critical parameter',
            wx.YES_NO | wx.ICON_WARNING
            )
        if dlg.ShowModal() != wx.ID_YES:
            return
        self.write('SOUT ' + value)

    output_on = BooleanOption(
        'Output on',
        get_func=lambda instr: instr.query('SOUT?'),
        set_func=lambda instr, value: instr.set_output(value),
    )

    four_wire = BooleanOption(
        'Four wire',
        get_func=lambda instr: instr.query('SENS?'),
        set_func=lambda instr, value: instr.write('SENS '+value),
    )

    output_float = BooleanOption(
        'Floating output',
        get_func=lambda instr: instr.query('ISOL?'),
        set_func=lambda instr, value: instr.write('ISOL '+value),
    )

    volt_range_values = {
        '1 V':('0', Decimal('1.01'), Decimal('0.000001')),
        '10 V':('1', Decimal('10.1'), Decimal('0.00001')),
        '100 V':('2', Decimal('101'), Decimal('0.0001')),
        }

    def get_range(self):
        value = self.query('RNGE?')
        for val in self.volt_range_values.items():
            if Decimal(val[1][0]) == Decimal(value):
                return val
        raise ValueError('Invalid range: ' + value)

    def set_range(self, value):
        try:
            volt_range = self.volt_range_values[value]
        except KeyError:
            raise ValueError('Invalid range: ' + value)
        self.write('RNGE ' + volt_range[0])

    volt_range = ListDeviceOption(
        'Source voltage range',
        volt_range_values.keys(),
        get_func=lambda instr: instr.get_range()[0],
        set_func=lambda instr, value: instr.set_range(value),
        enabled=lambda instr: not instr.output_on.get_value()
    )
