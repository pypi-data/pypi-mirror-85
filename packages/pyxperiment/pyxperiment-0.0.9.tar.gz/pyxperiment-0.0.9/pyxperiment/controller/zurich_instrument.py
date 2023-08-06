"""
    pyxperiment/controller/zurich_instrument.py: The base class for instruments
    manufactured by Zurich Instruments

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
try:
    import zhinst
    import zhinst.utils
except ImportError:
    logging.debug('zhinst failed to import', exc_info=True)
from .instrument import Instrument

class ZurichInstrument(Instrument):
    """
    The base class for instruments manufactured by Zurich Instruments
    """

    APILEVEL = 6

    def __init__(self, resource, devtype):
        super().__init__('')
        self.resource = resource
        self.devtype = devtype
        (self.ds, self.node_name, _) = zhinst.utils.create_api_session(
            self.resource,
            self.APILEVEL,
            required_devtype=self.devtype)

    @property
    def location(self):
        return self.resource

    def device_name(self):
        return 'Zurich Instruments ' + self.ds.getString('/%s/features/devtype' % self.node_name)

    def device_id(self):
        return self.ds.getString('/%s/features/serial' % self.node_name)

    def get_double(self, cmd):
        return str(self.ds.getDouble(cmd % self.node_name))

    def set_double(self, cmd, value):
        self.ds.setDouble(cmd % self.node_name, float(value))

    def get_int(self, cmd):
        return str(self.ds.getInt(cmd % self.node_name))

    def set_int(self, cmd, value):
        self.ds.setDouble(cmd % self.node_name, int(value))
