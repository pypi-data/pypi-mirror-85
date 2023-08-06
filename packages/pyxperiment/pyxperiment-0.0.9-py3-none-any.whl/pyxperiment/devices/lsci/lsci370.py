"""
    pyxperiment/devices/lsci/lsci370.py:
    Support for Lake Shore Model 370 resistance bridge

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

import time
from decimal import Decimal
import wx
from pyxperiment.controller import VisaInstrument
from pyxperiment.controller.device_options import (
    ValueDeviceOption, ListDeviceOption
)
from pyxperiment.frames.device_config import (
    DeviceConfig, ControlField, ControlPanel, MultiControlPanel, option_to_control
)
from pyxperiment.frames.basic_panels import (
    CaptionTextPanel, CaptionDropBox, ModifiedCheckBox
)
from pyxperiment.controller.validation import SimpleRangeValidator

class LakeShore370ResBridge(VisaInstrument):
    """
    Lake Shore Model 370 resistance bridge support
    """

    def __init__(self, rm, resource):
        super().__init__(rm, resource)
        self.write('*CLS')
        self.set_options([
            self.sample_control_mode,
            self.sample_heater_range,
            self.still_voltage,
            self.target_temp
        ])
        self.current_value = None

    @staticmethod
    def driver_name():
        return 'Lake Shore Model 370 resistance bridge'

    def get_config_class(self):
        return LakeShore370ResBridgeConfig

    def device_name(self):
        value = self.query_id().translate({ord(c): None for c in ['\r', '\n']}).split(',')
        return value[0] + ' ' + value[1] + ' resistance bridge'

    analog_mode_values = [
        'Off', 'Channel', 'Manual', 'Zone', 'Still'
        ]

    def get_analog_mode(self, num):
        values = self.query('ANALOG? ' + str(num)).split(',')
        values[0] = int(values[0]) == 1# bipolar
        values[1] = self.analog_mode_values[int(values[1])]
        return values[:2]

    def set_analog_mode(self, num, bipolar, mode):
        values = self.query('ANALOG? ' + str(num)).split(',')
        values[0] = '1' if bipolar else '0'
        values[1] = str(self.analog_mode_values.index(mode))
        self.write('ANALOG ' + str(num) + ',' + ','.join(values))

    control_mode_values = [
        'Closed Loop (PID)', 'Zone', 'Open Loop', 'Off'
    ]

    sample_control_mode = ListDeviceOption(
        'Heater mode', control_mode_values,
        get_func=lambda instr:
        instr.control_mode_values[int(instr.query('CMODE?'))-1],
        set_func=lambda instr, value:
        instr.write('CMODE '+ str(instr.control_mode_values.index(value)+1)),
    )

    heater_input_values = [
        '1', '2', '3', '4', '5', '6', '7',
        '8', '9', '10', '11', '12', '13', '14', '15', '16'
        ]

    def get_control_setup(self):
        values = self.query('CSET?').split(',')
        values[0] = str(int(values[0]))
        values[1] = int(values[1]) == 1# filter
        values[3] = str(int(values[3]))
        values[5] = self.heater_range_values[int(values[5])]
        return [values[0],values[1],values[3],values[5]]

    def set_control_setup(self, input_num, filter_on, delay, limit):
        values = self.query('CSET?').split(',')
        values[0] = input_num
        values[1] = ('1' if filter_on else '0')
        values[3] = str(delay)
        values[5] = str(self.heater_range_values.index(limit))
        self.write('CSET ' + ','.join(values))

    heater_range_values = [
        'off', '31.6 µA', '100 µA', '316 µA',
        '1.00 mA', '3.16 mA', '10.0 mA', '31.6 mA', '100 mA'
        ]

    sample_heater_range = ListDeviceOption(
        'Sample heater range', heater_range_values,
        get_func=lambda instr:
        instr.heater_range_values[int(instr.query('HTRRNG?'))],
        set_func=lambda instr, value:
        instr.write('HTRRNG '+ str(instr.heater_range_values.index(value))),
    )

    def get_pid_values(self):
        return map(lambda x: str(Decimal(x)), self.query('PID?').split(','))

    def set_pid_values(self, p_value, i_value, d_value):
        self.write('PID '+str(p_value)+','+str(i_value)+','+str(d_value))

    def get_ramp(self):
        values = self.query('RAMP?').split(',')
        values[0] = int(values[0]) == 1
        values[1] = values[1].translate({ord(c): None for c in ['\r', '\n']})
        return values

    def set_ramp(self, ramp_on, ramp_rate):
        self.write('RAMP ' + ('1' if ramp_on else '0') + ',' + str(ramp_rate))

    temperature = [
        ValueDeviceOption(
            'Temperature CH ' + str(i), 'K',
            get_func=lambda instr, ch=i: instr.query('RDGK? '+str(ch)).translate({ord(c): None for c in ['\r', '\n']})
            )
        for i in [2, 6]]

    resistance = [
        ValueDeviceOption(
            'Resistance CH ' + str(i), 'Ohm',
            get_func=lambda instr, ch=i: instr.query('RDGR? '+str(ch)).translate({ord(c): None for c in ['\r', '\n']})
            )
        for i in [2, 6]]

    still_voltage = ValueDeviceOption(
        'Still output', 'V',
        get_func=lambda instr:
        str(Decimal(instr.query('STILL?'))/Decimal('10')),
        set_func=lambda instr, value:
        instr.write('STILL '+str(Decimal(value)*Decimal('10'))),
        validator=SimpleRangeValidator('0', '10'),
        sweepable=False
    )

    target_temp = ValueDeviceOption(
        'Set Temperature', 'K',
        get_func=lambda instr: instr.query('SETP?').translate({ord(c): None for c in ['\r', '\n']}),
        set_func=lambda instr, value: instr.write('SETP '+str(value)),
        validator=SimpleRangeValidator('0', '0.8'),
        sweepable=False
    )

    def set_value(self, value):
        self.target_temp.set_value(value)
        self.current_value = value

    def check_values(self, values):
        return self.target_temp.check_values(values)

    def finished(self):
        if self.current_value != None:
            return abs(
                (Decimal(self.current_value) - Decimal(self.temperature[1].get_value())
                ) / Decimal(self.current_value)) < Decimal('0.02')
        return True

    def get_value(self):
        return self.temperature[1].get_value()

class LakeShore370ResBridgeConfig(DeviceConfig):

    def __init__(self, parent, device):
        super().__init__(parent, device, 100)

    class SampleHeaterPanel(ControlPanel):
        def __init__(self, parent, device):
            super().__init__(parent, 'Sample Heater', wx.VERTICAL)
            self.device = device

            heater_mode_panel = MultiControlPanel(
                self, None, lambda dev=device: dev.get_control_setup(),
                lambda x, dev=device: dev.set_control_setup(*x), wx.VERTICAL
                )
            heater_mode_panel.set_controls([
                CaptionDropBox(heater_mode_panel, 'Heater input', device.heater_input_values),
                ModifiedCheckBox(heater_mode_panel, 'Filter'),
                CaptionTextPanel(heater_mode_panel, 'Delay'),
                CaptionDropBox(heater_mode_panel, 'Heater limit', device.heater_range_values),
            ])

            heater_pid_panel = MultiControlPanel(
                self, 'PID', lambda dev=device: dev.get_pid_values(),
                lambda x, dev=device: dev.set_pid_values(*x), wx.HORIZONTAL
                )
            heater_pid_panel.set_controls([
                CaptionTextPanel(heater_pid_panel, 'P', size=(50, -1)),
                CaptionTextPanel(heater_pid_panel, 'I', size=(50, -1)),
                CaptionTextPanel(heater_pid_panel, 'D', size=(50, -1))
            ])

            heater_ramp_panel = MultiControlPanel(
                self, 'PID Ramp', lambda dev=device: dev.get_ramp(),
                lambda x, dev=device: dev.set_ramp(*x), wx.HORIZONTAL
                )
            heater_ramp_panel.set_controls([
                ModifiedCheckBox(heater_ramp_panel, 'Ramp on'),
                CaptionTextPanel(heater_ramp_panel, 'Ramp rate, K/min'),
            ])

            self.set_controls([
                option_to_control(self, device.sample_control_mode),
                heater_mode_panel,
                option_to_control(self, device.sample_heater_range),
                heater_pid_panel,# Sample heater PID
                heater_ramp_panel,
                option_to_control(self, device.target_temp)
            ])

    class StillHeaterPanel(ControlPanel):
        def __init__(self, parent, device):
            super().__init__(parent, 'Still Heater', wx.VERTICAL)
            self.device = device

            still_mode_panel = MultiControlPanel(
                self, None, lambda dev=self.device: dev.get_analog_mode(2),
                lambda x, dev=self.device: dev.set_analog_mode(2, *x), wx.VERTICAL
            )
            still_mode_panel.set_controls([
                ModifiedCheckBox(still_mode_panel, 'Polarity'),
                CaptionDropBox(still_mode_panel, 'Heater mode', self.device.analog_mode_values),
            ])

            still_power = MultiControlPanel(
                self, None, self.__get_still_power, self.__set_still_power, wx.VERTICAL
                )
            still_power.set_controls([
                CaptionTextPanel(still_power, label='Still power, mW'),
                CaptionTextPanel(still_power, label='Still voltage, V')
            ])
            still_power.controls[1].SetEnabled(False)

            self.set_controls([
                still_mode_panel,
                still_power
            ])

        def __get_still_power(self):
            value = self.device.still_voltage.get_value()
            return [str(pow(Decimal(value)/150, 2)*120*1000), value]

        def __set_still_power(self, power):
            voltage = pow(Decimal(power[0])/1000/120, Decimal('0.5'))*150
            self.device.still_voltage.set_value(voltage)
            time.sleep(0.05)

    def _create_controls(self):
        self.sample_heater = self.SampleHeaterPanel(self.panel, self.device)
        self.still_heater = self.StillHeaterPanel(self.panel, self.device)
        self.current_temp = option_to_control(self.panel, self.device.temperature[1])

        self.controls.append(self.sample_heater)
        self.controls.append(self.still_heater)
        self.controls.append(self.current_temp.control)

    def read_control(self):
        self.sample_heater.read_control()
        self.still_heater.read_control()

    def write_control(self):
        self.sample_heater.write_control()
        self.still_heater.write_control()
        time.sleep(0.1)

    def on_reload_timer(self, event):
        del event
        self.current_temp.read_control()
