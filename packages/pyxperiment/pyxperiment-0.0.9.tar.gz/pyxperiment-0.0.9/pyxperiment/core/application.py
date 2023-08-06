"""
    pyxperiment/core/application.py: This module defines the base entity for any
    PyXperiment application

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

import logging
import sys
import wx
import matplotlib
import pyvisa as visa

class PyXperimentApp(object):
    """The PyXperiment application basebone"""

    app = None

    def __init__(self):
        # Configure logging and global exception handling
        logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s',
                            filename='logfile.log', level=logging.INFO)
        sys.excepthook = self.log_excepthook
        # Configure matplotlib to use wxpython
        matplotlib.use('WXAgg')
        self.wx_app = wx.App()
        # Import other classes, that may result in exceptions
        from pyxperiment.controller import DeviceFactory
        from pyxperiment.settings.core_settings import CoreSettings
        self._settings = CoreSettings
        # Create resource manager
        self._resource_manager = DeviceFactory(
            visa.ResourceManager(self.settings.get_resource_manager())
            )
        PyXperimentApp.app = self
        self.is_running = False

    @staticmethod
    def log_excepthook(exc_type, exc_value, exc_traceback):
        """Logs the unhandled exception to log file"""
        if not issubclass(exc_type, KeyboardInterrupt):
            logging.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))
        sys.__excepthook__(exc_type, exc_value, exc_traceback)

    @property
    def frame(self):
        """Get the application main frame"""
        return self.wx_app.frame

    @frame.setter
    def frame(self, value):
        """Set the application main frame"""
        self.wx_app.frame = value

    def start(self):
        """Start the application main loop"""
        if not self.is_running:
            if self.frame:
                self.frame.Show()
            self.is_running = True
            self.wx_app.MainLoop()
            self.frame = None
            self.is_running = False

    @property
    def resource_manager(self):
        """Get the global resource manager"""
        return self._resource_manager

    @property
    def settings(self):
        """Get the global application settings"""
        return self._settings
