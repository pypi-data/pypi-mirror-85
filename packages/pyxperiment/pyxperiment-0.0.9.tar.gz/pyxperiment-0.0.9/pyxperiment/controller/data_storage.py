"""
    pyxperiment/controller/data_storage.py: The storage for experimental data

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

class DataSweep(object):
    """
    A result of a single sweep
    """

    def __init__(self, time, wrdata, rddata):
        self._time = time
        self._wrdata = wrdata
        self._rddata = rddata

    def read_data(self):
        return self._rddata

    def write_data(self):
        return self._wrdata

    def time_markers(self):
        return self._time

class DataStorage(object):
    """
    Data storage stores measured data for the entire experiment
    """

    def __init__(self):
        self._curves = []

    def add_curve(self, time, writable, readables):
        """
        Aggregates readable and writable data in a single set.
        The data is not copied, but referenced to account for modifications.
        """
        self._curves.append(DataSweep(time, writable.values, [rdev._values for rdev in readables]))

    def get_data(self):
        """
        Get all the stored curves
        """
        return self._curves
