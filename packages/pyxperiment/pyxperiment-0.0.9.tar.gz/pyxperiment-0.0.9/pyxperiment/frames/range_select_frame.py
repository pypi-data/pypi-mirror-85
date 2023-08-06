"""
    pyxperiment/frames/range_select_frame.py:
    The frame for experiment range selection

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

from pyxperiment.controller import data_context
from pyxperiment.data_format.text_data_format import TextDataWriter
from pyxperiment.data_format.columned_data_format import ColumnedDataWriter
from pyxperiment.settings.core_settings import CoreSettings
from pyxperiment.settings.view_settings import ViewSettings

from .basic_panels import BoxedTextPanel, CaptionDropBox
from .experiment_control_frame import ExperimentControlFrame
from .range_panels import TimeSweepPanel, FieldSweepPanel, DeviceSweepPanel

class RangeSelectFrame(wx.Frame):
    title = 'Select range'

    def __get_device_panel(self, device, device_settings):
        if device.device_name() == 'Time':
            panel = TimeSweepPanel(self.panel, device, device_settings)
        elif self.xdevices.index(device) == 0 and callable(getattr(device, 'get_field', None)):
            panel = FieldSweepPanel(self.panel, device, device_settings)
        else:
            panel = DeviceSweepPanel(self.panel, device, device_settings)
        return panel

    STR_MODE_DEFAULT = 'Default (n-D scan)'
    STR_MODE_SIMULTANEOUS = 'Simultaneous scan'
    STR_MODE_SEQUENTIAL = 'Sequential scan'

    def __init__(self, parent, dataWriter, ydevices, xdevices):
        super().__init__(parent, wx.ID_ANY, self.title)
        self.BUTTON_FONT = wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.BOLD)
        self.EDIT_FONT = wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.BOLD)

        self.parent = parent
        self.panel = wx.Panel(self)
        self.Bind(wx.EVT_CLOSE, self.on_close)
        self.dataWriter = dataWriter
        self.xdevices = xdevices
        self.ydevices = ydevices
        self.range = []

        self.vbox = wx.BoxSizer(wx.VERTICAL)
        self.hbox_devices = wx.BoxSizer(wx.HORIZONTAL)

        device_settings = CoreSettings.get_device_settings()

        # For each x
        self.device_panels = [self.__get_device_panel(xdevice, device_settings) for xdevice in xdevices]
        for panel in self.device_panels:
            self.hbox_devices.Add(panel, proportion=1, border=5, flag=wx.ALL|wx.GROW)
        self.vbox.Add(self.hbox_devices, proportion=1, border=5, flag=wx.ALL|wx.GROW)

        # One for all
        self.edit_iterations = BoxedTextPanel(self.panel, 'Iterations', size=(120, -1))
        self.edit_iterations.edit.SetFont(self.EDIT_FONT)

        self.edit_iterations_delay = BoxedTextPanel(self.panel, 'Delay between iterations, s', size=(120, -1))
        self.edit_iterations_delay.edit.SetFont(self.EDIT_FONT)

        self.checkbox_backsweep = wx.CheckBox(self.panel, label='Sweep both directions')
        self.checkbox_doublesweep = wx.CheckBox(self.panel, label='Simultaneous sweep')
        self.checkbox_fastascolumns = wx.CheckBox(self.panel, label='Fast device as columns')
        self.combobox_sweep_mode = CaptionDropBox(
            self.panel,
            'Sweep mode',
            [self.STR_MODE_DEFAULT, self.STR_MODE_SIMULTANEOUS, self.STR_MODE_SEQUENTIAL]
            )
        self.combobox_sweep_mode.combo.SetSelection(0)
        self.checkbox_cumulative = wx.CheckBox(self.panel, label='View all curves')

        self.hbox_iterations = wx.BoxSizer(wx.HORIZONTAL)
        self.hbox_iterations.Add(self.edit_iterations, proportion=1, border=5, flag=wx.ALL|wx.GROW)
        self.hbox_iterations.Add(self.edit_iterations_delay, proportion=1, border=5, flag=wx.ALL|wx.GROW)
        self.hbox_iterations.Add(self.checkbox_backsweep, border=5, flag=wx.ALL|wx.ALIGN_CENTER_VERTICAL)

        self.vbox.Add(self.hbox_iterations, flag=wx.ALL|wx.ALIGN_CENTRE_HORIZONTAL)

        self.hbox_extras = wx.BoxSizer(wx.HORIZONTAL)
        self.hbox_extras.Add(self.combobox_sweep_mode, proportion=1, border=5, flag=wx.ALL|wx.GROW)
        self.hbox_extras.Add(self.checkbox_doublesweep, proportion=1, border=5, flag=wx.ALL|wx.GROW)
        self.hbox_extras.Add(self.checkbox_fastascolumns, proportion=1, border=5, flag=wx.ALL|wx.GROW)
        self.hbox_extras.Add(self.checkbox_cumulative, proportion=1, border=5, flag=wx.ALL|wx.GROW)

        self.vbox.Add(self.hbox_extras, flag=wx.ALL|wx.ALIGN_CENTRE_HORIZONTAL)

        self.edit_filename = BoxedTextPanel(self.panel, 'File name', size=(350, -1))
        self.edit_filename.edit.SetFont(ViewSettings().SMALL_FONT)
        self.vbox.Add(self.edit_filename, border=5, flag=wx.ALL|wx.GROW)

        self.__load_settings()

        self.btn_start = wx.Button(self.panel, label='Start', size=(100, 35))
        self.btn_start.SetFont(self.BUTTON_FONT)
        self.Bind(wx.EVT_BUTTON, self.OnStart, self.btn_start)
        self.btn_cancel = wx.Button(self.panel, label='Cancel', size=(100, 35))
        self.btn_cancel.SetFont(self.BUTTON_FONT)
        self.Bind(wx.EVT_BUTTON, self.on_close, self.btn_cancel)

        self.hbox_buttons = wx.BoxSizer(wx.HORIZONTAL)
        self.hbox_buttons.Add(self.btn_start, border=5, flag=wx.ALL)
        self.hbox_buttons.Add(self.btn_cancel, border=5, flag=wx.ALL)

        self.vbox.Add(self.hbox_buttons, flag=wx.ALIGN_CENTER_HORIZONTAL)
        self.panel.SetSizer(self.vbox)
        self.vbox.Fit(self)

        self.parent.Disable()
        self.Center()
        self.SetFocus()
        self.__reload()

    def __reload(self):
        self.dataWriter.start_new_file()
        self.edit_filename.SetValue(self.dataWriter.get_filename())
        for panel in self.device_panels:
            panel.reload()

    def __load_settings(self):
        sweep_settings = CoreSettings.get_sweep_settings()
        self.edit_iterations.SetValue(sweep_settings.iterations)
        self.edit_iterations_delay.SetValue(sweep_settings.iterationsDelay)
        if self.validate_backsweep():
            self.checkbox_backsweep.SetValue(sweep_settings.backsweep)
        else:
            self.checkbox_backsweep.SetValue(False)
            self.checkbox_backsweep.Disable()
        if self.validate_doublesweep():
            self.checkbox_doublesweep.SetValue(sweep_settings.doublesweep)
        else:
            self.checkbox_doublesweep.SetValue(False)
            self.checkbox_doublesweep.Disable()
        if self.validate_fastascolumns():
            self.checkbox_fastascolumns.SetValue(sweep_settings.fastAsColumns)
        else:
            self.checkbox_fastascolumns.SetValue(False)
            self.checkbox_fastascolumns.Disable()
        self.checkbox_cumulative.SetValue(sweep_settings.cumulativeView)

    def save_settings(self):
        device_settings = CoreSettings.get_device_settings()
        for panel in self.device_panels:
            panel.saveSettings(device_settings)
        CoreSettings.set_device_settings(device_settings)

        sweep_settings = CoreSettings.get_sweep_settings()
        sweep_settings.iterations = self.edit_iterations.GetValue()
        sweep_settings.iterationsDelay = self.edit_iterations_delay.GetValue()
        if self.validate_backsweep():
            sweep_settings.backsweep = self.checkbox_backsweep.IsChecked()
        if self.validate_doublesweep():
            sweep_settings.doublesweep = self.checkbox_doublesweep.IsChecked()
        if self.validate_fastascolumns():
            sweep_settings.fastAsColumns = self.checkbox_fastascolumns.IsChecked()
        sweep_settings.cumulativeView = self.checkbox_cumulative.IsChecked()
        CoreSettings.set_sweep_settings(sweep_settings)

    def validate_fastascolumns(self):
        """Check if "Fast as columns" option is possible to activate"""
        return (
            len(self.ydevices) == 1 and
            len(self.device_panels) > 1 and
            not any(device.is_sweep_based() for device in self.ydevices)
            )

    def validate_backsweep(self):
        return self.device_panels[0].can_backsweep()

    def validate_doublesweep(self):
        if len(self.device_panels) != 2:
            return False
        if (
                not isinstance(self.device_panels[0], DeviceSweepPanel) or
                not isinstance(self.device_panels[1], DeviceSweepPanel)
            ):
            return False
        return True

    def validate_device_panel(self, panel):
        if callable(getattr(panel.device, 'check_values', None)) and not panel.device.check_values(panel.GetRange()):
            dlg = wx.MessageDialog(
                self, 'The values range contains points, which are unable to be set by selected device.',
                'Wrong dataset', wx.OK | wx.ICON_INFORMATION)
            dlg.ShowModal()
            return False
        return True

    def sequential_task(self, data_contexts):
        import time
        for i in range(int(self.edit_iterations.GetValue())):
            for device_context in data_contexts:
                self.dataWriter.start_new_file()
                device_context.rearm()
                device_context.start()
                while not device_context.finished:
                    time.sleep(0.1)

    def run_sequential_mode(self):
        data_contexts = []
        for panel in self.device_panels:
            device_context = data_context.DataContext()
            device_context.set_data_writer(self.dataWriter)
            device_context.add_readables(self.ydevices)
            if not self.validate_device_panel(panel):
                return
            if isinstance(panel, FieldSweepPanel):
                device_context.add_observable(panel.device, panel.GetRange(), int(panel.edit_delay.edit.Value))
            else:
                device_context.add_writable(panel.device, panel.GetRange(), int(panel.edit_delay.edit.Value))
            device_context.set_curves_num(
                1,
                float(self.edit_iterations_delay.GetValue()),
                False
            )
            data_contexts.append(device_context)
        self.save_settings()
        self.dataWriter.start_new_file()
        self.dataWriter.save_info_file(
            [dev.description() for dev in self.ydevices],
            [panel.description() for panel in self.device_panels],
            self.description()
            )
        import threading
        wnds = []
        for device_context in data_contexts:
            wnd = ExperimentControlFrame(self, device_context, self.checkbox_cumulative.IsChecked())
            wnd.Show()
            wnds.append(wnd)
        self.thread = threading.Thread(target=self.sequential_task, args=(data_contexts,))
        self.thread.start()

    def OnStart(self, event):
        del event
        # Validation
        if self.checkbox_fastascolumns.IsChecked() and not self.validate_fastascolumns():
            dlg = wx.MessageDialog(
                self, 'Saving Y data in columns is currently only possible with a single Y device.',
                'Too many Y devices', wx.OK | wx.ICON_INFORMATION
                )
            dlg.ShowModal()
            return
        if self.checkbox_backsweep.IsChecked() and not self.validate_backsweep():
            dlg = wx.MessageDialog(
                self, 'It is not possible to sweep both directions in time scans.',
                'No backsweep for time scans', wx.OK | wx.ICON_INFORMATION
                )
            dlg.ShowModal()
            return
        if self.checkbox_doublesweep.IsChecked():
            if not self.validate_doublesweep():
                dlg = wx.MessageDialog(
                    self, 'Simultaneous sweep only possible with two normal x devices.',
                    'Wrong set of devices', wx.OK | wx.ICON_INFORMATION)
                dlg.ShowModal()
                return
            if len(self.device_panels[0].GetRange()) != len(self.device_panels[1].GetRange()):
                dlg = wx.MessageDialog(
                    self, 'Simultaneous sweep needs equal length for x devices.',
                    'Wrong x values', wx.OK | wx.ICON_INFORMATION
                    )
                dlg.ShowModal()
                return
        if self.checkbox_fastascolumns.IsChecked() and self.checkbox_doublesweep.IsChecked():
            dlg = wx.MessageDialog(
                self, 'Simultaneous sweep and saving Y data in columns are not to be combined.',
                'Wrong settings', wx.OK | wx.ICON_INFORMATION
                )
            dlg.ShowModal()
            return

        if self.combobox_sweep_mode.GetValue() == self.STR_MODE_SEQUENTIAL:
            self.run_sequential_mode()
            return

        # TODO: must be done before???
        if self.checkbox_fastascolumns.IsChecked():
            self.dataWriter = ColumnedDataWriter(self.dataWriter.name_exp)
        else:
            self.dataWriter = TextDataWriter(self.dataWriter.name_exp)
        context = data_context.DataContext()
        #TODO: check if modified
        context.set_data_writer(self.dataWriter)
        context.add_readables(self.ydevices)
        if not self.checkbox_doublesweep.IsChecked():
            for panel in self.device_panels:
                if not self.validate_device_panel(panel):
                    return
                if isinstance(panel, FieldSweepPanel):
                    context.add_observable(panel.device, panel.GetRange(), int(panel.edit_delay.edit.Value))
                else:
                    context.add_writable(panel.device, panel.GetRange(), int(panel.edit_delay.edit.Value))
        else:
            for panel in self.device_panels:
                if not self.validate_device_panel(panel):
                    return
            context.add_double_writable(
                self.device_panels[0].device, self.device_panels[1].device,
                self.device_panels[0].GetRange(), self.device_panels[1].GetRange(),
                int(panel.edit_delay.edit.Value)
                )

        context.set_curves_num(
            int(self.edit_iterations.GetValue()),
            float(self.edit_iterations_delay.GetValue()),
            self.checkbox_backsweep.IsChecked()
            )
        self.save_settings()
        self.dataWriter.start_new_file()
        self.dataWriter.save_info_file(
            [dev.description() for dev in self.ydevices],
            [panel.description() for panel in self.device_panels],
            self.description()
            )
        wnd = ExperimentControlFrame(self, context, self.checkbox_cumulative.IsChecked())
        context.start()
        wnd.Show()

    def description(self):
        ret = []
        ret.append(('Iterations', self.edit_iterations.GetValue()))
        ret.append(('Iterations delay', self.edit_iterations_delay.GetValue()))
        ret.append(('Backsweep', self.checkbox_backsweep.GetValue()))
        ret.append(('Fast as columns', self.checkbox_fastascolumns.GetValue()))
        ret.append(('Double sweep', self.checkbox_doublesweep.GetValue()))
        return ret

    def Enable(self):
        self.__reload()
        wx.Frame.Enable(self)

    def on_close(self, event):
        del event
        self.save_settings()
        self.Destroy()
        self.parent.Enable()
        self.parent.SetFocus()
