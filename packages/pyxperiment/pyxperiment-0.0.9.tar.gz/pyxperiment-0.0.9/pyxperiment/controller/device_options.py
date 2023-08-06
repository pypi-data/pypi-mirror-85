"""
    pyxperiment/controller/device_options.py:
    The base classes for options - device specific data entities

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

from abc import ABCMeta, abstractmethod
from copy import copy
from .validation import EmptyValidator

class DeviceOption(metaclass=ABCMeta):
    """
    Device option, that generally can not be used for a sweep,
    only in editor, abstract base class
    """

    def __init__(self, name, get_func=None, set_func=None, enabled=None):
        self._name = name
        self._fget = get_func
        self._fset = set_func
        self._enabled = enabled
        self.device = None

    @property
    def name(self):
        """The name of the current option"""
        return self._name

    @abstractmethod
    def get_value(self):
        """
        Retrieve the option value
        """

    @abstractmethod
    def set_value(self, value):
        """
        Set the option value
        """

    def is_enabled(self):
        """
        Is the option modification allowed
        """
        if self._enabled is None:
            return True
        return self._enabled(self.device)

    def is_readable(self):
        """
        Readable option can be only read
        """
        return self._fset is None

    def is_writable(self):
        """
        Writable option can be set
        """
        return self._fset is not None

    def with_instance(self, device):
        """
        Used to instantiate options when a specific device is created
        """
        #pylint: disable=W0212
        ret = copy(self)
        ret.device = device
        if self._fset is not None:
            ret._fset = lambda value, set_func=self._fset, instr=device: set_func(instr, value)
        if self._fget is not None:
            ret._fget = lambda get_func=self._fget, instr=device: get_func(instr)
        return ret

    def description(self):
        """
        Get the description tuple array
        """
        ret = self.device.description()
        ret.append(('Property', self._name))
        return ret

    def driver_name(self):
        return self.device.driver_name()

    def device_name(self):
        return self.device.device_name()

    def device_id(self):
        return self.device.device_id()

    def is_sweep_based(self):
        return False

    @property
    def location(self):
        return self.device.location

    def to_remote(self):
        self.device.to_remote()

    def to_local(self):
        self.device.to_local()

class ListDeviceOption(DeviceOption):
    """Device option, that accepts only values, present
    in a special list
    TODO: must implement all checks of elements """

    def __init__(self, name, values_list, get_func=None, set_func=None, enabled=None):
        super().__init__(name, get_func, set_func, enabled)
        self._values_list = values_list

    def values_list(self):
        """return the list of the valid values"""
        return self._values_list

    def get_value(self):
        return self._fget()

    def set_value(self, value):
        self._fset(value)

class ListOption(ListDeviceOption):
    """
    List device option that does data conversion internally
    """

    def get_value(self):
        value = self._fget()
        return self._values_list[int(value)]

    def set_value(self, value):
        if value in self._values_list:
            self._fset(str(self._values_list.index(value)))
        else:
            raise ValueError('Invalid value for ' + self.name + ': ' + value)

class BooleanDeviceOption(DeviceOption):
    """
    Device option, that accepts only two values:
    true or false
    """

    def get_value(self):
        return self._fget()

    def set_value(self, value):
        self._fset(value) 

class BooleanOption(BooleanDeviceOption):
    """
    Device option, that accepts only two values:
    true or false, and does data conversion internally
    """

    def __init__(
            self, name, get_func=None, set_func=None, enabled=None,
            true_str='1', false_str='0'
        ):
        super().__init__(name, get_func, set_func, enabled)
        self.true_str = true_str
        self.false_str = false_str

    def get_value(self):
        value = self._fget()
        int_value = int(value)
        if int_value == 1:
            return True
        if int_value == 0:
            return False
        raise ValueError('Bad value for ' + self.name + ': "' + str(value) + '"')

    def set_value(self, value):
        self._fset(self.true_str if value else self.false_str)

class ValueDeviceOption(DeviceOption):
    """
    Device option, that repesents a numerical value of physical
    quantity (a valid x for a sweep).
    """

    def __init__(
            self, name, phys_q, get_func=None, set_func=None, channels=1,
            validator=EmptyValidator, enabled=None, sweepable=True
        ):
        super().__init__(name, get_func, set_func, enabled)
        self._phys_q = phys_q
        self._validator = validator
        self._channels = channels
        self._sweepable = sweepable

    def phys_quantity(self):
        """
        Get physical quantity (if applicable)
        """
        return self._phys_q

    def get_value(self):
        return self._fget()

    def set_value(self, value):
        self._fset(value)

    def is_sweepable(self):
        return self._sweepable

    def check_values(self, values):
        """
        Check the ability to set all the values present in collection
        """
        return self._validator.check_values(values)

    @property
    def channels_num(self):
        """
        Return the length of the output data vector
        """
        return self._channels

class StateDeviceOption(DeviceOption):
    """
    Device option, that can only be read, and represents
    certain state (string)
    """

    def __init__(self, name, fget, enabled=None):
        super().__init__(name, fget, None, enabled)

    def get_value(self):
        return self._fget()

    def set_value(self, value):
        raise NotImplementedError('set_value not valid for StateDeviceOption')

class ActionDeviceOption(DeviceOption):
    """
    Device option, that can only be set (activated), and
    represents certain action/state transition
    """

    def __init__(self, name, fset):
        super().__init__(name, None, fset)

    def get_value(self):
        raise NotImplementedError('get_value not valid for ActionDeviceOption')

    def set_value(self, value=None):
        self._fset()

class TimeoutOption(ValueDeviceOption):
    """
    A special property, representing timeout for another property
    """

    def __init__(self, option):
        super().__init__(
            'Timeout', 'ms', None, None, sweepable=False
        )
        # Value is set externally by ControlField
        self.value = None
        self.option = option
        option.read_timeout = self

    def get_value(self):
        if not self.value:
            return ''
        return str(round((self.value)*1000, 2))
