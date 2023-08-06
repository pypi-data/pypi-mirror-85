"""
    pyxperiment/frames/plots/pcolor_plot.py: The module defining a pcolor
    plot panel for showing 2D color plots

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
import matplotlib
import matplotlib.animation as animation
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import (
    FigureCanvasWxAgg as FigCanvas
)

class ImageLimits:
    def __init__(self):
        self._limits_dist = dict()
        self._manual_limits = None

    def update_limits(self, source, values):
        self._limits_dist[source] = values

    def get_limits(self):
        if not self._manual_limits is None:
            return self._manual_limits
        min_value = min(map(lambda x: x[0], self._limits_dist.values()))
        max_value = max(map(lambda x: x[1], self._limits_dist.values()))
        return (min_value, max_value)

    def set_manual_limits(self):
        pass

class ImageShowPanel(wx.Panel):

    def __init__(self, parent, title, limits=ImageLimits(), dpi=100):
        super().__init__(parent, wx.ID_ANY)
        self.limits = limits
        self.dpi = dpi
        self.fig = Figure((4.5, 3.5), dpi=self.dpi, facecolor='lightgray')
        self.canvas = FigCanvas(self, -1, self.fig)

        self.axes = self.fig.add_subplot(111)

        if callable(getattr(self.axes, 'set_facecolor', None)):
            self.axes.set_facecolor('white')
        else:
            self.axes.set_axis_bgcolor('white')

        self.axes.grid(True, color='black')
        if title:
            self.axes.set_title(title, size=10)
        #self.toolbar = NavigationToolbar(self.canvas)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.canvas, 1, flag=wx.ALL | wx.GROW)
        #self.sizer.Add(self.toolbar, 0, flag=wx.ALL | wx.GROW)
        self.SetSizer(self.sizer)
        self.sizer.Fit(self)

        self.images = []
        self.meshes = []
        #self.animator = animation.FuncAnimation(self.fig, self.__update_func, interval=100, blit=True)
        self.colorbar = None

    class Image:
        def __init__(self, axes, x, y):
            self.x = x
            self.y = y
            self.data_provider = None
            self.data = np.array([np.nan for i in range(len(x)*len(y))])
            X = self.__mesh_from_range(x)
            Y = self.__mesh_from_range(y)
            axes.set_xlim(left=min(X), right=max(X))
            axes.set_ylim(bottom=min(Y), top=max(Y))
            X, Y = np.meshgrid(np.array(X), np.array(Y))
            self.mesh = axes.pcolormesh(X, Y, np.zeros((len(y), len(x))), cmap='inferno')
            self.cmap = matplotlib.cm.get_cmap('inferno')

        @staticmethod
        def __mesh_from_range(x):
            x_new = [float((x[i]+x[i+1])/2) for i in range(len(x)-1)]
            x_new.insert(0, float(x[0]-(x[1]-x[0])/2))
            x_new.append(float(x[-1]+(x[-1]-x[-2])/2))
            return x_new

        def update(self, panel):
            zdata = self.data_provider.get_data()
            for i in range(len(zdata)):
                curve = zdata[i].read_data()
                start = i * len(self.x)
                if zdata[i].write_data() == self.x:
                    self.data[start:(start+len(curve))] = curve
                elif start+len(self.x)-len(curve)-1 >= 0:
                    self.data[(start+len(self.x)-1):(start+len(self.x)-len(curve)-1):-1] = curve
                else:
                    self.data[(start+len(self.x)-1)::-1] = curve
            new_data = np.ma.masked_invalid(np.atleast_2d(self.data))
            self.cmap.set_bad('black', 1)
            if not new_data.min() is np.ma.masked:
                panel.limits.update_limits(panel.axes.get_title(), (new_data.min(), new_data.max()))
                limits = panel.limits.get_limits()
                panel.colorbar.set_clim(vmin=limits[0], vmax=limits[1])
                panel.colorbar.set_ticks(np.linspace(limits[0], limits[1], num=11, endpoint=True))
                panel.colorbar.draw_all()
                norm = matplotlib.colors.Normalize(vmin=limits[0], vmax=limits[1])
                new_color = self.cmap(norm(new_data.T.ravel()))
                self.mesh.update({'facecolors':new_color})

        def set_data(self, data_provider):
            self.data_provider = data_provider

    def add_image(self, x, y):
        for img in self.images:
            img.mesh.remove()
        self.images = []
        self.meshes = []
        image = ImageShowPanel.Image(self.axes, x, y)
        self.images.append(image)
        self.meshes = [x.mesh for x in self.images]
        if self.colorbar == None:
            self.colorbar = self.fig.colorbar(image.mesh)
        self.canvas.draw()
        return image

    def update_image(self, image):
        image.update(self)
        self.canvas.draw()

    def __update_func(self, *args):
        return self.meshes
