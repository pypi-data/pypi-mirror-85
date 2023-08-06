"""
    pyxperiment/devices/yokogawa/yokogawaGS200.py: Support for Yokogawa GS200/2553A

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
from pyxperiment.frames.device_config import DeviceConfig, option_to_control
from pyxperiment.frames.basic_panels import (
    CaptionTextPanel, CaptionDropBox, ModifiedCheckBox
)
from pyxperiment.controller.device_options import (
    ValueDeviceOption, ListDeviceOption
)

class YokogawaGS200(VisaInstrument):
    """
    Support for Yokogawa GS200/2553A
    """

    def __init__(self, rm, resource):
        super().__init__(rm, resource)
        self.write('*CLS')
        self.idn = self.query_id().split(',')
        if self.idn[0].upper() != 'YOKOGAWA':
            raise ValueError('Invalid manufacturer: ' + self.idn[0])
        if self.idn[1].upper() == 'GS210':
            self.volt_range_values = self.volt_range_values_gs200
            self.curr_range_values = self.curr_range_values_gs200
        elif self.idn[1].upper() == '2553A':
            self.volt_range_values = self.volt_range_values_2553a
            self.curr_range_values = self.curr_range_values_2553a
            self.write('COMM:HEAD OFF')
        else:
            raise ValueError('Invalid model: ' + self.idn[1])
        self.sweep_ready = True

        self.set_options(
            ([
                self.volt_limit, self.curr_limit,
                self.prog_time, self.prog_slop] if self.idn[1].upper() == 'GS210' else []
                ) + \
            [self.value]
            )

    @staticmethod
    def driver_name():
        return 'Yokogawa GS200/2553A programmable DC source'

    def query(self, data):
        return super().query(data).translate({ord(c): None for c in ['\r', '\n']})

    def device_name(self):
        return self.idn[0].title() + ' ' + self.idn[1] + ' DC source'

    def device_id(self):
        return self.idn[2]

    def _get_condition(self):
        return int(self.query('STAT:COND?'))

    def get_value(self):
        stat = self._get_condition()
        if stat & (1 << 10):
            return '-Inf'
        elif stat & (1 << 11):
            return 'Inf'
        if self.idn[1].upper() == '2553A':
            inv = self.query('OUTP:POL?') == 'INV'
            return str(Decimal(self.query('SOUR:LEV?')) if not inv else -Decimal(self.query('SOUR:LEV?')))
        return self.query('SOUR:LEV?')

    def set_value(self, value):
        if self.idn[1].upper() == '2553A':
            inv = self.query('OUTP:POL?') == 'INV'
            new_inv = Decimal(value) < Decimal('0')
            if new_inv != inv:
                self.write('SOUR:LEV 0')
                self.write('OUTP:POL ' + ('INV' if new_inv else 'NORM'))
                value = abs(Decimal(value))
        self.write('SOUR:LEV ' + str(value))

    def check_values(self, values):
        """Проверить что такие значения могут быть установлены с текущими настройками устройства"""
        current_range = self.get_range()[1]
        values = [x for x in values if abs(Decimal(x)) > current_range[1] or divmod(Decimal(x), current_range[2])[1] > 0]
        return len(values) == 0

    def get_output(self):
        return self._query_boolean('OUTP?')

    def set_output(self, value):
        self.write('OUTP ' + ('1' if value else '0'))

    VOLT_NAME = 'volt'
    CURR_NAME = 'curr'

    function_values = {
        VOLT_NAME:'VOLT',
        CURR_NAME:'CURR',
        }

    def get_function(self):
        func = self.query('SOUR:FUNC?')
        for name, fn in self.function_values.items():
            if fn == func:
                return name
        raise ValueError('Invalid function: ' + func)

    def set_function(self, value):
        try:
            cmd = self.function_values[value]
        except KeyError:
            raise ValueError('Invalid function: ' + value)
        self.write('SOUR:FUNC ' + cmd)

    volt_range_values_gs200 = {
        '10 mV':('10E-3', Decimal('0.012'), Decimal('0.0000001')),
        '100 mV':('100E-3', Decimal('0.12'), Decimal('0.000001')),
        '1 V':('1E0', Decimal('1.2'), Decimal('0.00001')),
        '10 V':('10E0', Decimal('12'), Decimal('0.0001')),
        '30 V':('30E0', Decimal('32'), Decimal('0.001')),
        }

    curr_range_values_gs200 = {
        '1 mA':('1E-3', Decimal('1.2e-3'), Decimal('0.00000001')),
        '10 mA':('10E-3', Decimal('12e-3'), Decimal('0.0000001')),
        '100 mA':('100E-3', Decimal('120e-3'), Decimal('0.000001')),
        '200 mA':('200E-3', Decimal('200e-3'), Decimal('0.000001')),
        }

    volt_range_values_2553a = volt_range_values_gs200

    curr_range_values_2553a = {
        '1 mA':('1E-3', Decimal('1.2e-3'), Decimal('0.00000001')),
        '10 mA':('10E-3', Decimal('12e-3'), Decimal('0.0000001')),
        '30 mA':('30E-3', Decimal('32e-3'), Decimal('0.000001')),
        '100 mA':('100E-3', Decimal('120e-3'), Decimal('0.000001')),
        }

    def get_range(self):
        func = self.get_function()
        value = self.query('SOUR:RANG?')
        if func == self.VOLT_NAME:
            ranges = self.volt_range_values
        elif func == self.CURR_NAME:
            ranges = self.curr_range_values
        else:
            raise ValueError('Invalid function: ' + func)
        for val in ranges.items():
            if Decimal(val[1][0]) == Decimal(value):
                return val
        raise ValueError('Invalid range: ' + value)

    def set_range(self, value):
        func = self.get_function()
        try:
            if func == self.VOLT_NAME:
                volt_range = self.volt_range_values[value]
            elif func == self.CURR_NAME:
                volt_range = self.curr_range_values[value]
            else:
                raise ValueError('Invalid function: ' + func)
        except KeyError:
            raise ValueError('Invalid range: ' + value)
        self.write('SOUR:RANG ' + volt_range[0])

    volt_limit = ValueDeviceOption(
        'Voltage limit', 'V',
        get_func=lambda instr: instr.query('SOUR:PROT:VOLT?'),
        set_func=lambda instr, value: instr.write('SOUR:PROT:VOLT ' + value),
        sweepable=False
    )

    curr_limit = ValueDeviceOption(
        'Current limit', 'A',
        get_func=lambda instr: instr.query('SOUR:PROT:CURR?'),
        set_func=lambda instr, value: instr.write('SOUR:PROT:CURR ' + value),
        sweepable=False
    )

    prog_time = ValueDeviceOption(
        'Program step time', 's',
        get_func=lambda instr: instr.query('PROG:INT?'),
        set_func=lambda instr, value: instr.write('PROG:INT ' + value),
        sweepable=False
    )

    prog_slop = ValueDeviceOption(
        'Program slope time', 's',
        get_func=lambda instr: instr.query('PROG:SLOP?'),
        set_func=lambda instr, value: instr.write('PROG:SLOP ' + value),
        sweepable=False
    )

    value = ValueDeviceOption(
        'Value', None,
        get_func=get_value,
        set_func=set_value
    )

    def get_value_slope(self):
        if not self.sweep_ready:
            #val = int(self.query(':STAT:EVEN?'))
            #while (val & 128) != 1:
            #    val = int(self.query(':STAT:EVEN?'))
            self.sweep_ready = True
        return self.get_value()

    def set_value_slope(self, value):
        self.sweep_ready = False
        self.write(':PROG:REP 0;:PROG:EDIT:STAR;')
        self.set_value(value)
        self.write(':PROG:EDIT:END;:PROG:RUN')

    value_slope = ValueDeviceOption(
        'Value (with slope)', None,
        get_func=get_value_slope,
        set_func=set_value_slope
    )

    def get_config_class(self):
        return YokogawaGS200Config

class YokogawaGS200Config(DeviceConfig):

    def _range_value(self, func):
        def range_value(item):
            return func(item)[1]
        return range_value

    def _create_controls(self):
        self.controls = []
        self.function = CaptionDropBox(self.panel, 'Function', self.device.function_values)
        self.controls.append(self.function)
        self.range = CaptionDropBox(self.panel, 'Range', [])
        self.controls.append(self.range)
        if self.device.idn[1].upper() != '2553A':
            self.volt_limit = option_to_control(self.panel, self.device.volt_limit)
            self.controls.append(self.volt_limit.control)
            self.curr_limit = option_to_control(self.panel, self.device.curr_limit)
            self.controls.append(self.curr_limit.control)
        self.value = CaptionTextPanel(self.panel, 'Value', show_mod=True)
        self.output = ModifiedCheckBox(self.panel, label='Output on')
        self.controls.append(self.value)
        self.controls.append(self.output)
        if self.device.idn[1].upper() != '2553A':
            self.prog_time = option_to_control(self.panel, self.device.prog_time)
            self.prog_slop = option_to_control(self.panel, self.device.prog_slop)
            self.controls.append(self.prog_time.control)
            self.controls.append(self.prog_slop.control)

    def read_control(self):
        self.function.SetValue(self.device.get_function())
        if self.function.GetValue() == self.device.VOLT_NAME:
            self.range.SetItems(
                sorted(
                    self.device.volt_range_values,
                    key=self._range_value(self.device.volt_range_values.__getitem__)
                )
            )
        elif self.function.GetValue() == self.device.CURR_NAME:
            self.range.SetItems(
                sorted(
                    self.device.curr_range_values,
                    key=self._range_value(self.device.curr_range_values.__getitem__)
                )
            )
        self.range.SetValue(self.device.get_range()[0])
        if self.device.idn[1].upper() != '2553A':
            self.volt_limit.read_control()
            self.curr_limit.read_control()
            self.prog_slop.read_control()
            self.prog_time.read_control()
        self.value.SetValue(str(Decimal(self.device.get_value())))
        self.output.SetValue(self.device.get_output())

    def write_control(self):
        if (self.output.IsModified() and self.output.GetValue() != self.device.get_output()) or (self.function.IsModified() and self.function.GetValue() != self.device.get_function()):
            dlg = wx.MessageDialog(
                self,
                'Warning! you are trying to modify a' +
                'critical parameter (output on/off, output function).' +
                'Such modification is potentially dangerous to the connected load. Please check twice before proceeding.',
                'Modification of a critical parameter',
                wx.YES_NO | wx.ICON_WARNING
                )
            if dlg.ShowModal() != wx.ID_YES:
                return
        if self.function.IsModified() and self.function.GetValue() != self.device.get_function():
            self.device.set_function(self.function.GetValue())
        if self.range.IsModified():
            self.device.set_range(self.range.GetValue())
        if self.value.IsModified():
            self.device.set_value(self.value.GetValue())
        if self.output.IsModified() and self.output.GetValue() != self.device.get_output():
            self.device.set_output(self.output.GetValue())
        if self.device.idn[1].upper() != '2553A':
            self.volt_limit.write_control()
            self.curr_limit.write_control()
            self.prog_slop.write_control()
            self.prog_time.write_control()
