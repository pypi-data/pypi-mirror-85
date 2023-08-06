"""
    pyxperiment/settings/group_settings.py:
    This module declares programm setting groups, accessible elsewhere via
    core_settings module

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

from .xml_settings import (
    XMLSetting, XMLSettingBoolean, XMLSettingsBundle, XMLSettingsArray
)

class ExperimentSettings(XMLSettingsBundle):
    """
    This class declares basic experiment properties
    """
    def __init__(self):
        super().__init__(
            'experiment',
            [
                XMLSetting('iterations', '1'),
                XMLSetting('iterationsDelay', '0'),
                XMLSettingBoolean('backsweep', 'False'),
                XMLSettingBoolean('doublesweep', 'False'),
                XMLSettingBoolean('fastAsColumns', 'False'),
                XMLSettingBoolean('cumulativeView', 'False')
                ]
        )

class DeviceSweepSettings(XMLSettingsBundle):
    """
    Sweep settings for a single x device
    """
    def __init__(self):
        super().__init__(
            'sweep',
            [
                XMLSetting('range', ''),
                XMLSetting('delay', '0'),
                XMLSetting('returnDelay', '0.1')
                ]
        )

class DevicePropertySettings(XMLSettingsBundle):
    """
    A list of settings, attributed to single device property
    """
    def __init__(self):
        super().__init__(
            'property',
            [
                XMLSetting('name', ''),
                DeviceSweepSettings()
                ]
        )

class DeviceSetting(XMLSettingsBundle):
    """
    A list of settings, attributed to single device
    """
    def __init__(self):
        super().__init__(
            'instrument',
            [
                XMLSetting('name', ''),
                XMLSetting('serial', ''),
                XMLSetting('address', ''),
                XMLSetting('driverName', ''),
                DeviceSweepSettings(),
                XMLSettingsArray('properties', DevicePropertySettings)
                ]
        )

class DeviceSettingsArray(XMLSettingsArray):
    """
    A list of device settings
    """
    def __init__(self):
        super().__init__(
            'instruments',
            DeviceSetting
        )

    def find_device_settings(self, location, driver):
        """
        Special method to find a device based on it's location and driver name
        """
        if not location == '':
            for device in self.children:
                if device.address == location:
                    return device
        else:
            for device in self.children:
                if device.driverName == driver:
                    return device
        return None
        