"""
    frames/device_add_panel.py: The panel for adding new devices

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

from pyxperiment.settings.view_settings import ViewSettings

class DeviceAddPanel(wx.Panel):
    """
    The panel for adding new devices
    """

    def __init__(self, parent, res_manager):
        super().__init__(parent, wx.ID_ANY)

        self.res_manager = res_manager
        text_name = wx.StaticText(self, label='Add new device')
        text_name.SetFont(ViewSettings().BUTTON_FONT)

        self.dropbox_device = wx.ComboBox(self, style=wx.CB_READONLY)
        for driver in self.res_manager.list_drivers():
            self.dropbox_device.Append(driver.driver_name(), driver)
        self.dropbox_device.Select(0)
        self.dropbox_device.SetFont(ViewSettings().MAIN_FONT)

        self.dropbox_resource = wx.ComboBox(self, style=wx.CB_DROPDOWN)
        self.dropbox_resource.SetFont(ViewSettings().MAIN_FONT)
        for resource in self.res_manager.list_resources():
            self.dropbox_resource.Append(resource, resource)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(text_name, 0, wx.ALIGN_CENTRE)
        self.sizer.Add(self.dropbox_device, 0, wx.GROW)
        self.sizer.Add(self.dropbox_resource, 0, wx.TOP | wx.GROW, 20)
        self.SetSizer(self.sizer)
        self.sizer.Fit(self)

    def get_device(self):
        """
        Return the device, specified by selected resource and driver
        """
        value = self.dropbox_device.GetSelection()
        device_control = self.dropbox_device.GetClientData(value)
        resource = self.dropbox_resource.GetValue()
        match = re.match(r"^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3}):(\d{1,5})$", resource)
        if match:
            resource = "TCPIP0::"+match.group(1)+'.'+match.group(2) +'.'+match.group(3)+'.'+match.group(4)+"::"+match.group(5)+"::SOCKET"
        ret = self.res_manager.open_visa_device(device_control, resource)
        return ret

    def set_resource(self, value):
        self.dropbox_resource.SetValue(value)

    def set_driver(self, value):
        for i in range(self.dropbox_device.GetCount()):
            if self.dropbox_device.GetString(i) == value:
                self.dropbox_device.SetSelection(i)
