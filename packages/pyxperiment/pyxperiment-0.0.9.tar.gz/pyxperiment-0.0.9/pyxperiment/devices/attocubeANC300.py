"""
    pyxperiment/devices/attocubeANC300.py: Support for ANC300 piezo controller

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

import wx
from pyxperiment.controller import VisaInstrument
from pyxperiment.frames.device_config import (
    DeviceConfig, ControlField, ControlPanel
)
from pyxperiment.frames.basic_panels import (
    CaptionTextPanel, CaptionDropBox, ModifiedCheckBox
)
from pyxperiment.controller.device_options import ValueDeviceOption

class AttocubeANC300(VisaInstrument):
    """
    ANC300 piezo controller support
    """

    DEFAULT_PORT = 7230
    PWD = '123456'
    ACTIVE_MODULES = [1, 2, 3]

    def __init__(self, rm, resource):
        super().__init__(rm, resource)
        self.modules = [AttocubeANC300.ANM300Channel(self, i) for i in self.ACTIVE_MODULES]
        self.inst.write_termination = '\r\n'
        self.inst.read_termination = '\r\n'
        with self.lock:
            self.inst.read_raw()
            line = self.inst.read()
            self.inst.write(self.PWD)
            line = self.inst.read()
            while line != 'Authorization success':
                line = self.inst.read()
            self.inst.write('echo off')
            line = self.inst.read()
            while line != 'OK':
                line = self.inst.read()

    def write(self, data):
        with self.lock:
            self.inst.write(data)
            line = self.inst.read()
            while line != 'OK':
                line = self.inst.read()

    def query(self, data):
        with self.lock:
            ret = self.inst.query(data)
            match = re.match('([^ =]+) += +([^ ]+)', ret)
            ret = match.group(2)
            line = self.inst.read()
            while line != 'OK':
                line = self.inst.read()
            return ret

    @staticmethod
    def driver_name():
        return 'ANC300 piezo controller (' + str(AttocubeANC300.DEFAULT_PORT) + ')'

    def device_name(self):
        return 'Attocube ANC300 piezo controller'

    class ANM300Channel(object):

        def __init__(self, device, chnum):
            self.device = device
            self.chnum = chnum
            self.steps = 0

        modes = {
            'Ground':'gnd',
            'AC-IN/DC-IN only':'inp',
            'Cap. measurement':'cap',
            'Stepping only':'stp',
            'Offset only':'off',
            'Offset + stepping':'stp+',
            'Offset - stepping':'stp-'
        }

        def get_mode(self):
            data = self.device.query('getm ' + str(self.chnum))
            for name, val in self.modes.items():
                if val == data:
                    return name
            return data

        def set_mode(self, mode):
            self.device.write('setm ' + str(self.chnum) + ' ' + str(self.modes[mode]))

        def get_dc_in(self):
            data = self.device.query('getdci ' + str(self.chnum))
            return data == 'on'

        def set_dc_in(self, value):
            self.device.write('setdci ' + str(self.chnum) + ' ' + ('on' if value else 'off'))

        def get_step_freq(self):
            data = self.device.query('getf ' + str(self.chnum))
            return data

        def set_step_freq(self, freq):
            self.device.write('setf ' + str(self.chnum) + ' ' + str(freq))

        def get_step_volt(self):
            data = self.device.query('getv ' + str(self.chnum))
            return data

        def set_step_volt(self, volt):
            self.device.write('setv ' + str(self.chnum) + ' ' + str(volt))

        def get_offset_volt(self):
            data = self.device.query('geta ' + str(self.chnum))
            return data

        def set_offset_volt(self, volt):
            self.device.write('seta ' + str(self.chnum) + ' ' + str(volt))

        filters = {
            'Off':'off',
            '16 Hz':'16',
            '160 Hz':'160'
        }

        def get_filter(self):
            data = self.device.query('getfil ' + str(self.chnum))
            for name, val in self.filters.items():
                if val == data:
                    return name
            return data

        def set_filter(self, value):
            self.device.write('setfil ' + str(self.chnum) + ' ' + str(self.filters[value]))

        def get_capacitance(self):
            return self.device.query('getc ' + str(self.chnum))

        def get_output(self):
            return self.device.query('geto ' + str(self.chnum))

        def get_steps(self):
            return str(self.steps)

        def set_steps(self, value):
            self.steps = int(value)

        def step_forward(self, steps):
            self.device.write('stepu ' + str(self.chnum) + ' ' + str(steps))
            self.device.write('stepw ' + str(self.chnum))
            self.steps += int(steps)

        def step_backward(self, steps):
            self.device.write('stepd ' + str(self.chnum) + ' ' + str(steps))
            self.device.write('stepw ' + str(self.chnum))
            self.steps -= int(steps)

        def step_cont_forward(self):
            self.device.write('stepu ' + str(self.chnum) + ' c')

        def stop(self):
            self.device.write('stop ' + str(self.chnum))

    def get_module_steps(self, module):
        return self.modules[module].get_steps()

    def set_module_steps(self, module, value):
        value = int(value)
        current = self.modules[module].steps
        if value > current:
            self.modules[module].step_forward(value - current)
        elif value < current:
            self.modules[module].step_backward(current - value)

    def get_module_offset(self, module):
        return self.modules[module].get_offset_volt()

    def set_module_offset(self, module, value):
        self.modules[module].set_offset_volt(value)

    stepping_params = []
    scanning_params = []
    output_params = []
    for i, num in zip(list(range(len(ACTIVE_MODULES))), ACTIVE_MODULES):
        stepping_params.append(ValueDeviceOption(
            'Axis ' + str(num) + ' stepping', '',
            lambda x, mod=i: x.get_module_steps(mod),
            lambda x, val, mod=i: x.set_module_steps(mod, val)))
        scanning_params.append(ValueDeviceOption(
            'Axis ' + str(num) + ' scanning', '',
            lambda x, mod=i: x.get_module_offset(mod),
            lambda x, val, mod=i: x.set_module_offset(mod, val)))
        output_params.append(ValueDeviceOption(
            'Axis ' + str(num) + ' output', '',
            lambda x, mod=i: x.modules[mod].get_output()))

    def get_config_class(self):
        return AttocubeANC300Config

class AttocubeANC300Lua(AttocubeANC300):
    """
    ANC300 piezo controller support (lua console)
    """
    DEFAULT_PORT = 7231
    PWD = '123456'
    ACTIVE_MODULES = [1, 2, 3]

    def __init__(self, rm, resource):
        VisaInstrument.__init__(self, rm, resource)
        self.modules = [AttocubeANC300.ANM300Channel(self, i) for i in self.ACTIVE_MODULES]
        self.inst.write_termination = '\r\n'
        self.inst.read_termination = '\r\n'
        with self.lock:
            self.inst.read_raw()
            line = self.inst.read()
            line = self.inst.read()
            self.inst.write(self.PWD)
            line = self.inst.read()
            while line != 'Authorization success':
                line = self.inst.read()

    scanning_params = []
    for i, num in zip(list(range(len(ACTIVE_MODULES))), ACTIVE_MODULES):
        scanning_params.append(ValueDeviceOption(
            'Axis ' + str(num) + ' scanning', '',
            lambda x, mod=i: x.get_module_offset(mod),
            lambda x, val, mod=i: x.set_module_offset(mod, val)))

class AttocubeANC300Config(DeviceConfig):

    class AttocubeANM300Panel(ControlPanel):
        def __init__(self, parent, device, channel):
            super().__init__(parent, 'Channel: ' + str(channel), wx.VERTICAL)
            self.channel_num = channel
            self.device = device.modules[channel-1]

            self.controls = [
                ControlField(
                    CaptionDropBox(self, 'Mode', self.device.modes),
                    self.device.get_mode, self.device.set_mode),
                ControlField(
                    ModifiedCheckBox(self, 'DC-IN'),
                    self.device.get_dc_in, self.device.set_dc_in),
                ControlField(
                    CaptionDropBox(self, 'Filter', self.device.filters),
                    self.device.get_filter, self.device.set_filter),
                ControlField(
                    CaptionTextPanel(self, 'Step frequency, Hz'),
                    self.device.get_step_freq, self.device.set_step_freq),
                ControlField(
                    CaptionTextPanel(self, 'Step voltage, V'),
                    self.device.get_step_volt, self.device.set_step_volt),
                ControlField(
                    CaptionTextPanel(self, 'Offset voltage, V'),
                    self.device.get_offset_volt, self.device.set_offset_volt),
                ControlField(
                    CaptionTextPanel(self, 'Capacitance, nF'),
                    self.device.get_capacitance, None),
                ControlField(
                    CaptionTextPanel(self, 'Output voltage, V'),
                    self.device.get_output, None),
                ControlField(
                    CaptionTextPanel(self, 'Steps'),
                    self.device.get_steps, self.device.set_steps),
            ]

            self.btn_forward = wx.Button(self, label='Forward')
            self.Bind(wx.EVT_BUTTON, self.on_btn_forward, self.btn_forward)
            self.btn_backward = wx.Button(self, label='Backward')
            self.Bind(wx.EVT_BUTTON, self.on_btn_backward, self.btn_backward)
            self.steps_to_move = CaptionTextPanel(self, 'Steps to move')
            self.steps_to_move.SetValue('1')

            for control in self.controls:
                self.sizer.Add(control.control, flag=wx.ALL | wx.GROW)
            self.sizer.Add(self.btn_forward, flag=wx.ALL | wx.GROW)
            self.sizer.Add(self.btn_backward, flag=wx.ALL | wx.GROW)
            self.sizer.Add(self.steps_to_move, flag=wx.ALL | wx.GROW)
            self.SetSizer(self.sizer)
            self.sizer.Fit(self)

        def on_btn_forward(self, event):
            del event
            if int(self.steps_to_move.GetValue()) < 0:
                return
            self.device.step_forward(self.steps_to_move.GetValue())
            self.read_control()

        def on_btn_backward(self, event):
            del event
            if int(self.steps_to_move.GetValue()) < 0:
                return
            self.device.step_backward(self.steps_to_move.GetValue())
            self.read_control()

    def _create_controls(self):
        self.controls_fields = [
            self.AttocubeANM300Panel(self.panel, self.device, i) for i in self.device.ACTIVE_MODULES
            ]
        self.controls = self.controls_fields
        self.columns = len(self.controls_fields)
