"""
    pyxperiment/frames/device_library_frame.py:
    The special window for manipulating saved devices list

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
import wx.dataview
import pyvisa

from pyxperiment.settings.core_settings import CoreSettings
from pyxperiment.settings.group_settings import DeviceSetting
from pyxperiment.settings.view_settings import ViewSettings
from .device_add_panel import DeviceAddPanel

class DeviceLibraryFrame(wx.Frame):
    """
    The special window for manipulating saved devices list
    """

    def __init__(self, parent, res_manager):
        super().__init__(parent, wx.ID_ANY, 'Device library')
        self.parent = parent
        self.panel = wx.Panel(self)
        self.res_manager = res_manager

        self.viewlist_devices = wx.dataview.DataViewListCtrl(
            self.panel,
            wx.ID_ANY,
            size=(800, 300),
            style=wx.dataview.DV_HORIZ_RULES|wx.dataview.DV_VERT_RULES
            )
        column = self.viewlist_devices.AppendTextColumn("VISA address")
        column.SetWidth(200)
        column = self.viewlist_devices.AppendTextColumn("Driver")
        column.SetWidth(280)
        column = self.viewlist_devices.AppendTextColumn("Model")
        column.SetWidth(300)
        column = self.viewlist_devices.AppendTextColumn("Serial")
        column.SetWidth(80)
        self.add_device_panel = DeviceAddPanel(self.panel, self.res_manager)
        self.button_add = wx.Button(self.panel, wx.ID_ANY, "Add", size=(100, 35))
        self.button_add.SetFont(ViewSettings().BUTTON_FONT)
        self.button_configure = wx.Button(self.panel, wx.ID_ANY, "Configure", size=(100, 35))
        self.button_configure.SetFont(ViewSettings().BUTTON_FONT)
        self.button_remove = wx.Button(self.panel, wx.ID_ANY, "Remove", size=(100, 35))
        self.button_remove.SetFont(ViewSettings().BUTTON_FONT)

        self.vbox = wx.BoxSizer(wx.VERTICAL)
        self.hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.hbox.Add(self.button_add, 1, wx.ALL|wx.GROW, 10)
        self.hbox.Add(self.button_configure, 1, wx.ALL|wx.GROW, 10)
        self.hbox.Add(self.button_remove, 1, wx.ALL|wx.GROW, 10)
        self.vbox.Add(self.viewlist_devices, 1, wx.ALL|wx.GROW, 10)
        self.vbox.Add(self.add_device_panel, 0, wx.ALL|wx.GROW, 10)
        self.vbox.Add(self.hbox, 0, wx.ALL|wx.GROW, 10)
        self.panel.SetSizer(self.vbox)
        self.vbox.Fit(self)

        self.Bind(wx.EVT_BUTTON, self._on_add_device, self.button_add)
        self.Bind(wx.EVT_BUTTON, self._on_configure, self.button_configure)
        self.Bind(wx.EVT_BUTTON, self._on_button_remove_click, self.button_remove)
        self.Bind(wx.dataview.EVT_DATAVIEW_SELECTION_CHANGED, self._on_selection,
            self.viewlist_devices)

        self._reload_devices()

    def _save_device_settings(self, device):
        settings = CoreSettings.get_device_settings()
        if settings.find_device_settings(device.location, device.driver_name()) is None:
            device_settings = DeviceSetting()
            device_settings.name = device.device_name()
            device_settings.address = device.location
            device_settings.driverName = device.driver_name()
            device_settings.serial = device.device_id()
            settings.add_child(device_settings)
        CoreSettings.set_device_settings(settings)

    def _on_add_device(self, event):
        del event
        try:
            device = self.add_device_panel.get_device()
        except (pyvisa.errors.VisaIOError) as err:
            wx.MessageBox(err.description)
            return
        self._save_device_settings(device)
        self._reload_devices()
        self.parent.update_devices()

    def _on_selection(self, event):
        del event
        device_settings = CoreSettings.get_device_settings()
        selected = self.viewlist_devices.GetSelectedRow()
        if selected != wx.NOT_FOUND:
            setting = device_settings.find_device_settings(
                self.viewlist_devices.GetTextValue(selected, 0),
                self.viewlist_devices.GetTextValue(selected, 1)
                )
            self.add_device_panel.set_resource(setting.address)
            self.add_device_panel.set_driver(setting.driverName)

    def _on_configure(self, event):
        del event
        try:
            device = self.add_device_panel.get_device()
        except (pyvisa.errors.VisaIOError) as err:
            wx.MessageBox(err.description)
            return
        self._save_device_settings(device)
        config = device.get_config_class()
        config_frame = config(self.Parent, device)
        config_frame.Show()
        self._reload_devices()
        self.parent.update_devices()

    def _reload_devices(self):
        self.viewlist_devices.DeleteAllItems()
        device_settings = CoreSettings.get_device_settings()
        for setting in device_settings.get_children():
            if setting.driverName != 'Time':
                self.viewlist_devices.AppendItem(
                    [setting.address if setting.address is not None else '', setting.driverName, setting.name, setting.serial]
                    )

    def _on_button_remove_click(self, event):
        del event
        device_settings = CoreSettings.get_device_settings()
        selected = self.viewlist_devices.GetSelectedRow()
        if selected != wx.NOT_FOUND:
            setting = device_settings.find_device_settings(
                self.viewlist_devices.GetTextValue(selected, 0),
                self.viewlist_devices.GetTextValue(selected, 1)
                )
            if setting is not None:
                device_settings.remove_child(setting)
                CoreSettings.set_device_settings(device_settings)
        self._reload_devices()
        self.parent.update_devices()
        