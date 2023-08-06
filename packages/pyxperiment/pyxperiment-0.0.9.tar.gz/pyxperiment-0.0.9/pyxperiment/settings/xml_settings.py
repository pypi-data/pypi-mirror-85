"""This module declares basic xml-based setting handling routines"""
from lxml import etree

class XMLSettingBase(object):
    """A base class for all xml elements"""

    def __init__(self, name):
        self.__name = name

    def get_xml_name(self):
        return self.__name

    def from_xml_element(self, element, is_root=False):
        """
        Convert from xml to object
        """
        if is_root:
            return element
        ret = element.find(self.__name)
        if ret is None:
            ret = etree.SubElement(element, self.__name)
        return ret

    def to_xml_element(self, element):
        """
        Convert current object to xml element
        """
        return etree.SubElement(element, self.__name)

class XMLSetting(XMLSettingBase):
    """A single string-type setting"""
    def __init__(self, name, default):
        super().__init__(name)
        self.default = default
        self.value = default

    def from_xml_element(self, element, is_root=False):
        element = super().from_xml_element(element, is_root)
        self.value = element.text
        if self.value is None:
            self.value = self.default
        return self

    def to_xml_element(self, element):
        element = super().to_xml_element(element)
        element.text = str(self.value)
        return element

    def set_value(self, value):
        self.value = value

class XMLSettingBoolean(XMLSettingBase):
    """A single boolean-type setting"""

    TRUE_STR = 'true'
    FALSE_STR = 'false'

    def __init__(self, name, default):
        super().__init__(name)
        self.default = default.lower() in self.TRUE_STR
        self.value = self.default

    def from_xml_element(self, element, is_root=False):
        element = super().from_xml_element(element, is_root)
        self.value = element.text.lower()
        if self.value is None or not self.value in [self.TRUE_STR, self.FALSE_STR]:
            self.value = self.default
        self.value = self.value in self.TRUE_STR
        return self

    def to_xml_element(self, element):
        element = XMLSettingBase.to_xml_element(self, element)
        element.text = str(self.value)
        return element

    def set_value(self, value):
        self.value = value

class XMLSettingsBundle(XMLSettingBase):
    """A bundle of settings"""
    def __init__(self, name, settings):
        super().__init__(name)
        self.settings = settings
        for setting in self.settings:
            if isinstance(setting, XMLSetting) or isinstance(setting, XMLSettingBoolean):
                setattr(self, setting.get_xml_name(), setting.value)
            else:
                setattr(self, setting.get_xml_name(), setting)

    def from_xml_element(self, element, is_root=False):
        element = super().from_xml_element(element, is_root)
        for setting in self.settings:
            setting.from_xml_element(element)
            if isinstance(setting, (XMLSetting, XMLSettingBoolean)):
                setattr(self, setting.get_xml_name(), setting.value)
            else:
                setattr(self, setting.get_xml_name(), setting)
        return self

    def to_xml_element(self, element):
        element = XMLSettingBase.to_xml_element(self, element)
        for setting in self.settings:
            setting.value = getattr(self, setting.get_xml_name())
            setting.to_xml_element(element)
        return element

class XMLSettingsArray(XMLSettingBase):
    """
    A list of XML settings
    """

    def __init__(self, name, elem_class):
        super().__init__(name)
        self.elem_class = elem_class
        self.children = []

    def from_xml_element(self, element, is_root=False):
        element = super().from_xml_element(element, is_root)
        for elem in element.iter(self.elem_class().get_xml_name()):
            self.children.append(self.elem_class().from_xml_element(elem, True))
        return self

    def to_xml_element(self, element):
        element = XMLSettingBase.to_xml_element(self, element)
        for device in self.children:
            device.to_xml_element(element)

    def get_children(self):
        return self.children

    def add_child(self, child):
        self.children.append(child)

    def remove_child(self, settings):
        self.children.remove(settings)
        