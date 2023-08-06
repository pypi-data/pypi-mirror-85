"""
    pyxperiment/frames/device_select_panel.py:
    The panel for selecting experimental devices

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

import wx
import pyvisa

from pyxperiment.settings.view_settings import ViewSettings
from pyxperiment.controller.time_device import TimeDevice

class DeviceSelectPanel(wx.Panel):
    """
    The panel for selecting experimental devices
    """

    NONE_DEVICE = 'None'

    def __init__(self, parent, res_manager, is_readable, name=''):
        super().__init__(parent, wx.ID_ANY)
        self.res_manager = res_manager
        self.is_readable = is_readable
        text_name = wx.StaticText(self, label=name)
        text_name.SetFont(ViewSettings().BUTTON_FONT)

        self.dropbox_device = wx.ComboBox(self, style=wx.CB_READONLY)
        self.dropbox_device.SetFont(ViewSettings().MAIN_FONT)

        self.dropbox_parameter = wx.ComboBox(self, style=wx.CB_READONLY)
        self.dropbox_parameter.SetFont(ViewSettings().MAIN_FONT)
        self.dropbox_parameter.Disable()

        self.dropbox_driver = wx.ComboBox(self, style=wx.CB_READONLY)
        self.dropbox_driver.SetFont(ViewSettings().MAIN_FONT)
        self.dropbox_driver.Disable()
        for driver in self.res_manager.list_drivers():
            self.dropbox_driver.Append(driver.driver_name(), driver)

        self.button_configure = wx.Button(self, -1, 'Configure')
        self.button_configure.SetFont(ViewSettings().BUTTON_FONT)
        self.Bind(wx.EVT_BUTTON, self._on_configure, self.button_configure)

        self.Bind(wx.EVT_COMBOBOX, self._on_device_change, self.dropbox_device)
        self._on_device_change(None)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(text_name, 0, wx.ALIGN_CENTRE)
        self.sizer.Add(self.dropbox_device, 0, wx.ALL | wx.GROW)
        self.sizer.Add(self.dropbox_driver, 0, wx.TOP | wx.BOTTOM | wx.GROW, 20)
        self.sizer.Add(self.dropbox_parameter, 0, wx.BOTTOM | wx.GROW, 20)
        self.sizer.Add(self.button_configure, 0, wx.ALL | wx.ALIGN_RIGHT)
        self.SetSizer(self.sizer)
        self.sizer.Fit(self)

    def set_devices_list(self, devices):
        """
        Set the devices list avialiable in this panel
        """
        #value = self.dropbox_device.GetSelection()
        self.dropbox_device.Clear()
        for device in devices:
            if device[1] is None:
                self.dropbox_device.Append(DeviceSelectPanel.NONE_DEVICE, device)
            elif device[1] == TimeDevice:
                self.dropbox_device.Append(TimeDevice.driver_name(), device)
            else:
                self.dropbox_device.Append(device[0].address, device)
        self.dropbox_device.Select(0)
        self._on_device_change(None)

    def _on_device_change(self, event):
        del event
        value = self.dropbox_device.GetSelection()
        if value < 0:
            return
        device_class = self.dropbox_device.GetClientData(value)[1]
        if (device_class is None or device_class == TimeDevice):
            self.button_configure.Disable()
            self.dropbox_parameter.Disable()
            self.dropbox_parameter.Clear()
            self.dropbox_driver.Select(-1)
            return
        element = self.dropbox_driver.FindString(device_class.driver_name())
        self.dropbox_driver.Select(element)

        self.button_configure.Enable()
        properties = (
            device_class.get_readable_properties()
            if self.is_readable
            else device_class.get_writable_properties()
            )
        if properties:
            self.dropbox_parameter.Clear()
            self.dropbox_parameter.Enable()
            for prop in properties:
                self.dropbox_parameter.Append(prop.name, prop)
            self.dropbox_parameter.Select(0)
        else:
            self.dropbox_parameter.Disable()
            self.dropbox_parameter.Clear()

    def _on_configure(self, event):
        del event
        try:
            device = self.get_device(True)
        except (pyvisa.errors.VisaIOError) as err:
            wx.MessageBox(err.description)
            return
        except OSError as err:
            # TODO: get better descriptions
            wx.MessageBox(str(err))
            return
        if device == DeviceSelectPanel.NONE_DEVICE:
            return
        config = device.get_config_class()
        config_frame = config(self.Parent, device)
        config_frame.Show()

    def get_device(self, no_param=False):
        value = self.dropbox_device.GetSelection()
        if value < 0:
            return DeviceSelectPanel.NONE_DEVICE
        device_control = self.dropbox_device.GetClientData(value)
        if device_control[1] is None:
            return DeviceSelectPanel.NONE_DEVICE
        if device_control[1] == TimeDevice:
            return device_control[1]()
        ret = self.res_manager.open_visa_device(device_control[1], device_control[0].address)
        if self.dropbox_parameter.Items and not no_param:
            param = self.dropbox_parameter.GetClientData(self.dropbox_parameter.GetSelection())
            return param.with_instance(ret)
        return ret
