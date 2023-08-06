"""
    pyxperiment/devices/sr72x5.py:
    Support for Signal Recovery 7225/7265 DSP Lock-In Amplifier

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

from pyxperiment.controller import VisaInstrument
from pyxperiment.controller.device_options import (
    ListDeviceOption, ValueDeviceOption, StateDeviceOption
)

class SR7225DSPLockIn(VisaInstrument):
    """
    Signal Recovery SR7225/SR7265 support
    """

    @staticmethod
    def driver_name():
        return 'SR7225/7265 DSP Lock-In'

    def __init__(self, rm, resource):
        super().__init__(rm, resource)
        self.clear_buf(7)
        self.query('GP')
        self._model = self.query_id()
        self.set_options([
            ValueDeviceOption(
                'Oscillator frequency', 'Hz', self.get_osc_frequency,
                self.set_osc_frequency),
            ValueDeviceOption(
                'Oscillator amplitude', 'V', self.get_osc_amplitude,
                self.set_osc_amplitude),
            ListDeviceOption(
                'Tc', self.tc_values, self.get_tc, self.set_tc),
            ListDeviceOption(
                'Slope', self.slope_values,
                self.get_slope, self.set_slope),
            ListDeviceOption(
                'AC gain', self.ac_gain_values,
                self.get_ac_gain, self.set_ac_gain),
            ListDeviceOption(
                'Sensitivity', self.sensitivity_values,
                self.get_sensitivity, self.set_sensitivity),
            ValueDeviceOption(
                'Phase', 'deg',
                self.get_ref_phase, self.set_ref_phase),
            ValueDeviceOption(
                'Harmonic', None,
                self.get_ref_harmonic, self.set_ref_harmonic),
            ValueDeviceOption(
                'DAC 1', 'V',
                lambda dev=self: dev.get_dac_value(1), lambda x, dev=self: dev.set_dac_value(1, x)),
            ValueDeviceOption(
                'DAC 2', 'V',
                lambda dev=self: dev.get_dac_value(2), lambda x, dev=self: dev.set_dac_value(2, x)),
            StateDeviceOption('Value', lambda dev=self: str(dev.get_value())),#, ['X, V', 'Y, V']),self.x.SetValue(value[0])self.y.SetValue(value[1])
            StateDeviceOption('Overload', lambda dev=self: ', '.join(dev.get_overload()))
        ])

    def query_id(self):
        return self.query('ID')

    def device_name(self):
        return 'SR' + self._model + ' DSP Lock-in'

    def query(self, data):
        self.inst.write(data, '\n')
        stb = self.read_stb()
        tries = 0
        while (not stb & (1 << 7)) and tries < 100:
            stb = self.read_stb()
            tries += 1
        value = self.read()
        return value.translate(
            {ord(c): None for c in ['\r', '\n']} if
            data.find('.') == -1 else {ord(c): None for c in ['\r', '\n', chr(0)]}
            )

    def get_overload(self):
        value = int(self.query('N'))
        overload_str = []
        if value & (1 << 1):
            overload_str.append('CH1 output')
        if value & (1 << 2):
            overload_str.append('CH2 output')
        if value & (1 << 3):
            overload_str.append('Y output')
        if value & (1 << 4):
            overload_str.append('X output')
        if value & (1 << 6):
            overload_str.append('Input')
        if value & (1 << 7):
            overload_str.append('Reference unlock')
        return overload_str

    def get_value(self):
        value = self.query('XY.')
        if self.read_stb() & (1 << 4):
            return ['Inf', 'Inf']
        return value.split(',')

    sensitivity_values = [
        '2 nV',
        '5 nV',
        '10 nV',
        '20 nV',
        '50 nV',
        '100 nV',
        '200 nV',
        '500 nV',
        '1 uV',
        '2 uV',
        '5 uV',
        '10 uV',
        '20 uV',
        '50 uV',
        '100 uV',
        '200 uV',
        '500 uV',
        '1 mV',
        '2 mV',
        '5 mV',
        '10 mV',
        '20 mV',
        '50 mV',
        '100 mV',
        '200 mV',
        '500 mV',
        '1 V'
        ]

    def get_sensitivity(self):
        value = int(self.query('SEN'))
        return self.sensitivity_values[value-1]

    def set_sensitivity(self, value):
        if value in self.sensitivity_values:
            self.write('SEN ' + str(self.sensitivity_values.index(value)+1))
        else:
            raise ValueError('Invalid sensitivity.')

    ac_gain_values = [
        '0 dB', '10 dB', '20 dB',
        '30 dB', '40 dB', '50 dB',
        '60 dB', '70 dB', '80 dB', '90 dB'
        ]

    def get_ac_gain(self):
        value = int(self.query('ACGAIN'))
        return self.ac_gain_values[value]

    def set_ac_gain(self, value):
        if value in self.ac_gain_values:
            self.write('ACGAIN ' + str(self.ac_gain_values.index(value)))
        else:
            raise ValueError('Invalid ac gain.')

    slope_values = [
        '6 dB/octave', '12 dB/octave', '18 dB/octave', '24 dB/octave'
        ]

    def get_slope(self):
        value = int(self.query('SLOPE'))
        return self.slope_values[value]

    def set_slope(self, value):
        if value in self.slope_values:
            self.write('SLOPE ' + str(self.slope_values.index(value)))
        else:
            raise ValueError('Invalid slope.')

    tc_values = [
        '10 us', '20 us', '40 us', '80 us', '160 us', '320 us',
        '640 us', '5 ms', '10 ms', '20 ms', '50 ms', '100 ms',
        '200 ms', '500 ms', '1 s', '2 s', '5 s', '10 s',
        '20 s', '50 s', '100 s', '200 s', '500 s', '1 ks',
        '2 ks', '5 ks', '10 ks', '20 ks', '50 ks', '100 ks'
        ]

    def get_tc(self):
        value = int(self.query('TC'))
        return self.tc_values[value]

    def set_tc(self, value):
        if value in self.tc_values:
            self.write('TC ' + str(self.tc_values.index(value)))
        else:
            raise ValueError('Invalid time constant.')

    def get_osc_amplitude(self):
        value = self.query('OA.')
        return value

    def set_osc_amplitude(self, value):
        self.write('OA. ' + str(value))

    def get_osc_frequency(self):
        return self.query('OF.')

    def set_osc_frequency(self, value):
        self.write('OF. ' + str(value))

    def get_ref_harmonic(self):
        return self.query('REFN')

    def set_ref_harmonic(self, value):
        self.write('REFN ' + str(value))

    def get_ref_phase(self):
        return self.query('REFP.')

    def set_ref_phase(self, value):
        self.write('REFP. ' + str(value))

    def get_dac_value(self, dac):
        return self.query('DAC. ' + str(dac))

    def set_dac_value(self, dac, value):
        self.write('DAC. ' + str(dac) + ' ' + str(value))

    x_y = ValueDeviceOption('X,Y', 'V', get_value, None, 2)

    frequency = ValueDeviceOption(
        'Frequency', 'Hz',
        lambda x: x.get_osc_frequency(),
        lambda x, val: x.set_osc_frequency(val)
        )

    analog_out = [
        ValueDeviceOption(
            'ANALOG OUT ' + str(i), 'V',
            lambda x, ch=i: x.get_dac_value(ch),
            lambda x, val, ch=i: x.set_dac_value(ch, val)
        )  for i in range(1, 3)]
