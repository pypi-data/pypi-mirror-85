"""
    pyxperiment/frames/plots/line_plot.py: The module defining line plot panel
    for data representation

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

from enum import Enum
from math import isinf, isnan
import wx
import numpy as np
import pylab
import matplotlib
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import \
    FigureCanvasWxAgg as FigCanvas, \
    NavigationToolbar2WxAgg
from pyxperiment.controller.device_control import SweepReadableControl
from pyxperiment.controller.device_options import ValueDeviceOption

class NavigationToolbar(NavigationToolbar2WxAgg):
    """A custom NavigationToolbar replacement to fix the rubberband glitches"""
    def __init__(self, canvas):
        NavigationToolbar2WxAgg.__init__(self, canvas)
        self.lastRubberband = None
        #self.DeleteToolByPos(7)

    def draw_rubberband(self, event, x0, y0, x1, y1):
        self.lastRubberband = (x0, y0, x1, y1)
        NavigationToolbar2WxAgg.draw_rubberband(self, event, x0, y0, x1, y1)

    def remove_rubberband(self):
        self.lastRubberband = None
        NavigationToolbar2WxAgg.remove_rubberband(self)

    def redraw_rubberband(self):
        if self.lastRubberband != None:
            self.wxoverlay = wx.Overlay()
            NavigationToolbar2WxAgg.draw_rubberband(self, None, *self.lastRubberband)

class DataViewMode(Enum):
    SIMPLE = 1
    CUMULATIVE = 2
    SLOWERX = 3

class MyScalarFormatter(matplotlib.ticker.ScalarFormatter):
    """Minor tweaks to display the exponent along the value"""
    def __init__(self):
        super().__init__(False, True, None)
        self.set_powerlimits((-3, 4))

    def get_offset(self):
        return ''

    def _set_format(self, *arg):
        super()._set_format(*arg)
        offset = super().get_offset().lstrip('$')
        if offset:
            self.format = self.format.rstrip('$') + offset

class DataViewAxis(wx.Panel):

    plot_colors = [(1, 1, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1), (0, 1, 1), (1, 0, 1)]

    def __init__(self, parent, dataContext, readable, mode=DataViewMode.SIMPLE, dpi=100):
        super().__init__(parent, wx.ID_ANY)

        self.dataContext = dataContext
        self.readable = readable
        self.dpi = dpi
        self.mode = mode

        self.fig = Figure((4.5, 3.0), dpi=self.dpi, facecolor='lightgray')
        self.canvas = FigCanvas(self, -1, self.fig)
        self.toolbar = NavigationToolbar(self.canvas)
        self.toolbar.set_cursor = lambda cursor: None

        self.axes = self.fig.add_subplot(111)
        self.fig.subplots_adjust(left=0.15, right=0.95, top=0.9, bottom=0.1)
        if callable(getattr(self.axes, 'set_facecolor', None)):
            self.axes.set_facecolor('black')
        else:
            self.axes.set_axis_bgcolor('black')
        self.axes.grid(True, color='gray')
        self.axes.set_title('Reading from: ' + self.readable.device_name + ' at ' + self.readable.location, size=10)
        if isinstance(self.readable.device, ValueDeviceOption):
            if self.readable.device.phys_quantity() is not None:
                self.axes.set_ylabel(self.readable.device.name + ', ' + self.readable.device.phys_quantity())
            else:
                self.axes.set_ylabel(self.readable.device.name)

        pylab.setp(self.axes.get_xticklabels(), fontsize=9)
        pylab.setp(self.axes.get_yticklabels(), fontsize=9)
        self.axes.get_xaxis().set_major_formatter(MyScalarFormatter())
        self.axes.get_yaxis().set_major_formatter(MyScalarFormatter())

        self.cb_autox = wx.CheckBox(
            self, -1, "Auto scale X", style=wx.ALIGN_RIGHT)
        self.Bind(wx.EVT_CHECKBOX, self.on_cb_xlab, self.cb_autox)
        self.cb_autox.SetValue(False)

        self.cb_autoy = wx.CheckBox(
            self, -1, "Auto scale Y", style=wx.ALIGN_RIGHT)
        self.Bind(wx.EVT_CHECKBOX, self.on_cb_ylab, self.cb_autoy)
        self.cb_autoy.SetValue(True)

        self.sizer = wx.BoxSizer(wx.VERTICAL)

        self.sizer_controls = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer_controls.Add(self.toolbar, 0, wx.ALIGN_LEFT)
        self.sizer_controls.Add(self.cb_autox, border=5, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL)
        self.sizer_controls.Add(self.cb_autoy, border=5, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL)

        self.sizer.Add(self.canvas, 1, flag=wx.ALL | wx.GROW)
        self.sizer.Add(self.sizer_controls, 0, flag=wx.ALIGN_LEFT | wx.TOP)

        self.SetSizer(self.sizer)
        self.sizer.Fit(self)

        if self.readable.num_channels() > len(self.plot_colors):
            self.plot_colors = [self.plot_colors[1]] * self.readable.num_channels()

        self.plot_data = [
            self.axes.plot([], linewidth=1, color=self.plot_colors[i])[0]
            for i in range(self.readable.num_channels())
            ]
        self.curves_plotted = 1
        self.ymin = None
        self.ymax = None
        self.__set_xscale()

    def Destroy(self):
        # TODO: почему-то класс корректно не уничтожается - видимо надо закрывать график
        del self.readable
        del self.dataContext
        return super().Destroy()

    def __set_xscale(self):
        if isinstance(self.readable, SweepReadableControl):
            xdata = list(map(float, self.readable.get_sweep_x()))
        else:
            xdata = self.dataContext.xval()
        if xdata:
            self.axes.set_xbound(lower=min(xdata), upper=max(xdata))

    def on_cb_xlab(self, event):
        del event
        if not self.cb_autox.Value:
            self.__set_xscale()
        self.draw_plot()

    def on_cb_ylab(self, event):
        del event
        self.draw_plot()

    def draw_plot(self):
        """Redraws the plot"""
        data_storage = self.dataContext.all_data
        if self.mode == DataViewMode.CUMULATIVE:
            if len(data_storage.get_data()) > self.curves_plotted:
                for plot in self.plot_data:
                    plot.set_color([col / 3 for col in plot.get_color()])
                self.plot_data = [
                    self.axes.plot([], linewidth=1, color=self.plot_colors[i])[0]
                    for i in range(self.readable.num_channels())
                ]
                self.curves_plotted += 1
                self.__set_xscale()
        else:
            self.ymin = None
            self.ymax = None

        if not data_storage.get_data():
            return
        xdata = list(map(float, data_storage.get_data()[-1].write_data()))

        for i in range(self.readable.num_channels()):
            try:
                ydata = list(map(float, self.readable.data(i)))
            except:
                return

            if self.cb_autoy.Value and ydata:
                self.ymin = min(self.ymin, min(ydata)) if self.ymin else min(ydata)
                self.ymax = max(self.ymax, max(ydata)) if self.ymax else max(ydata)

            if isinstance(self.readable, SweepReadableControl):
                self.__set_xscale()
                xdata = list(map(float, self.readable.get_sweep_x()))
            xdata_part = xdata[0:len(ydata)] if ydata else []
            self.plot_data[i].set_xdata(np.array(xdata_part))
            self.plot_data[i].set_ydata(np.array(ydata))

            if self.cb_autox.Value and xdata_part:
                self.axes.set_xbound(lower=min(xdata_part), upper=max(xdata_part))

        if (
                self.cb_autoy.Value and not any(
                    map(lambda x: x is None or isinf(x) or isnan(x), [self.ymin, self.ymax]))
            ):
            margin = (self.ymax - self.ymin) / 10
            if margin == 0:
                margin = 0.1
            self.axes.set_ybound(lower=self.ymin - margin, upper=self.ymax + margin)

        self.canvas.draw()
        self.toolbar.redraw_rubberband()
