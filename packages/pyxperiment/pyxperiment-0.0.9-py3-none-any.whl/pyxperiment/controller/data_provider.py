"""
    pyxperiment/controller/data_provider.py:
    Manipulates data storage to fetch specific datasets

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

class FilteredCurve(object):
    """FilteredCurve manages filtering for a single curve"""

    def __init__(self, curve, y_device):
        self.curve = curve
        self.y_device = y_device

    def read_data(self):
        data = self.curve.read_data()
        if self.y_device != None:
            data = data[self.y_device]
        return data

    def write_data(self):
        return self.curve.write_data()

    def time_markers(self):
        return self.curve.time_markers()

class DataProvider(object):
    """
    DataProvider fetches data from DataStorage for a specific
    Y device, or all Y devices according to set rules
    """

    def __init__(self, data_storage):
        self.data_storage = data_storage
        self.filter_x = None# Take all slow x points
        self.y_device = None# fetch all y devices

    def set_device(self, device):
        """
        Set the y points to be fetched
        """
        self.y_device = device
        return self

    def set_filter_x(self, index):
        """
        Set filter to 0 to take odd, 1 to take even, None to take all
        """
        self.filter_x = index
        return self

    def get_data(self):
        """
        Return the set of filtered curves
        """
        data = self.data_storage.get_data()
        if self.filter_x != None:
            data = data[self.filter_x::2]
        if self.y_device != None:
            data = [FilteredCurve(c, self.y_device) for c in data]
        return data
