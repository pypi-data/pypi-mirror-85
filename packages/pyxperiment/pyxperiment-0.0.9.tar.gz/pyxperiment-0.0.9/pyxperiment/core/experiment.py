"""
    pyxperiment/core/experiment.py: This module defines the class for defining
    a single data aquisition activity

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

from pyxperiment.controller.data_context import DataContext
from pyxperiment.frames.experiment_control_frame import ExperimentControlFrame

class Experiment(object):
    """
    Experiment defines the interface for a single data aquisition activity
    """

    def __init__(self, app, data_writer):
        """
        Create a new empty experiment.

        Parameters
        ----------
        app : the PyXperimentApp entity of the current application
        """
        self.app = app
        self.data_writer = data_writer
        self.data_context = DataContext()
        self.data_context.set_data_writer(self.data_writer)

    def add_observable(self, writable, values, timeout):
        """
        Add the device, which reads the parameter for Х axis
        """
        self.data_context.add_observable(writable, values, timeout)

    def add_writable(self, writable, values, timeout):
        """
        Add the device which will set some parameter
        """
        self.data_context.add_writable(writable, values, timeout)

    def add_double_writable(self, writable1, writable2, values1, values2, timeout):
        """
        Add the devices which will set their parameters simultaneously
        """
        self.data_context.add_double_writable(writable1, writable2, values1, values2, timeout)

    def add_readables(self, readables):
        """
        Add the devices which will read some parameters
        """
        self.data_context.add_readables(readables)

    def add_curve_callback(self, callback):
        """
        Add a function to be called after a curve is finished
        """
        self.data_context.add_curve_callback(callback)

    def set_curves_num(self, num, delay, backsweep):
        """
        Sets the number of repeated curve measurements
        """
        self.data_context.set_curves_num(num, delay, backsweep)

    def run(self, auto_close=False):
        """
        Start the experiment. Blocks current execution until the experiment is complete.
        """
        self.data_writer.start_new_file()
        if self.data_context.finished:
            self.data_context.rearm()
        control_frame = ExperimentControlFrame(self.app.frame, self.data_context, True, auto_close)
        control_frame.Show()
        self.data_context.start()
        if self.app.frame is None:
            self.app.frame = control_frame
        self.app.start()
