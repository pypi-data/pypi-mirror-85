"""
    pyxperiment/settings/core_settings.py:
    The core module for PyXperiment settings management

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

import platform
import logging
from lxml import etree
from .group_settings import DeviceSettingsArray, ExperimentSettings

class CoreSettings(object):
    """Base class, defines settings storage and hierarchy"""

    SETTINGS_FILENAME = 'settings.xml'
    ROOT_ELEMENT_NAME = 'settings'
    RESOURCE_MANAGER_NAME = 'resourceManager'
    READERS_NAME = 'readers'
    WRITERS_NAME = 'writers'

    @staticmethod
    def __get_root():
        try:
            root = etree.parse(CoreSettings.SETTINGS_FILENAME, etree.XMLParser(remove_blank_text=True)).getroot()
        except Exception:
            logging.exception("Error reading settings file: ")
            root = etree.Element(CoreSettings.ROOT_ELEMENT_NAME)
        return root

    @staticmethod
    def __get_element(root, name):
        path = root.find(name)
        if path is None:
            path = etree.SubElement(root, name)
        return path

    @staticmethod
    def get_device_settings():
        try:
            root = etree.parse(CoreSettings.SETTINGS_FILENAME, etree.XMLParser(remove_blank_text=True)).getroot()
            deviceSettings = DeviceSettingsArray().from_xml_element(root)
        except Exception:
            deviceSettings = DeviceSettingsArray()
            CoreSettings.set_device_settings(deviceSettings)
        return deviceSettings

    @staticmethod
    def set_device_settings(value):
        root = CoreSettings.__get_root()
        root.remove(CoreSettings.__get_element(root, value.get_xml_name()))
        value.to_xml_element(root)
        etree.ElementTree(root).write(CoreSettings.SETTINGS_FILENAME, method='xml', pretty_print=True)

    @staticmethod
    def get_last_path():
        try:
            root = etree.parse(CoreSettings.SETTINGS_FILENAME, etree.XMLParser(remove_blank_text=True)).getroot()
            return root.find("lastPath").text
        except Exception:
            if platform.system() == 'Windows':
                path = "C:\\test\\test*.dat"
            else:
                path = '~/test/test*.dat'
            CoreSettings.set_last_path(path)
            return path

    @staticmethod
    def set_last_path(value):
        root = CoreSettings.__get_root()
        path = CoreSettings.__get_element(root, "lastPath")
        path.text = value
        etree.ElementTree(root).write(CoreSettings.SETTINGS_FILENAME, method='xml', pretty_print=True)

    @staticmethod
    def get_spm_enabled():
        try:
            root = etree.parse(CoreSettings.SETTINGS_FILENAME, etree.XMLParser(remove_blank_text=True)).getroot()
            return root.find('spmEnabled').text.lower() in 'true'
        except Exception:
            CoreSettings.set_spm_enabled(False)
            return False

    @staticmethod
    def set_spm_enabled(value):
        root = CoreSettings.__get_root()
        path = CoreSettings.__get_element(root, 'spmEnabled')
        path.text = 'True' if value else 'False'
        etree.ElementTree(root).write(CoreSettings.SETTINGS_FILENAME, method='xml', pretty_print=True)

    @staticmethod
    def get_sweep_settings():
        try:
            root = etree.parse(CoreSettings.SETTINGS_FILENAME, etree.XMLParser(remove_blank_text=True)).getroot()
            settings = ExperimentSettings()
            settings.from_xml_element(root)
        except Exception:
            settings = ExperimentSettings()
            CoreSettings.set_sweep_settings(settings)
        return settings

    @staticmethod
    def set_sweep_settings(value):
        root = CoreSettings.__get_root()
        root.remove(CoreSettings.__get_element(root, value.get_xml_name()))
        value.to_xml_element(root)
        etree.ElementTree(root).write(CoreSettings.SETTINGS_FILENAME, method='xml', pretty_print=True)

    @staticmethod
    def get_resource_manager():
        try:
            root = etree.parse(CoreSettings.SETTINGS_FILENAME, etree.XMLParser(remove_blank_text=True)).getroot()
            manager_name = root.find(CoreSettings.RESOURCE_MANAGER_NAME).text
        except Exception:
            if platform.system() == 'Windows':
                manager_name = 'agvisa32.dll'
            else:
                manager_name = '@ni'
            CoreSettings.set_resource_manager(manager_name)
        return manager_name

    @staticmethod
    def set_resource_manager(value):
        root = CoreSettings.__get_root()
        CoreSettings.__get_element(root, CoreSettings.RESOURCE_MANAGER_NAME).text = value
        etree.ElementTree(root).write(CoreSettings.SETTINGS_FILENAME, method='xml', pretty_print=True)

    @staticmethod
    def get_readers():
        try:
            root = etree.parse(CoreSettings.SETTINGS_FILENAME, etree.XMLParser(remove_blank_text=True)).getroot()
            readers = (int)(root.find(CoreSettings.READERS_NAME).text)
        except Exception:
            readers = 3
            CoreSettings.set_readers((str)(readers))
        return readers

    @staticmethod
    def set_readers(value):
        root = CoreSettings.__get_root()
        CoreSettings.__get_element(root, CoreSettings.READERS_NAME).text = value
        etree.ElementTree(root).write(CoreSettings.SETTINGS_FILENAME, method='xml', pretty_print=True)

    @staticmethod
    def get_writers():
        try:
            root = etree.parse(CoreSettings.SETTINGS_FILENAME, etree.XMLParser(remove_blank_text=True)).getroot()
            writers = (int)(root.find(CoreSettings.WRITERS_NAME).text)
        except Exception:
            writers = 3
            CoreSettings.set_writers((str)(writers))
        return writers

    @staticmethod
    def set_writers(value):
        root = CoreSettings.__get_root()
        CoreSettings.__get_element(root, CoreSettings.WRITERS_NAME).text = value
        etree.ElementTree(root).write(CoreSettings.SETTINGS_FILENAME, method='xml', pretty_print=True)
