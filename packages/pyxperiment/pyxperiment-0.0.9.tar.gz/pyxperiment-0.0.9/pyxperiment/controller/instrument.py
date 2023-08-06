"""
    pyxperiment/controller/instrument.py:
    The base class for all test and measure instruments

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

from threading import RLock
from abc import (
    ABCMeta, abstractmethod, abstractstaticmethod, abstractproperty
)
# TODO: remove this connection
from pyxperiment.frames.device_config import DeviceConfig
from .device_options import (
    ValueDeviceOption, DeviceOption
)

class Instrument(metaclass=ABCMeta):
    """
    This class defines any instruments, controllable with the application

    :param name: A user-friendly personal instrument name
    """

    def __init__(self, name):
        self.name = name
        # Lock for access management
        self.__lock = RLock()
        # List of all options TODO: remove
        self.options = []
        self.__bind_properties()

    def __bind_properties(self):
        """
        When the device instance is created all the properties must be bound
        to this device instance
        """
        for attr in filter(lambda x: not x.startswith("_"), dir(self.__class__)):
            prop = getattr(self.__class__, attr)
            # Properties that are contained directly in the class
            if isinstance(prop, DeviceOption):
                setattr(self, attr, prop.with_instance(self))
            # Lists of propetries
            if isinstance(prop, list) and all([isinstance(el, DeviceOption) for el in prop]):
                setattr(self, attr, list([el.with_instance(self) for el in prop]))

    @abstractproperty
    def location(self):
        """
        Get the instrument location string
        """

    @abstractstaticmethod
    def driver_name():
        """
        Get the controlled instrument class name string
        """

    @abstractmethod
    def device_name(self):
        """
        Get the instrument model
        """

    def device_id(self):
        """
        Get the unique serial number, assigned by the manufacturer
        """
        return 'Unknown'

    @property
    def lock(self):
        """TODO: remove the lock accessor"""
        return self.__lock

    def to_remote(self):
        """
        Make preparations as a sweep is starting
        """

    def to_local(self):
        """
        Enable local controls after sweep is over
        """

    def is_sweep_based(self):
        """
        Tell, if this device performes measurements via sweeps
        """
        return callable(getattr(self, 'get_sweep', None))

    def get_options(self):
        """
        Return all the options for this instrument
        """
        return self.options

    def set_options(self, options_list):
        """
        Set the options list (to be called from successor)
        """
        self.options = options_list

    @classmethod
    def get_properties(cls):
        """
        Return all the sweepable options for this instrument
        """
        properties = [
            prop
            for prop in [getattr(cls, attr) for attr in dir(cls) if not attr.startswith("_")]
            if isinstance(prop, ValueDeviceOption) and prop.is_sweepable()
            ]
        for prop_list in [getattr(cls, attr) for attr in dir(cls)]:
            if isinstance(prop_list, list) and prop_list:
                properties.extend([
                    prop
                    for prop in prop_list
                    if isinstance(prop, ValueDeviceOption) and prop.is_sweepable()
                ])
        return properties

    @classmethod
    def get_readable_properties(cls):
        """
        Get all the readable properties for this class
        """
        return list(filter(lambda x: x.is_readable(), cls.get_properties()))

    @classmethod
    def get_writable_properties(cls):
        """
        Get all the writable properties for this class
        """
        return list(filter(lambda x: x.is_writable(), cls.get_properties()))

    @classmethod
    def is_readable(cls):
        """
        Check if this instrument is able to read any properties
        """
        return (
            (not callable(getattr(cls, 'set_value', None))) or
            len(cls.get_readable_properties()) > 0
        )

    @classmethod
    def is_writable(cls):
        """
        Check if this instrument is able to set any properties
        """
        return (
            callable(getattr(cls, 'set_value', None)) or
            callable(getattr(cls, 'get_field', None)) or
            len(cls.get_writable_properties()) > 0
        )

    def description(self):
        ret = [(option.name, str(option.get_value())) for option in self.get_options()]
        ret.insert(0, ('Address', self.location))
        ret.insert(0, ('Name', self.device_name()))
        return ret

    def get_config_class(self):
        return DeviceConfig
