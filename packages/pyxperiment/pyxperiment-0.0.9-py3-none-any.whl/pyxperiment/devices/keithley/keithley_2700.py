"""
    pyxperiment/devices/keithley/keithley2700.py: Support for Keithley 2700 DMM

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

from decimal import Decimal
import time

import wx
from wx.lib.scrolledpanel import ScrolledPanel

from pyxperiment.controller import VisaInstrument
from pyxperiment.frames.device_config import DeviceConfig
from pyxperiment.frames.basic_panels import (
    CaptionTextPanel, CaptionDropBox, ModifiedCheckBox
)

class Keithley2700DMM(VisaInstrument):
    """
    Keithley 2700 DMM support
    """

    def __init__(self, rm, resource):
        super().__init__(rm, resource)
        self.clear_buf(4)
        self.inst.write_termination = '\n'
        self.inst.read_termination = '\n'
        self.write('*CLS')
        self.write('INIT:CONT OFF')
        self.write('TRAC:CLE')
        self.write('FORM:ELEM READ')
        self.write('TRIG:SOUR IMM')
        self.idn = self.query_id().translate({ord(c): None for c in ['\r', '\n']}).split(',')
        if not self.get_scan_enable():
            self.channels_num = 1
        else:
            self.channels_num = len(self.__channelstr_to_list(self.get_scanlist()))

    @staticmethod
    def driver_name():
        return 'Keithley 270x DMM'

    def query(self, data):
        with self.lock:
            self.inst.write(data, '\n')
            stb = self.inst.read_stb()
            tries = 0
            while (not stb & (1 << 4)) and tries < 100:
                stb = self.inst.read_stb()
                tries += 1
                time.sleep(0.001)
            value = self.inst.read()
        return value

    @staticmethod
    def __get_channel_str(channel):
        return ' (@'+str(channel)+')' if channel is not None else ''

    @staticmethod
    def __set_channel_str(channel):
        return ',(@'+str(channel)+')' if channel is not None else ''

    @staticmethod
    def __channelstr_to_list(chstr):
        chstr = chstr.translate({ord(c): None for c in ['(', ')', '@']})
        if chstr.find(':') != -1:
            parts = chstr.split(':')
            start = int(parts[0])
            end = int(parts[1])
            return [str(i) for i in range(start, end+1)]
        return chstr.split(',')

    def device_name(self):
        return self.idn[0].title() + ' ' + self.idn[1].title() + ' DMM'

    def device_id(self):
        return self.idn[2]

    def reset(self):
        self.write('*RST')

    def set_scanlist(self, value):
        self.write('ROUT:SCAN ' + value)

    def get_scanlist(self):
        return self.query('ROUT:SCAN?')

    def get_scan_enable(self):
        value = self.query('ROUT:SCAN:LSEL?')
        if value == 'INT':
            return True
        elif value == 'NONE':
            return False
        raise ValueError('Bad ROUT:SCAN:LSEL value: "' + str(value) + '"')

    def set_scan_enable(self, value):
        self.write('INIT:CONT OFF')
        self.write('TRAC:CLE')
        self.write('TRIG:COUN 1')
        if value:
            self.channels_num = len(self.__channelstr_to_list(self.get_scanlist()))
            self.write('SAMP:COUN ' + str(self.channels_num))
            self.write('ROUT:SCAN:TSO IMM')
        else:
            self.channels_num = 1
            self.write('SAMP:COUN 1')
        self.write('ROUT:SCAN:LSEL ' + ('INT' if value else 'NONE'))

    def get_highz(self):
        return not self._query_boolean('SENS:VOLT:IDIV?')

    def set_highz(self, value):
        self.write('SENS:VOLT:IDIV ' + ('OFF' if value else 'ON'))

    def get_autozero(self):
        return self._query_boolean('SYST:AZER:STAT?')

    def set_autozero(self, value):
        self.write('SYST:AZER:STAT ' + ('1' if value else '0'))

    def set_resolution(self, value, channel=None):
        self.write('VOLT:DIG ' + str(value) + self.__set_channel_str(channel))

    def get_resolution(self, channel=None):
        value = self.query('VOLT:DIG?' + self.__get_channel_str(channel))
        return value

    def set_autorange(self, value, channel=None):
        self.write('VOLT:RANG:AUTO ' + ('ON' if value else 'OFF') + self.__set_channel_str(channel))

    def get_autorange(self, channel=None):
        return self._query_boolean('VOLT:RANG:AUTO?' + self.__get_channel_str(channel))

    range_values = [
        '1010',
        '100',
        '10',
        '1',
        '0.1'
        ]

    def set_range(self, value, channel=None):
        if value in self.range_values:
            self.write('VOLT:RANG ' + value + self.__set_channel_str(channel))
        else:
            raise ValueError('Invalid range.')

    def get_range(self, channel=None):
        value = self.query('VOLT:RANG?' + self.__get_channel_str(channel))
        for range_value in self.range_values:
            if Decimal(range_value) == Decimal(value):
                return range_value
        raise ValueError('Unkwown range ' + value)

    def set_nplc(self, value, channel=None):
        self.write('VOLT:NPLC ' + str(value) + self.__set_channel_str(channel))

    def get_nplc(self, channel=None):
        value = self.query('VOLT:NPLC?' + self.__get_channel_str(channel))
        return value

    def get_value(self):
        value = self.query('INIT:CONT OFF\nREAD?').translate({ord(c): None for c in ['\r', '\n']})
        return value.split(',') if self.channels_num > 1 else value

    def init_get_value(self):
        self.write('INIT:CONT OFF\nREAD?')

    def end_get_value(self):
        value = self.read().translate({ord(c): None for c in ['\r', '\n']})
        return value.split(',') if self.channels_num > 1 else value

    def get_func(self, channel=None):
        value = self.query('FUNC?' + self.__get_channel_str(channel))
        return value

    def to_local(self):
        pass
        #import pyvisa
        #TODO: to_local breaks things when in scan mode
        #self.inst.control_ren(pyvisa.constants.VI_GPIB_REN_ADDRESS_GTL)

    def get_config_class(self):
        return Keithley2700DMMConfig

class Keithley2700DMMConfig(DeviceConfig):

    class ChannelPanel(wx.Panel):
        def __init__(self, parent, device, channel):
            super().__init__(parent, wx.ID_ANY)
            self.channel_num = channel
            self.device = device

            label = wx.StaticText(self, label=('Channel: '+str(channel)))

            self.function = CaptionTextPanel(self, 'Function')
            self.autorange = ModifiedCheckBox(self, label='Auto Range')
            self.range = CaptionDropBox(self, 'Range, V', Keithley2700DMM.range_values)
            self.resolution = CaptionTextPanel(self, 'Resolution, digits')
            self.nplc = CaptionTextPanel(self, 'Power cycles')

            sizer = wx.BoxSizer(wx.VERTICAL)
            sizer.Add(label, 1, wx.ALL | wx.GROW, 10)
            sizer.Add(self.function, flag=wx.ALL | wx.GROW)
            sizer.Add(self.autorange, flag=wx.ALL | wx.GROW)
            sizer.Add(self.range, flag=wx.ALL | wx.GROW)
            sizer.Add(self.resolution, flag=wx.ALL | wx.GROW)
            sizer.Add(self.nplc, flag=wx.ALL | wx.GROW)

            if channel is None:
                sizer.AddSpacer(20)

            self.SetSizer(sizer)
            sizer.Fit(self)

        def get_channel_num(self):
            return self.channel_num

        def read_control(self):
            self.function.SetValue(self.device.get_func(self.channel_num))
            self.nplc.SetValue(self.device.get_nplc(self.channel_num))
            self.range.SetValue(self.device.get_range(self.channel_num))
            self.resolution.SetValue(self.device.get_resolution(self.channel_num))
            self.autorange.SetValue(self.device.get_autorange(self.channel_num))
            self.range.SetEnabled(not self.autorange.Value)

        def write_control(self):
            if self.nplc.IsModified():
                self.device.set_nplc(self.nplc.GetValue(), self.channel_num)
            if self.range.IsModified():
                self.device.set_range(self.range.GetValue(), self.channel_num)
            if self.resolution.IsModified():
                self.device.set_resolution(self.resolution.GetValue(), self.channel_num)
            if self.autorange.IsModified():
                self.device.set_autorange(self.autorange.Value, self.channel_num)

    def __init__(self, parent, device):
        super().__init__(parent, device, 1000)

    def _init_view(self):
        self._create_panel()
        self.channels = CaptionTextPanel(self.panel, label='Scan channels', size=(-1, -1))
        self.autozero = ModifiedCheckBox(self.panel, label='Auto Zero')
        self.highz = ModifiedCheckBox(self.panel, label='High Z')
        self.scanenable = ModifiedCheckBox(self.panel, label='Enable Scan')
        self.value = CaptionTextPanel(self.panel, 'Value, V', size=(120, -1))
        self.value.SetEnabled(False)
        self.timeout = CaptionTextPanel(self.panel, 'Timeout, ms')
        self.timeout.SetEnabled(False)
        self.channel_panels = []
        self.vbox = wx.BoxSizer(wx.VERTICAL)
        self.vbox.Add(self.name, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 10)
        self.vbox.Add(self.location, 0, wx.ALIGN_CENTER_HORIZONTAL, 0)
        self.vbox.Add(self.channels, border=10, flag=wx.ALL |wx.ALIGN_CENTER_HORIZONTAL | wx.GROW)
        self.vbox.Add(self.autozero, border=5, flag=wx.ALL |wx.ALIGN_CENTER_HORIZONTAL)
        self.vbox.Add(self.highz, border=5, flag=wx.ALL |wx.ALIGN_CENTER_HORIZONTAL)
        self.vbox.Add(self.scanenable, border=5, flag=wx.ALL |wx.ALIGN_CENTER_HORIZONTAL)

        self.no_channel_panel = Keithley2700DMMConfig.ChannelPanel(self.panel, self.device, None)

        self.scroll_panel = ScrolledPanel(self.panel, size=wx.Size(-1, -1))
        self.scroll_panel.SetupScrolling()
        self.hbox_channels = wx.BoxSizer(wx.HORIZONTAL)
        self.scroll_panel.SetSizer(self.hbox_channels)
        self.hbox_channels.Fit(self.scroll_panel)

        self.hbox_measure = wx.BoxSizer(wx.HORIZONTAL)
        self.hbox_measure.Add(self.no_channel_panel, 1, border=10, flag=wx.ALL | wx.GROW)
        self.hbox_measure.AddSpacer(10)
        self.hbox_measure.Add(self.scroll_panel, 2, border=10, flag=wx.ALL | wx.GROW)

        self.vbox.Add(self.hbox_measure, flag=wx.ALIGN_CENTER_HORIZONTAL | wx.GROW)
        self.hbox_value = wx.BoxSizer(wx.HORIZONTAL)
        self.hbox_value.Add(self.value, 1, border=10, flag=wx.TOP | wx.GROW)
        self.hbox_value.Add(self.timeout, 1, border=10, flag=wx.TOP | wx.GROW)
        self.vbox.Add(self.hbox_value, flag=wx.ALIGN_CENTER_HORIZONTAL | wx.GROW)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(self.btn_save, 0, flag=wx.ALIGN_CENTER_HORIZONTAL | wx.LEFT)
        hbox.Add(self.btn_load, 0, flag=wx.ALIGN_CENTER_HORIZONTAL | wx.RIGHT)
        self.vbox.Add(hbox, 0, flag=wx.ALIGN_CENTER_HORIZONTAL | wx.TOP)
        self.vbox.AddSpacer(10)
        self.panel.SetSizer(self.vbox)
        self.__init_sizer__()

    def __init_sizer__(self):
        for panel in self.channel_panels:
            self.hbox_channels.Add(panel, flag=wx.TOP | wx.GROW)
        self.vbox.Fit(self)
        self.vbox.Layout()
        self.Fit()

    def read_control(self):
        channels = self.device.get_scanlist()
        self.channels.SetValue(channels)
        channels = channels.translate({ord(c): None for c in ['(', ')', '@']})
        if channels.find(':') != -1:
            parts = channels.split(':')
            start = int(parts[0])
            end = int(parts[1])
            channels = [str(i) for i in range(start, end+1)]
        else:
            channels = channels.split(',')

        self.autozero.SetValue(self.device.get_autozero())
        self.scanenable.SetValue(self.device.get_scan_enable())
        self.highz.SetValue(self.device.get_highz())

        self.hbox_channels.Clear(True)
        self.channel_panels = []
        for i in channels:
            self.channel_panels.append(
                Keithley2700DMMConfig.ChannelPanel(self.scroll_panel, self.device, int(i))
                )

        self.__init_sizer__()

        self.no_channel_panel.read_control()
        for panel in self.channel_panels:
            panel.read_control()

    def write_control(self):
        self.no_channel_panel.write_control()
        for panel in self.channel_panels:
            panel.write_control()

        self.device.set_autozero(self.autozero.GetValue())
        self.device.set_scan_enable(self.scanenable.GetValue())
        self.device.set_highz(self.highz.GetValue())

        if self.channels.IsModified():
            self.device.set_scanlist(self.channels.GetValue())

    def on_reload_timer(self, event):
        del event
        start_time = time.perf_counter()
        val = self.device.get_value()
        end_time = time.perf_counter()
        self.timeout.SetValue(str(Decimal(end_time - start_time)*Decimal('1000')))
        if not isinstance(val, list):
            self.value.SetValue(val)
        else:
            self.value.SetValue(', '.join(val))
