"""
    pyxperiment/frames/device_config.py:
    The class defining base functions for device configuration dialogs

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
import wx

from pyxperiment.controller.device_options import (
    ListDeviceOption, BooleanDeviceOption, ValueDeviceOption, StateDeviceOption
)
from pyxperiment.settings.view_settings import ViewSettings
from .basic_panels import (
    CaptionTextPanel, CaptionDropBox, ModifiedCheckBox
)

def option_to_control(panel, option):
    if isinstance(option, ListDeviceOption):
        return ControlField(CaptionDropBox(panel, option.name, option.values_list()),
                            option.get_value, option.set_value, option)
    if isinstance(option, BooleanDeviceOption):
        return ControlField(ModifiedCheckBox(panel, option.name),
                            option.get_value, option.set_value, option)
    if isinstance(option, ValueDeviceOption):
        panel = CaptionTextPanel(
            panel,
            option.name + ((', ' + option.phys_quantity()) if option.phys_quantity() else ''),
            show_mod=True
            )
        return ControlField(panel,
                            option.get_value,
                            None if option.is_readable() else option.set_value, option)
    if isinstance(option, StateDeviceOption):
        return ControlField(CaptionTextPanel(panel, option.name),
                            option.get_value, None, option)
    return None

class ControlField(object):
    def __init__(self, control, getf, setf, option=None):
        self.control = control
        self.setf = setf
        self.getf = getf
        self.option = option
        self.read_timeout = 0
        if self.setf is None:
            self.control.SetEnabled(False)

    def read_control(self):
        start_time = time.perf_counter()
        value = self.getf()
        end_time = time.perf_counter()
        if not isinstance(value, list):
            self.control.SetValue(value)
        else:
            self.control.SetValue(', '.join(value))
        if self.option is not None and hasattr(self.option, 'read_timeout'):
            self.option.read_timeout.value = end_time - start_time
        if self.setf is not None and self.option is not None:
            self.control.SetEnabled(self.option.is_enabled())

    def write_control(self):
        if self.setf is not None and self.control.IsModified():
            self.setf(self.control.GetValue())

class ControlPanel(wx.Panel):
    def __init__(self, parent, name, orientation):
        super().__init__(parent)
        self.controls = []
        self.sizer = wx.BoxSizer(orientation)
        if name is not None:
            self.sizer.Add(wx.StaticText(self, label=name), 0, wx.ALL | wx.ALIGN_CENTER, 10)

    def set_controls(self, controls):
        self.controls = controls
        self.fit_control()

    def fit_control(self):
        for control in self.controls:
            self.sizer.Add(control.control, 0, wx.ALL | wx.GROW, 2)
        self.SetSizer(self.sizer)
        self.sizer.Fit(self)

    def read_control(self):
        for control in self.controls:
            control.read_control()

    def write_control(self):
        for control in self.controls:
            control.write_control()

    @property
    def control(self):
        return self

class MultiControlPanel(ControlPanel):
    def __init__(self, parent, name, get_func, set_func, orientation):
        super().__init__(parent, name, orientation)
        self.get_func = get_func
        self.set_func = set_func

    def fit_control(self):
        for control in self.controls:
            self.sizer.Add(control, 0, wx.ALL | wx.GROW, 5)
            self.SetSizer(self.sizer)
            self.sizer.Fit(self)

    def read_control(self):
        values = self.get_func()
        for i, value in enumerate(values):
            self.controls[i].SetValue(value)

    def write_control(self):
        if any(map(lambda x: x.IsModified(), self.controls)):
            values = [x.GetValue() for x in self.controls]
            self.set_func(values)

class DeviceConfig(wx.Frame):
    def __init__(self, parent, device, reload_speed=100):
        super().__init__(parent, -1, device.driver_name() + ' config',
                         style=wx.DEFAULT_FRAME_STYLE & (~(wx.RESIZE_BORDER|wx.MAXIMIZE_BOX)))
        self.device = device
        self.timer_controls = []
        self.controls_fields = []

        self._init_view()
        self.read_control()

        self.reload_timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.on_reload_timer, self.reload_timer)
        self.reload_timer.Start(reload_speed)
        self.Bind(wx.EVT_CLOSE, self._on_close)

    def _create_panel(self):
        self.panel = wx.Panel(self)
        self.name = wx.StaticText(self.panel, label=self.device.device_name())
        self.name.SetFont(ViewSettings().TITLE_FONT)
        self.location = wx.StaticText(self.panel, label=self.device.location)
        self.location.SetFont(ViewSettings().EDIT_FONT)

        self.btn_save = wx.Button(self.panel, label='Save')
        self.Bind(wx.EVT_BUTTON, self.on_save_button, self.btn_save)
        self.btn_load = wx.Button(self.panel, label='Load')
        self.Bind(wx.EVT_BUTTON, self.on_load_button, self.btn_load)

    def _init_view(self):
        self._create_panel()
        self.columns = 2
        self.controls = []
        self._create_controls()

        self.vbox = wx.BoxSizer(wx.VERTICAL)
        self.vbox.Add(self.name, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 10)
        self.vbox.Add(self.location, 0, wx.ALIGN_CENTER_HORIZONTAL, 0)

        for i in range(0, len(self.controls), self.columns):
            hbox = wx.BoxSizer(wx.HORIZONTAL)
            for j in range(self.columns):
                if i+j < len(self.controls):
                    hbox.Add(self.controls[i+j], 1, wx.GROW | wx.ALL, 2)
            self.vbox.Add(hbox, 0, wx.GROW | wx.LEFT | wx.RIGHT, 10)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(self.btn_save, 0, border=10, flag=wx.ALL)
        hbox.Add(self.btn_load, 0, border=10, flag=wx.ALL)
        self.vbox.Add(hbox, 0, wx.ALIGN_CENTER_HORIZONTAL)
        self.panel.SetSizer(self.vbox)
        self.vbox.Fit(self)

    def _on_close(self, _):
        self.reload_timer.Stop()
        self.Destroy()
        self.device.to_local()

    def on_save_button(self, _):
        self.write_control()
        self.read_control()
        self.Refresh()

    def on_load_button(self, _):
        self.read_control()
        self.Refresh()

    def _create_controls(self):
        for option in self.device.get_options():
            control = option_to_control(self.panel, option)
            if option.is_readable():
                self.timer_controls.append(control)
            else:
                self.controls_fields.append(control)
            self.controls.append(control.control)

    def read_control(self):
        for control in self.controls_fields:
            control.read_control()

    def write_control(self):
        for control in self.controls_fields:
            control.write_control()

    def on_reload_timer(self, event):
        del event
        for control in self.timer_controls:
            control.read_control()
