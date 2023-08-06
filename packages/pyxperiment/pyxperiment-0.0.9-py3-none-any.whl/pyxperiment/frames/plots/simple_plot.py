"""
    pyxperiment/frames/plots/simple_plot.py: The module defining a simple line
    plot panel for various purposes

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
import numpy as np
import pylab
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import \
    FigureCanvasWxAgg as FigCanvas

class SimpleAxisPanel(wx.Panel):
    """
    A simple panel, containing a single line graph
    """

    def __init__(self, parent, dpi=80):
        super().__init__(parent, wx.ID_ANY)

        self.dpi = dpi
        self.fig = Figure((4.0, 2.25), dpi=self.dpi)

        self.axes = self.fig.add_subplot(111)
        if callable(getattr(self.axes, 'set_facecolor', None)):
            self.axes.set_facecolor('black')
        else:
            self.axes.set_axis_bgcolor('black')
        self.axes.grid(True, color='gray')

        pylab.setp(self.axes.get_xticklabels(), fontsize=8)
        pylab.setp(self.axes.get_yticklabels(), fontsize=8)

        self.plot_data = self.axes.plot([], linewidth=1, color=(1, 1, 0))[0]

        self.canvas = FigCanvas(self, -1, self.fig)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.canvas, 1, flag=wx.ALL | wx.GROW)
        self.SetSizer(self.sizer)
        self.sizer.Fit(self)

    def plot(self, x_values, y_values):
        """
        Set the display data
        """
        if len(x_values) > 1:
            self.axes.set_xbound(lower=min(x_values), upper=max(x_values))
            self.axes.set_ybound(lower=min(y_values), upper=max(y_values))

        self.plot_data.set_xdata(np.array(x_values))
        self.plot_data.set_ydata(np.array(y_values))
        self.canvas.draw()
        