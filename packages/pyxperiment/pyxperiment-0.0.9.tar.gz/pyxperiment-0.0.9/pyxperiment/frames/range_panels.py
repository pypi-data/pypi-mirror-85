"""
    frames/range_panels.py: This module declares the frames for experiment
    range selection

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

from pyxperiment.settings.group_settings import DeviceSetting, DevicePropertySettings
from pyxperiment.settings.view_settings import ViewSettings
from pyxperiment.core.utils import str_to_range
from pyxperiment.controller.device_options import DeviceOption
from .basic_panels import BoxedTextPanel
from .plots.simple_plot import SimpleAxisPanel

class SweepPanel(wx.Panel):
    """
    A base class for all sweep panels
    """

    def __init__(self, parent, device):
        wx.Panel.__init__(self, parent)
        self.device = device

    def can_backsweep(self):
        """
        Return if the device can sweep in opposide direction
        """
        return not self.device.driver_name() == 'Time'

    def reload(self):
        """
        Resets the panel
        """

    def new_device_settings(self):
        """
        Populate new DeviceSetting struct with current device
        """
        device_settings = DeviceSetting()
        device_settings.name = self.device.device_name()
        device_settings.address = self.device.location
        device_settings.driverName = self.device.driver_name()
        device_settings.serial = self.device.device_id()
        return device_settings

    def find_sweep_settings(self, settings):
        """
        Find the corresponding sweep settings from device or property
        """
        device_settings = settings.find_device_settings(
            self.device.location,
            self.device.driver_name())
        if device_settings is None:
            return None
        if not isinstance(self.device, DeviceOption):
            return device_settings
        return next(filter(
            lambda x: x.name == self.device.name,
            device_settings.properties.get_children()), None)

    def save_sweep_settings(self, settings, sweep_range, delay, return_delay):
        """
        Save the sweep settings to respective device or property
        """
        device_settings = settings.find_device_settings(
            self.device.location,
            self.device.driver_name())
        if device_settings is None:
            device_settings = self.new_device_settings()
            settings.add_child(device_settings)
        if not isinstance(self.device, DeviceOption):
            device_settings.sweep.range = sweep_range
            device_settings.sweep.delay = delay
            device_settings.sweep.returnDelay = return_delay
            return
        device_property = next(filter(
            lambda x: x.name == self.device.name,
            device_settings.properties.get_children()), None)
        if device_property is None:
            device_property = DevicePropertySettings()
            device_property.name = self.device.name
            device_settings.properties.add_child(device_property)
        device_property.sweep.range = sweep_range
        device_property.sweep.delay = delay
        device_property.sweep.returnDelay = return_delay

class TimeSweepPanel(SweepPanel):
    """
    A special class for time sweep panel
    """

    def __init__(self, parent, device, settings):
        SweepPanel.__init__(self, parent, device)
        self.vbox = wx.BoxSizer(wx.VERTICAL)

        self.edit_numpoints = BoxedTextPanel(self, 'Num points', size=(240, -1))
        self.edit_numpoints.edit.SetFont(ViewSettings().RANGE_EDIT_FONT)
        self.vbox.Add(self.edit_numpoints, flag=wx.ALIGN_CENTRE_HORIZONTAL)

        self.edit_delay = BoxedTextPanel(self, 'Delay, ms', size=(120, -1))
        self.edit_delay.edit.SetFont(ViewSettings().RANGE_EDIT_FONT)
        self.vbox.Add(self.edit_delay, border=5, flag=wx.ALL | wx.ALIGN_CENTRE_HORIZONTAL)

        device_settings = self.find_sweep_settings(settings)
        if device_settings is None:
            device_settings = self.new_device_settings()
            device_settings.sweep.range = '100'
            device_settings.sweep.delay = '250'
            device_settings.sweep.returnDelay = '0.1'

        self.edit_numpoints.SetValue(device_settings.sweep.range)
        self.edit_delay.SetValue(device_settings.sweep.delay)

        self.SetSizer(self.vbox)
        self.vbox.Fit(self)

    def saveSettings(self, settings):
        self.save_sweep_settings(
            settings, self.edit_numpoints.GetValue(), self.edit_delay.GetValue(), '0.1'
        )

    def GetRange(self):
        delay = int(self.edit_delay.GetValue())
        return [(delay * x / 1000.0) for x in range(0, int(self.edit_numpoints.GetValue()))]

    def description(self):
        ret = self.device.description()
        ret.append(('Num points', self.edit_numpoints.GetValue()))
        ret.append(('Delay', self.edit_delay.GetValue()))
        return ret

class FieldSweepPanel(SweepPanel):
    """
    A special class for the device with automated sweep (Field, Temperature)
    """

    def __init__(self, parent, device, settings):
        super().__init__(parent, device)
        self.vbox = wx.BoxSizer(wx.VERTICAL)

        self.edit_value = BoxedTextPanel(
            self, 'Value', size=(240, -1), show_mod=True, style=wx.TE_PROCESS_ENTER)
        self.edit_value.edit.SetFont(ViewSettings().RANGE_EDIT_FONT)
        self.edit_value.edit.SetEditable(False)
        self.vbox.Add(self.edit_value, flag=wx.ALIGN_CENTRE_HORIZONTAL)

        self.edit_target = BoxedTextPanel(self, 'Target Value', size=(240, -1))
        self.edit_target.edit.SetFont(ViewSettings().RANGE_EDIT_FONT)
        self.vbox.Add(self.edit_target, flag=wx.ALIGN_CENTRE_HORIZONTAL)

        self.edit_delay = BoxedTextPanel(self, 'Delay, ms', size=(120, -1))
        self.edit_delay.edit.SetFont(ViewSettings().RANGE_EDIT_FONT)
        self.vbox.Add(self.edit_delay, border=5, flag=wx.ALL | wx.ALIGN_CENTRE_HORIZONTAL)

        device_settings = self.find_sweep_settings(settings)
        if device_settings is None:
            device_settings = self.new_device_settings()
            device_settings.sweep.range = self.device.get_target_field()
            device_settings.sweep.delay = '250'
            device_settings.sweep.returnDelay = '0.1'

        self.edit_target.SetValue(device_settings.sweep.range)
        self.edit_delay.SetValue(device_settings.sweep.delay)

        self.SetSizer(self.vbox)
        self.vbox.Fit(self)
        self.reload()

    def saveSettings(self, settings):
        self.save_sweep_settings(
            settings, self.edit_target.GetValue(), self.edit_delay.GetValue(), '0.1'
        )

    def reload(self):
        self.edit_value.SetValue(self.device.get_target_field())
        self.device.to_local()

    def GetRange(self):
        return [self.edit_value.GetValue(), self.edit_target.GetValue()]

    def description(self):
        ret = self.device.description()
        ret.append(('Start', self.edit_value.GetValue()))
        ret.append(('Target', self.edit_target.GetValue()))
        ret.append(('Delay', self.edit_delay.GetValue()))
        return ret

class DeviceSweepPanel(SweepPanel):
    def __init__(self, parent, device, settings, show_compiled=True):
        super().__init__(parent, device)
        self.show_compiled = show_compiled
        self.vbox = wx.BoxSizer(wx.VERTICAL)
        self.edit_value = BoxedTextPanel(self, 'Value', size=(240, -1), show_mod=True, style=wx.TE_PROCESS_ENTER)
        self.edit_value.edit.SetFont(ViewSettings().RANGE_EDIT_FONT)
        self.Bind(wx.EVT_TEXT_ENTER, self.OnEditValue, self.edit_value.edit)
        self.vbox.Add(self.edit_value, flag=wx.ALIGN_CENTRE_HORIZONTAL)

        self.edit_range = BoxedTextPanel(self, 'Range', size=(240, -1))
        self.edit_range.edit.SetFont(ViewSettings().RANGE_EDIT_FONT)
        self.Bind(wx.EVT_TEXT, self.OnEditRange, self.edit_range.edit)
        self.vbox.Add(self.edit_range, flag=wx.ALIGN_CENTRE_HORIZONTAL)

        if self.show_compiled:
            self.edit_range_compiled = BoxedTextPanel(self, 'Compiled range', size=(240, 60), style=wx.TE_MULTILINE)
            self.vbox.Add(self.edit_range_compiled, proportion=0.5, flag=wx.GROW)
            self.edit_range_compiled.edit.SetEditable(False)
            self.axis_range = SimpleAxisPanel(self)
            self.vbox.Add(self.axis_range, proportion=1, flag=wx.GROW)

        self.edit_delay = BoxedTextPanel(self, 'Delay, ms', size=(120, -1))
        self.edit_delay.edit.SetFont(ViewSettings().RANGE_EDIT_FONT)
        self.vbox.Add(self.edit_delay, border=5, flag=wx.ALL | wx.ALIGN_CENTRE_HORIZONTAL)

        device_settings = self.find_sweep_settings(settings)
        if device_settings is None:
            device_settings = self.new_device_settings()
            device_settings.sweep.range = self.device.get_value()
            device_settings.sweep.delay = '250'
            device_settings.sweep.returnDelay = '0.1'

        self.range = []
        self.edit_range.SetValue(device_settings.sweep.range)
        self.edit_delay.SetValue(device_settings.sweep.delay)

        self.SetSizer(self.vbox)
        self.vbox.Fit(self)
        self.reload()

    def saveSettings(self, settings):
        self.save_sweep_settings(
            settings, self.edit_range.GetValue(), self.edit_delay.GetValue(), '0.1'
        )

    def reload(self):
        self.edit_value.SetValue(str(Decimal(self.device.get_value())))
        self.device.to_local()

    def OnEditValue(self, event):
        del event
        if self.edit_value.IsModified():
            self.device.set_value(self.edit_value.GetValue())
        self.edit_value.SetValue(str(Decimal(self.device.get_value())))

    def OnEditRange(self, event):
        del event
        if self.show_compiled:
            self.edit_range_compiled.edit.Value = ''
        self.range = []
        try:
            self.range = str_to_range(self.edit_range.edit.Value)
            if self.show_compiled:
                self.axis_range.plot(range(len(self.range)), [float(el) for el in self.range])
                self.edit_range_compiled.edit.Value = ', '.join([str(el) for el in self.range])
        except:
            pass

    def GetRange(self):
        return list(self.range)

    def description(self):
        ret = self.device.description()
        ret.append(('Range', self.edit_range.GetValue()))
        ret.append(('Delay', self.edit_delay.GetValue()))
        return ret
