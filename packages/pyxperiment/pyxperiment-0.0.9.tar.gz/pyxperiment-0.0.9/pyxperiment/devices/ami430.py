"""
    pyxperiment/devices/ami430.py: Support for AMI 430 magnet power supply programmer

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
from pyxperiment.frames.device_config import DeviceConfig
from pyxperiment.frames.basic_panels import CaptionTextPanel

class AMI430Supply(VisaInstrument):
    """
    AMI 430 magnet power supply programmer support
    """

    def __init__(self, rm, resource):
        super().__init__(rm, resource)
        self.inst.read_termination = '\r\n'
        read_str = self.read()
        read_str = self.read()
        del read_str

    @staticmethod
    def driver_name():
        return 'AMI 430 magnet power supply programmer'

    def device_name(self):
        value = self.query_id().translate({ord(c): None for c in ['\r', '\n']}).split(',')
        return value[0] + ' ' + value[1] + ' power source'

    def set_pswitch(self, value):
        self.write('PSwitch ' + ('1' if value else '0'))

    def get_pswitch(self):
        return self._query_boolean('PSwitch?')

    def get_coil_const(self):
        return self.query("COIL?")

    def set_volt_limit(self, value):
        self.write('CONF:VOLT:LIM ' + value)

    def get_volt_limit(self):
        return self.query('VOLT:LIM?')

    def set_field_target(self, value):
        self.write('CONF:FIELD:TARG ' + value)

    def get_target_field(self):
        return self.query('FIELD:TARG?')

    def get_field(self):
        return self.query('FIELD:MAG?')

    def get_curr(self):
        return self.query('CURR:MAG?')

    def get_volt(self):
        return self.query('VOLT:SUPP?')

    def get_ramp_seg_field(self, num):
        return self.query('RAMP:RATE:FIELD:'+str(num)+'?').split(',')

    def get_ramp_seg_curr(self, num):
        return self.query('RAMP:RATE:CURR:'+str(num)+'?').split(',')

    def set_ramp_seg_curr(self, num, ramp, end):
        self.write('CONF:RAMP:RATE:CURR '+str(num)+','+ramp+','+end)

    def start_ramp(self):
        self.write('RAMP')

    def pause_ramp(self):
        self.write('PAUSE')

    def zero_ramp(self):
        self.write('ZERO')

    state_values = [
        'RAMPING',
        'HOLDING',
        'PAUSED',
        'MANUAL UP',
        'MANUAL DOWN',
        'ZEROING',
        'QUENCH!!!',
        'AT ZERO',
        'HEATING SWITCH',
        'COOLING SWITCH'
    ]

    def get_state(self):
        value = self.query('STATE?')
        return self.state_values[int(value)-1]

    def get_config_class(self):
        return AMI430SupplyConfig

    def set_value(self, value):
        self.set_field_target(str(value))
        self.start_ramp()

    def get_value(self):
        return self.get_field()

    def stop(self):
        pass

    def check_values(self, values):
        """Проверить что такие значения могут быть установлены с текущими настройками устройства"""
        values = [x for x in values if abs(Decimal(x)) > Decimal('9')]
        return len(values) == 0

    def finished(self):
        return self.get_state() != self.state_values[0]

class AMI430SupplyConfig(DeviceConfig):

    def __init__(self, parent, device):
        DeviceConfig.__init__(self, parent, device, 300)

    def _create_controls(self):
        self.controls = []
        self.columns = 3

        self.target_field = CaptionTextPanel(self.panel, label='Target field', show_mod=True)
        self.controls.append(self.target_field)
        self.voltage_limit = CaptionTextPanel(self.panel, label='Voltage limit', show_mod=True)
        self.controls.append(self.voltage_limit)
        self.coilconst = CaptionTextPanel(self.panel, label='Coil constant')
        self.coilconst.SetEnabled(False)
        self.controls.append(self.coilconst)

        self.field = CaptionTextPanel(self.panel, label='Magnet field')
        self.field.SetEnabled(False)
        self.controls.append(self.field)
        self.volt = CaptionTextPanel(self.panel, label='Magnet voltage')
        self.volt.SetEnabled(False)
        self.controls.append(self.volt)
        self.curr = CaptionTextPanel(self.panel, label='Magnet current')
        self.curr.SetEnabled(False)
        self.controls.append(self.curr)

        self.ramp_segments = 3
        self.ramp_limit = []
        self.ramp_rate = []
        for i in range(self.ramp_segments):
            segment_limit = CaptionTextPanel(self.panel, label='Segment limit', show_mod=True)
            self.controls.append(segment_limit)
            self.ramp_limit.append(segment_limit)
            segment_rate = CaptionTextPanel(self.panel, label='Segment rate', show_mod=True)
            self.controls.append(segment_rate)
            self.ramp_rate.append(segment_rate)

        self.btn_ramp = wx.Button(self.panel, label='Ramp')
        self.Bind(wx.EVT_BUTTON, self.on_btn_ramp, self.btn_ramp)
        self.controls.append(self.btn_ramp)
        self.btn_pause = wx.Button(self.panel, label='Pause')
        self.Bind(wx.EVT_BUTTON, self.on_btn_pause, self.btn_pause)
        self.controls.append(self.btn_pause)
        self.btn_zero = wx.Button(self.panel, label='Zero')
        self.Bind(wx.EVT_BUTTON, self.on_btn_zero, self.btn_zero)
        self.controls.append(self.btn_zero)

        self.pswitch = wx.CheckBox(self.panel, label='Persistent switch heater')
        self.controls.append(self.pswitch)

        self.state = CaptionTextPanel(self.panel, label='State')
        self.state.SetEnabled(False)
        self.controls.append(self.state)

    def on_btn_ramp(self, event):
        self.device.start_ramp()

    def on_btn_pause(self, event):
        self.device.pause_ramp()

    def on_btn_zero(self, event):
        self.device.zero_ramp()

    def read_control(self):
        self.target_field.SetValue(self.device.get_target_field())
        self.voltage_limit.SetValue(self.device.get_volt_limit())

        self.coilconst.SetValue(self.device.get_coil_const())

        for i in range(1, self.ramp_segments+1):
            seg_field = self.device.get_ramp_seg_field(i)
            seg_curr = self.device.get_ramp_seg_curr(i)
            self.ramp_rate[i-1].SetValue(seg_curr[0])
            self.ramp_limit[i-1].SetValue(seg_field[1])

        self.pswitch.SetValue(self.device.get_pswitch())

    def write_control(self):
        if self.target_field.IsModified():
            self.device.set_field_target(self.target_field.GetValue())
        if self.pswitch.Value != self.device.get_pswitch():
            self.device.set_pswitch(self.pswitch.Value)
        if self.voltage_limit.IsModified():
            self.device.set_volt_limit(self.voltage_limit.GetValue())
        # Пока только скорость разветки
        for i in range(0, self.ramp_segments):
            if self.ramp_rate[i].IsModified():
                seg_curr = self.device.get_ramp_seg_curr(i+1)
                self.device.set_ramp_seg_curr(i+1, self.ramp_rate[i].GetValue(), seg_curr[1])

    def on_reload_timer(self, event):
        self.field.SetValue(self.device.get_field())
        self.volt.SetValue(self.device.get_volt())
        self.curr.SetValue(self.device.get_curr())
        self.state.SetValue(self.device.get_state())
