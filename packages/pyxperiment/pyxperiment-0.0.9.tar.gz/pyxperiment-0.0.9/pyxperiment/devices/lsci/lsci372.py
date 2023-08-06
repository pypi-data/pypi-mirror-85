"""
    devices/lsci/lsci372.py: Support for Lake Shore Model 372 resistance bridge

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
import time

import wx
from pyxperiment.controller import VisaInstrument
from pyxperiment.frames.device_config import (
    DeviceConfig, ControlField, ControlPanel, MultiControlPanel
)
from pyxperiment.frames.basic_panels import (
    CaptionTextPanel, CaptionDropBox, ModifiedCheckBox
)

class LakeShore372ResBridge(VisaInstrument):
    """
    Lake Shore Model 372 resistance bridge support
    """

    channels_num = 1

    def __init__(self, rm, resource):
        super().__init__(rm, resource)
        self.currentValue = None

    @staticmethod
    def driver_name():
        return 'Lake Shore Model 372 resistance bridge'

    def device_name(self):
        value = self.query_id().translate({ord(c): None for c in ['\r', '\n']}).split(',')
        return value[0] + ' ' + value[1] + ' resistance bridge'

    def get_config_class(self):
        return LakeShore372ResBridgeConfig

    heater_mode_values = [
        'Off', 'Monitor Out', 'Open Loop (Manual)', 'Zone',
        'Still', 'Closed Loop (PID)', 'Warm up'
        ]

    heater_input_values = [
        '0', 'A', '1', '2', '3', '4', '5', '6', '7',
        '8', '9', '10', '11', '12', '13', '14', '15', '16'
        ]

    def get_heater_mode(self, heater):
        values = self.query('OUTMODE?' + str(heater)).split(',')
        values[0] = self.heater_mode_values[int(values[0])]
        values[2] = int(values[2]) == 1# powerup enable
        values[3] = int(values[3]) == 1# polarity
        values[4] = int(values[4]) == 1# filter
        values[5] = str(int(values[5]))# delay
        return values

    def set_heater_mode(self, heater, mode, input_num, pup_enable, polarity, filter_on, delay):
        self.write(
            'OUTMODE ' + str(heater) + ',' + str(self.heater_mode_values.index(mode)) +
            ',' + str(input_num) + ',' +
            ('1' if pup_enable else '0') + ',' + ('1' if polarity else '0') + ',' +
            ('1' if filter_on else '0') + ',' + str(delay)
            )

    heater_range_values = [
        'off', '31.6 µA', '100 µA', '316 µA',
        '1.00 mA', '3.16 mA', '10.0 mA', '31.6 mA', '100 mA'
        ]

    def get_heater_range(self):
        value = int(self.query('RANGE? 0'))
        return self.heater_range_values[value]

    def set_heater_range(self, value):
        self._write_value_from_list('RANGE 0,', value, self.heater_range_values)

    def get_target_temp(self):
        return self.query('SETP?')

    def set_target_temp(self, value):
        self.write('SETP'+str(value))

    def get_analog_volt(self, num=2):
        value = self.query('ANALOG? ' + str(2))
        return str(Decimal(value.split(',')[6])/Decimal('10'))# percent of 10.0V

    def set_analog_volt(self, value, num=2):
        self.write('ANALOG 2,0,4,0,2,+1.0E+00,+0.0E-03,' + str(Decimal(value)*Decimal('10')))# percent of 10.0V

    def set_still_voltage(self, value):
        self.write('STILL' + str(Decimal(value)*Decimal('10')))# percent of 10.0V

    def get_analog_on(self, heater=2):# 1=warmup, 2=still
        if heater != 1 and heater != 2:
            raise ValueError('Unknown analog heater "' + str(heater) + '"')
        return Decimal(self.query('RANGE?' + str(heater))) == Decimal('1.0')

    def set_analog_on(self, value, heater=2):
        if heater != 1 and heater != 2:
            raise ValueError('Wrong heater "' + str(heater) + '"')
        self.write('RANGE ' +str(heater) + ',' + ('1' if value else '0'))

    def get_pid_values(self, heater):
        if heater != 0 and heater != 1:
            raise ValueError('Wrong heater "' + str(heater) + '"')
        return map(lambda x: str(Decimal(x)), self.query('PID?'+str(heater)).split(','))

    def set_pid_values(self, heater, p_value, i_value, d_value):
        if heater != 0 and heater != 1:
            raise ValueError('Wrong heater "' + str(heater) + '"')
        self.write('PID '+str(heater)+','+str(p_value)+','+str(i_value)+','+str(d_value))

    def get_value(self):
        return self.query('KRDG?6')

    @classmethod
    def is_readable(cls):
        return True

    def set_value(self, value):
        if Decimal(value) < Decimal(self.get_value()):
            self.set_analog_on(True, 2)
        else:
            self.set_analog_on(False, 2)
        time.sleep(0.05)
        self.set_target_temp(value)
        self.currentValue = value

    def check_values(self, values):
        """Проверить что такие значения могут быть установлены с текущими настройками устройства"""
        values = [x for x in values if Decimal(x) > Decimal('0.8') or Decimal(x) < Decimal('0.0')]
        return len(values) == 0

    def finished(self):
        if self.currentValue != None:
            return abs((Decimal(self.currentValue) - Decimal(self.get_value())) / Decimal(self.currentValue)) < Decimal('0.02')
        return True

class LakeShore372ResBridgeConfig(DeviceConfig):

    def __init__(self, parent, device):
        super().__init__(parent, device, 100)

    class SampleHeaterPanel(ControlPanel):
        def __init__(self, parent, device):
            super().__init__(parent, 'Sample Heater', wx.VERTICAL)

            heater_mode_panel = MultiControlPanel(
                self, None, lambda dev=device: dev.get_heater_mode(0),
                lambda x, dev=device: dev.set_heater_mode(0, *x), wx.VERTICAL
                )
            heater_mode_panel.set_controls([
                CaptionDropBox(
                    heater_mode_panel,
                    'Heater mode',
                    [device.heater_mode_values[i] for i in [0, 2, 3, 5]]),
                CaptionDropBox(heater_mode_panel, 'Heater input', device.heater_input_values),
                ModifiedCheckBox(heater_mode_panel, 'Powerup enable'),
                ModifiedCheckBox(heater_mode_panel, 'Polarity'),
                ModifiedCheckBox(heater_mode_panel, 'Filter'),
                CaptionTextPanel(heater_mode_panel, 'Delay'),
            ])
            heater_pid_panel = MultiControlPanel(
                self, 'PID', lambda dev=device: dev.get_pid_values(0),
                lambda x, dev=device: dev.set_pid_values(0, *x), wx.HORIZONTAL
                )
            heater_pid_panel.set_controls([
                CaptionTextPanel(heater_pid_panel, 'P', size=(50, -1)),
                CaptionTextPanel(heater_pid_panel, 'I', size=(50, -1)),
                CaptionTextPanel(heater_pid_panel, 'D', size=(50, -1))
            ])

            self.set_controls([
                heater_mode_panel,
                # Sample heater range
                ControlField(
                    CaptionDropBox(self, 'Sample heater range', device.heater_range_values),
                    device.get_heater_range,
                    device.set_heater_range
                    ),
                # Sample heater PID
                heater_pid_panel,
                # Set temperature for PID
                ControlField(
                    CaptionTextPanel(self, label='Set Temperature, K'),
                    lambda x=device: str(Decimal(x.get_target_temp())),
                    device.set_target_temp
                    )
            ])

    def __set_still_heater_on(self, value):
        self.device.set_analog_on(value, 2)
        time.sleep(0.05)

    def __get_still_power(self):
        value = self.device.get_analog_volt(2)
        return [str(pow(Decimal(value)/150, 2)*120*1000), value]

    def __set_still_power(self, power):
        voltage = pow(Decimal(power[0])/1000/120, Decimal('0.5'))*150
        self.device.set_still_voltage(voltage)
        time.sleep(0.05)
        self.device.set_analog_volt(voltage)
        time.sleep(0.05)

    def _create_controls(self):
        # Sample heater
        self.sample_heater = self.SampleHeaterPanel(self.panel, self.device)

        # Still Heater
        self.still_heater = ControlPanel(self.panel, 'Still Heater', wx.VERTICAL)
        still_mode_panel = MultiControlPanel(
            self.still_heater, None, lambda dev=self.device: dev.get_heater_mode(2),
            lambda x, dev=self.device: dev.set_heater_mode(2, *x), wx.VERTICAL
            )
        still_mode_panel.set_controls([
            CaptionDropBox(
                still_mode_panel,
                'Heater mode',
                [self.device.heater_mode_values[i] for i in [0, 1, 2, 4]]),
            CaptionDropBox(still_mode_panel, 'Heater input', self.device.heater_input_values),
            ModifiedCheckBox(still_mode_panel, 'Powerup enable'),
            ModifiedCheckBox(still_mode_panel, 'Polarity'),
            ModifiedCheckBox(still_mode_panel, 'Filter'),
            CaptionTextPanel(still_mode_panel, 'Delay'),
        ])
        still_power = MultiControlPanel(
            self.still_heater, None, self.__get_still_power, self.__set_still_power, wx.VERTICAL
            )
        still_power.set_controls([
            CaptionTextPanel(still_power, label='Still power, mW'),
            CaptionTextPanel(still_power, label='Still voltage, V')
        ])
        still_power.controls[1].SetEnabled(False)
        self.still_heater.set_controls([
            still_mode_panel,
            # Range on/off
            ControlField(
                ModifiedCheckBox(self.still_heater, label='Heater range on'),
                lambda dev=self.device: dev.get_analog_on(2), self.__set_still_heater_on
                ),
            #
            still_power
        ])

        self.controls.append(self.sample_heater)
        self.controls.append(self.still_heater)

        self.current_temp = CaptionTextPanel(self.panel, label='Temperature, K')
        self.current_temp.SetEnabled(False)
        self.controls.append(self.current_temp)

    def read_control(self):
        self.sample_heater.read_control()
        self.still_heater.read_control()

    def write_control(self):
        self.sample_heater.write_control()
        self.still_heater.write_control()
        time.sleep(0.1)

    def on_reload_timer(self, event):
        del event
        self.current_temp.SetValue(self.device.get_value())
