"""
    pyxperiment/devices/smxxxx.py:
    Support for Delta Electronica SM800/SM3300 power source

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

import time
import threading
from decimal import Decimal

from pyxperiment.controller import TcpSocketInstrument
from pyxperiment.controller.device_options import (
    ValueDeviceOption, BooleanOption
)

class DeltaSMxxxxPS(TcpSocketInstrument):
    """
    SM800/SM3300 power source support
    """

    DEFAULT_PORT = 8462
    channels_num = 1

    def __init__(self, rm, resource):
        super().__init__(resource, 9191)
        self.model = self.query_id().translate({ord(c): None for c in ['\r', '\n']}).split(',')[1]
        if self.model.startswith('PSC ETH'):
            self.write('syst:rem:cv rem')
            self.write('syst:rem:cc rem')
        else:
            self.write('syst:rem:cv eth')
            self.write('syst:rem:cc eth')
        self._finished = True
        self._target_curr = self.get_curr_limit()
        self._speed = None
        self.set_options([
            ValueDeviceOption('Max. Voltage', 'V', self.get_volt_max),
            ValueDeviceOption('Max. Current', 'A', self.get_curr_max),
            ValueDeviceOption('Set Voltage', 'V',
                              self.get_volt_limit, self.set_volt_limit),
            ValueDeviceOption('Set Current', 'A',
                              self.get_curr_limit, self.set_curr_limit),
            ValueDeviceOption('Scan speed', 'A/min',
                              self.get_scan_speed, self.set_scan_speed),
            self.voltage,
            self.current,
            self.output
        ])

    @staticmethod
    def driver_name():
        return 'SM800/SM3300 power source (' + str(DeltaSMxxxxPS.DEFAULT_PORT) + ')'

    def device_name(self):
        value = self.query_id().translate({ord(c): None for c in ['\r', '\n']}).split(',')
        return value[0] + ' ' + value[1] + ' power source'

    output = BooleanOption(
        'Output on',
        get_func=lambda instr: instr.query('output?'),
        set_func=lambda instr, value: instr.write('output ' + value),
        true_str='ON',
        false_str='OFF'
    )

    def get_volt_max(self):
        return self.query('sour:volt:max?')

    def get_curr_max(self):
        return self.query('sour:curr:max?')

    def set_volt_limit(self, value):
        self.write('sour:volt ' + str(value))

    def get_volt_limit(self):
        return self.query('sour:volt?')

    def set_curr_limit(self, value):
        self.write('sour:curr ' + str(value))

    def get_curr_limit(self):
        return self.query('sour:curr?')

    def get_curr(self):
        return self.query('meas:curr?')

    def get_volt(self):
        return self.query('meas:volt?')

    def get_scan_speed(self):
        return '' if self._speed is None else str(self._speed)

    def set_scan_speed(self, value):
        self._speed = float(value)

    def _set_current_task(self, target_value):
        step = Decimal('0.001')
        target_value = Decimal(target_value)
        sleep_time = float(Decimal('60')*step/Decimal(self._speed))
        value = Decimal(self.get_curr_limit())
        reference_time = time.perf_counter()
        desired_time = 0
        while (not self._stop_thread) and (value != target_value):
            if value < target_value:
                value += step
            elif value > target_value:
                value -= step
            self.set_curr_limit(value)
            elapsed_time = time.perf_counter() - reference_time
            desired_time = desired_time + sleep_time
            if float(desired_time) > elapsed_time:
                time.sleep(float(desired_time) - elapsed_time)
        self._finished = True

    def set_value(self, value):
        if not self._finished:
            self._stop_thread = True
            while not self._finished:
                time.sleep(0.001)
        self._stop_thread = False
        self._finished = False
        self._thread = threading.Thread(target=self._set_current_task, args=(value,))
        self._thread.start()

    def get_value(self):
        return self.get_curr_limit()

    def get_field(self):
        return self.get_curr_limit()

    def get_target_field(self):
        if self._speed is None:
            import wx
            dlg = wx.TextEntryDialog(
                None,
                'Enter SMxxxx current sweep speed, A/min',
                'SMxxxx sweep speed'
                )
            dlg.SetValue("1")
            dlg.ShowModal()
            self._speed = dlg.GetValue()
            dlg.Destroy()
        return self.get_curr_limit()

    def finished(self):
        return self._finished

    def stop(self):
        if not self._finished:
            self._stop_thread = True
            while not self._finished:
                time.sleep(0.001)

    current = ValueDeviceOption('Output current', 'A', get_curr)
    voltage = ValueDeviceOption('Output voltage', 'V', get_volt)
