"""
    pyxperiment/frames/experiment_setup_frame.py: The frame for experiment setup

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

import os
import wx
import pyvisa

from pyxperiment.settings.core_settings import CoreSettings
from pyxperiment.settings.view_settings import ViewSettings

from pyxperiment.controller.time_device import TimeDevice

from pyxperiment.data_format.text_data_format import TextDataWriter
from .device_library_frame import DeviceLibraryFrame
from .device_select_panel import DeviceSelectPanel
from .range_select_frame import RangeSelectFrame

class ExperimentSetupFrame(wx.Frame):
    """
    Experiment setup window
    """

    def __init__(self, res_manager, readers, writers):
        wx.Frame.__init__(self, None, -1, 'Experiment setup')
        self.panel = wx.Panel(self)
        self.res_manager = res_manager

        self.reader_panels = []
        for reader in range(readers):
            panel = DeviceSelectPanel(
                self.panel, self.res_manager,
                True, name="Y-device " + str(reader+1) + ":"
                )
            self.reader_panels.append(panel)

        self.writer_panels = []
        for writer in range(writers):
            panel = DeviceSelectPanel(
                self.panel, self.res_manager,
                False, name="X-device:" if writer == 0 else "X-device slow:"
                )
            self.writer_panels.append(panel)
        self.update_devices()

        text_label = wx.StaticText(self.panel, label='Device selection')
        text_label.SetFont(ViewSettings().HEADER_FONT)

        text_path = wx.StaticText(self.panel, label='Path to save data files:')
        text_path.SetFont(ViewSettings().BUTTON_FONT)
        self.edit_path = wx.TextCtrl(self.panel, -1, size=(35, -1), value=str(CoreSettings.get_last_path()))
        self.edit_path.SetFont(ViewSettings().MAIN_FONT)
        self.button_select_path = wx.Button(self.panel, label='Select')
        self.button_select_path.SetFont(ViewSettings().MAIN_FONT)
        self.Bind(wx.EVT_BUTTON, self.on_select_path, self.button_select_path)

        self.btn_start = wx.Button(self.panel, label='Start', size=(-1, 35))
        self.btn_start.SetFont(ViewSettings().BUTTON_FONT)
        self.Bind(wx.EVT_BUTTON, self.on_start_button, self.btn_start)
        self.btn_exit = wx.Button(self.panel, label='Exit', size=(-1, 35))
        self.btn_exit.SetFont(ViewSettings().BUTTON_FONT)
        self.Bind(wx.EVT_BUTTON, self.on_close, self.btn_exit)
        self.btn_library = wx.Button(self.panel, label='Devices', size=(-1, 35))
        self.btn_library.SetFont(ViewSettings().BUTTON_FONT)
        self.Bind(wx.EVT_BUTTON, self.on_library_button, self.btn_library)

        self.hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        self.hbox1.AddSpacer(20)
        for panel in self.reader_panels:
            self.hbox1.Add(panel, 1, flag=wx.GROW)
            self.hbox1.AddSpacer(20)

        self.hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        self.hbox2.AddSpacer(20)
        for panel in self.writer_panels:
            self.hbox2.Add(panel, 1, flag=wx.GROW)
            self.hbox2.AddSpacer(20)

        self.hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        self.hbox3.Add(self.btn_start, 1, border=20, flag=wx.GROW|wx.LEFT|wx.RIGHT)
        self.hbox3.Add(self.btn_exit, 1, border=20, flag=wx.GROW|wx.LEFT|wx.RIGHT)
        self.hbox3.Add(self.btn_library, 1, border=20, flag=wx.GROW|wx.LEFT|wx.RIGHT)

        self.hbox4 = wx.BoxSizer(wx.HORIZONTAL)
        self.hbox4.AddSpacer(20)
        self.hbox4.Add(self.edit_path, 1)
        self.hbox4.AddSpacer(20)
        self.hbox4.Add(self.button_select_path, 0)
        self.hbox4.AddSpacer(20)

        self.vbox = wx.BoxSizer(wx.VERTICAL)
        self.vbox.AddSpacer(10)
        self.vbox.Add(text_label, 0, flag=wx.ALIGN_CENTRE_HORIZONTAL)
        self.vbox.AddSpacer(20)
        self.vbox.Add(self.hbox1, 1, flag=wx.GROW)
        self.vbox.AddSpacer(50)
        self.vbox.Add(self.hbox2, 1, flag=wx.GROW)
        self.vbox.AddSpacer(50)
        self.vbox.Add(text_path, 0, flag=wx.ALIGN_CENTRE_HORIZONTAL)
        self.vbox.Add(self.hbox4, 0, flag=wx.TOP | wx.GROW)
        self.vbox.AddSpacer(10)
        self.vbox.Add(self.hbox3, 0, flag=wx.TOP | wx.GROW)
        self.vbox.AddSpacer(10)

        self.panel.SetSizer(self.vbox)
        self.vbox.Fit(self)
        self.Center()
        self.Bind(wx.EVT_CLOSE, self.on_close)

    def update_devices(self):
        saved_resources = list(filter(
            lambda x: x.driverName != 'Time',
            CoreSettings.get_device_settings().get_children()
        ))
        drivers = self.res_manager.list_drivers()
        saved_resources = [
            (setting, next(x for x in drivers if x.driver_name() == setting.driverName))
            for setting in saved_resources
            ]
        readable_devices = list(filter(lambda x: x[1].is_readable(), saved_resources))
        writable_devices = list(filter(lambda x: x[1].is_writable(), saved_resources))
        for reader in range(len(self.reader_panels)):
            self.reader_panels[reader].set_devices_list(
                ([(None, None)] if reader > 0 else []) + readable_devices
            )
        for writer in range(len(self.writer_panels)):
            self.writer_panels[writer].set_devices_list(
                ([(None, None)] if writer > 0 else [(None, TimeDevice)]) + writable_devices
            )

    def on_select_path(self, event):
        del event
        dlg = wx.FileDialog(self, "Select path for data files...", os.getcwd(), "", "*.dat",
                            wx.FD_SAVE)
        result = dlg.ShowModal()
        if result == wx.ID_OK:
            self.edit_path.Value = dlg.GetPath()
            CoreSettings.set_last_path(self.edit_path.Value)
        dlg.Destroy()

    def on_start_button(self, event):
        del event
        writer = TextDataWriter(self.edit_path.Value)
        CoreSettings.set_last_path(self.edit_path.Value)
        try:
            selectRange = RangeSelectFrame(
                self, writer,
                list(filter(lambda x: x != 'None', [panel.get_device() for panel in self.reader_panels])),
                list(filter(lambda x: x != 'None', [panel.get_device() for panel in self.writer_panels])))
        except (pyvisa.errors.VisaIOError) as err:
            wx.MessageBox(err.description)
            return
        selectRange.Show()

    def on_library_button(self, event):
        del event
        libraryframe = DeviceLibraryFrame(self, self.res_manager)
        libraryframe.Show()

    def on_experiment_closed(self, event):
        del event
        self.Enable()

    def on_close(self, event):
        del event
        self.Destroy()
