"""
    pyxperiment/frames/experiment_control_frame.py:
    The frame for experiment control

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

from pyxperiment.settings.view_settings import ViewSettings
from .plots.line_plot import DataViewAxis, DataViewMode
from .basic_panels import BoxedTextPanel

class ExperimentControlFrame(wx.Frame):
    """
    The frame provides graphics for experiment control
    """

    title = 'Experiment control'

    class XShowPanel(wx.Panel):
        def __init__(self, parent, writable):
            super().__init__(parent, wx.ID_ANY)
            self.writable = writable

            box = wx.StaticBox(self, -1, writable.device_name)
            boxsizer = wx.StaticBoxSizer(box, wx.VERTICAL)
            sizer = wx.BoxSizer(wx.HORIZONTAL)

            if writable.location != '':
                self.static_location = wx.StaticText(self, label=writable.location)
                boxsizer.Add(self.static_location, border=5, flag=wx.ALL | wx.ALIGN_LEFT)

            self.edit_numpoints = BoxedTextPanel(self, 'Read points', initval='', size=(80, -1))
            self.edit_numpoints.SetEnabled(False)
            self.edit_numpoints.edit.SetFont(ViewSettings().EDIT_FONT)
            self.edit_value = BoxedTextPanel(self, 'Value:', initval='', size=(80, -1))
            self.edit_value.SetEnabled(False)
            self.edit_value.edit.SetFont(ViewSettings().EDIT_FONT)

            sizer.Add(self.edit_numpoints, border=5, flag=wx.ALL | wx.ALIGN_LEFT)
            sizer.Add(self.edit_value, border=5, flag=wx.ALL | wx.ALIGN_LEFT)
            boxsizer.Add(sizer, flag=wx.ALL)
            self.SetSizer(boxsizer)
            boxsizer.Fit(self)

        def Update(self):
            self.edit_numpoints.edit.Value = str(self.writable.index)
            self.edit_value.edit.Value = str(Decimal(self.writable.value))

    def __init__(self, parent, dataContext, cumulative, auto_close=False):
        super().__init__(parent, wx.ID_ANY, self.title)
        self.Bind(wx.EVT_CLOSE, self.on_close)

        self.parent = parent
        self.dataContext = dataContext
        self.auto_close = auto_close

        self.statusbar = self.CreateStatusBar()
        self.create_main_panel(cumulative)
        self.Center()

        self.redraw_timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.on_redraw_timer, self.redraw_timer)
        self.redraw_timer.Start(100)

        if self.parent:
            self.parent.Disable()
        self.SetFocus()

    def create_main_panel(self, cumulative):
        self.panel = wx.Panel(self)

        self.graphs = [
            DataViewAxis(
                self.panel, self.dataContext, readable,
                DataViewMode.CUMULATIVE if cumulative else DataViewMode.SIMPLE
                )
            for readable in self.dataContext.readables
            ]

        self.panels_calibrators = [
            ExperimentControlFrame.XShowPanel(self.panel, writable)
            for writable in self.dataContext.writables
            ]

        self.save_button = wx.Button(self.panel, wx.ID_ANY, "Save", size=(100, 35))
        self.save_button.SetFont(ViewSettings().BUTTON_FONT)
        self.Bind(wx.EVT_BUTTON, self.on_save_button, self.save_button)

        self.pause_button = wx.Button(self.panel, wx.ID_ANY, "Pause", size=(100, 35))
        self.pause_button.SetFont(ViewSettings().BUTTON_FONT)
        self.Bind(wx.EVT_BUTTON, self.on_pause_button, self.pause_button)

        self.stop_button = wx.Button(self.panel, wx.ID_ANY, "Stop", size=(100, 35))
        self.stop_button.SetFont(ViewSettings().BUTTON_FONT)
        self.Bind(wx.EVT_BUTTON, self.on_close, self.stop_button)

        self.edit_readdelay = BoxedTextPanel(self.panel, 'Read delay, ms', initval='0', size=(80, -1))
        self.edit_readdelay.edit.Enabled = False
        self.edit_readdelay.edit.SetFont(ViewSettings().EDIT_FONT)
        self.edit_readdelaymax = BoxedTextPanel(self.panel, 'Max delay, ms', initval='0', size=(80, -1))
        self.edit_readdelaymax.edit.Enabled = False
        self.edit_readdelaymax.edit.SetFont(ViewSettings().EDIT_FONT)
        self.edit_iteration = BoxedTextPanel(self.panel, 'Iteration', size=(80, -1))
        self.edit_iteration.edit.Enabled = False
        self.edit_iteration.edit.SetFont(ViewSettings().EDIT_FONT)
        self.edit_iterationsnum = BoxedTextPanel(self.panel, 'Num Iterations', size=(80, -1))
        self.edit_iterationsnum.edit.Enabled = False
        self.edit_iterationsnum.edit.SetFont(ViewSettings().EDIT_FONT)
        self.edit_filename = BoxedTextPanel(self.panel, 'Filename', size=(400, -1))
        self.edit_filename.edit.SetFont(ViewSettings().SMALL_FONT)
        self.edit_filename.edit.Enabled = False

        self.hbox_graphs = wx.BoxSizer(wx.HORIZONTAL)
        for graph in self.graphs:
            self.hbox_graphs.Add(graph, 1, flag=wx.ALL | wx.GROW)

        self.hbox_xval = wx.BoxSizer(wx.HORIZONTAL)
        for panel in self.panels_calibrators:
            self.hbox_xval.Add(panel, flag=wx.ALL | wx.ALIGN_LEFT)

        self.hbox_time = wx.BoxSizer(wx.HORIZONTAL)
        self.hbox_time.Add(self.edit_readdelay, border=5, flag=wx.ALL | wx.ALIGN_LEFT)
        self.hbox_time.Add(self.edit_readdelaymax, border=5, flag=wx.ALL | wx.ALIGN_LEFT)
        self.hbox_iter = wx.BoxSizer(wx.HORIZONTAL)
        self.hbox_iter.Add(self.edit_iteration, border=5, flag=wx.ALL | wx.ALIGN_LEFT)
        self.hbox_iter.Add(self.edit_iterationsnum, border=5, flag=wx.ALL | wx.ALIGN_LEFT)

        self.vbox_misc = wx.BoxSizer(wx.VERTICAL)
        self.vbox_misc.Add(self.hbox_time, flag=wx.ALL | wx.ALIGN_LEFT)
        self.vbox_misc.Add(self.hbox_iter, flag=wx.ALL | wx.ALIGN_LEFT)

        self.hboxbuttons = wx.BoxSizer(wx.HORIZONTAL)
        self.hboxbuttons.Add(self.save_button, border=5, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL)
        self.hboxbuttons.Add(self.pause_button, border=5, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL)
        self.hboxbuttons.Add(self.stop_button, border=5, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL)

        self.vbox_controls = wx.BoxSizer(wx.VERTICAL)
        self.vbox_controls.Add(self.hboxbuttons, flag=wx.ALIGN_CENTER_HORIZONTAL)
        self.vbox_controls.Add(self.edit_filename, flag=wx.ALIGN_CENTER_VERTICAL| wx.GROW)

        self.hbox_controls = wx.BoxSizer(wx.HORIZONTAL)
        self.hbox_controls.Add(self.vbox_misc, 0, flag=wx.ALIGN_LEFT | wx.TOP)
        self.hbox_controls.Add(self.vbox_controls, 1, flag=wx.ALIGN_CENTER_VERTICAL | wx.GROW)

        self.vbox = wx.BoxSizer(wx.VERTICAL)
        self.vbox.Add(self.hbox_graphs, 1, flag=wx.TOP | wx.GROW)
        self.vbox.Add(self.hbox_xval, 0, flag=wx.ALIGN_LEFT | wx.TOP)
        self.vbox.Add(self.hbox_controls, 0, flag=wx.ALIGN_LEFT | wx.TOP | wx.GROW)

        self.panel.SetSizer(self.vbox)
        self.vbox.Fit(self)

    def on_save_button(self, event):
        del event
        self.dataContext.save()

    def on_pause_button(self, event):
        del event
        self.dataContext.pause(not self.dataContext.isPaused)
        self.pause_button.SetLabel("Resume" if self.dataContext.isPaused else "Pause")

    def on_go_to_start_button(self, event):
        del event
        self.dataContext.sweepToStart()
        self.pause_button.Disable()

    def on_redraw_timer(self, event):
        del event
        if self.dataContext.finished:
            self.save_button.Disable()
            self.pause_button.SetLabel('Go to start')
            self.Bind(wx.EVT_BUTTON, self.on_go_to_start_button, self.pause_button)
            if self.auto_close:
                self.on_close(None)
                return

        self.edit_readdelay.SetValue("{:.3f}".format(self.dataContext.elapsed * 1000))
        self.edit_readdelaymax.SetValue("{:.3f}".format(self.dataContext.maxDelay * 1000))
        self.edit_iteration.SetValue(str(self.dataContext.currentCurve))
        self.edit_iterationsnum.SetValue(str(self.dataContext.curves_num))
        self.edit_filename.SetValue(self.dataContext.filename)
        self.set_status_message(self.dataContext.status)

        for panel in self.panels_calibrators:
            panel.Update()
        for graph in self.graphs:
            graph.draw_plot()

    def on_close(self, event):
        del event
        self.dataContext.stop()
        del self.dataContext
        self.redraw_timer.Stop()
        for graph in self.graphs:
            graph.Destroy()
        self.Destroy()
        if self.parent:
            self.parent.Enable()
            self.parent.SetFocus()

    def set_status_message(self, msg):
        self.statusbar.SetStatusText(msg)
