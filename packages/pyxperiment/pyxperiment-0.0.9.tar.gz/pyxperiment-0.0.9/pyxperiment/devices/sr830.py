"""
    pyxperiment/devices/sr830.py:
    Support for SR830 DSP Lock-In Amplifier

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

class SR830DSPLockIn(VisaInstrument):
    """
    SR830 DSP Lock-In Amplifier support
    """
    DATA_READY_BIT = 4

    @staticmethod
    def driver_name():
        return 'SR830 DSP Lock-In Amplifier'

    def __init__(self, rm, resource):
        super().__init__(rm, resource)
        self.write('OUTX1')
        self.write('LOCL1')
        self.clear_buf(SR830DSPLockIn.DATA_READY_BIT)
        self.write('OVRM1')
        self.write('*CLS')
        self.idn = self.query_id().translate({ord(c): None for c in ['\r', '\n']}).split(',')

        self.set_options([
            ValueDeviceOption('Oscillator frequency', 'Hz',
                              self.get_osc_frequency, self.set_osc_frequency),
            ValueDeviceOption('Oscillator amplitude', 'V',
                              self.get_osc_amplitude, self.set_osc_amplitude),
            ListDeviceOption('Tc', self.tc_values,
                             self.get_tc, self.set_tc),
            ListDeviceOption('Slope', self.slope_values,
                             self.get_slope, self.set_slope),
            ListDeviceOption('Reserve', self.reserve_values,
                             self.get_reserve, self.set_reserve),
            ListDeviceOption('Sensitivity', self.sensitivity_values,
                             self.get_sensitivity, self.set_sensitivity),
            ValueDeviceOption('Phase', 'deg',
                              self.get_ref_phase, self.set_ref_phase),
            ValueDeviceOption('Harmonic', None,
                              self.get_ref_harmonic, self.set_ref_harmonic),
        ] + self.analog_out + self.analog_in +
        [
            StateDeviceOption('Value', lambda dev=self: str(dev.get_value()))
        ])

    def device_name(self):
        return self.idn[0].replace('_', ' ') + ' ' + self.idn[1] + ' Lock-In Amplifier'

    def device_id(self):
        return self.idn[2]

    def query(self, data):
        with self.lock:
            self.inst.write(data, '\n')
            self.wait_bit(SR830DSPLockIn.DATA_READY_BIT, 100)
            value = self.read()
        return value.translate({ord(c): None for c in ['\r', '\n']})

    def get_value(self):
        value = self.query('SNAP?1,2')
        return value.split(',')

    sensitivity_values = [
        '2 nV', '5 nV', '10 nV', '20 nV', '50 nV', '100 nV',
        '200 nV', '500 nV', '1 uV', '2 uV', '5 uV', '10 uV',
        '20 uV', '50 uV', '100 uV', '200 uV', '500 uV', '1 mV',
        '2 mV', '5 mV', '10 mV', '20 mV', '50 mV', '100 mV',
        '200 mV', '500 mV', '1 V'
        ]

    def get_sensitivity(self):
        value = int(self.query('SENS?'))
        return self.sensitivity_values[value]

    def set_sensitivity(self, value):
        if value in self.sensitivity_values:
            self.write('SENS' + str(self.sensitivity_values.index(value)))
        else:
            raise ValueError('Invalid sensitivity.')

    reserve_values = [
        'High reserve',
        'Normal',
        'Low Noise',
        ]

    def get_reserve(self):
        value = int(self.query('RMOD?'))
        return self.reserve_values[value]

    def set_reserve(self, value):
        if value in self.reserve_values:
            self.write('RMOD' + str(self.reserve_values.index(value)))
        else:
            raise ValueError('Invalid reserve.')

    slope_values = [
        '6 dB/octave',
        '12 dB/octave',
        '18 dB/octave',
        '24 dB/octave',
        ]

    def get_slope(self):
        value = int(self.query('OFSL?'))
        return self.slope_values[value]

    def set_slope(self, value):
        if value in self.slope_values:
            self.write('OFSL' + str(self.slope_values.index(value)))
        else:
            raise ValueError('Invalid slope.')

    tc_values = [
        '10 us', '30 us', '100 us', '300 us',
        '1 ms', '3 ms', '10 ms', '30 ms',
        '100 ms', '300 ms', '1 s', '3 s',
        '10 s', '30 s', '100 s', '300 s',
        '1 ks', '3 ks', '10 ks', '30 ks',
        ]

    def get_tc(self):
        value = int(self.query('OFLT?'))
        return self.tc_values[value]

    def set_tc(self, value):
        if value in self.tc_values:
            self.write('OFLT' + str(self.tc_values.index(value)))
        else:
            raise ValueError('Invalid time constant.')

    def get_osc_amplitude(self):
        value = self.query('SLVL?')
        return value

    def set_osc_amplitude(self, value):
        self.write('SLVL' + str(value))

    def get_osc_frequency(self):
        return self.query('FREQ?')

    def set_osc_frequency(self, value):
        self.write('FREQ' + str(value))

    def get_ref_harmonic(self):
        return self.query('HARM?')

    def set_ref_harmonic(self, value):
        self.write('HARM' + str(value))

    def get_ref_phase(self):
        return self.query('PHAS?')

    def set_ref_phase(self, value):
        self.write('PHAS' + str(value))

    def get_analog_output(self, num):
        return self.query('AUXV? ' + str(num))

    def set_analog_output(self, num, value):
        self.write('AUXV ' + str(num) + ',' + str(value))

    def get_analog_input(self, num):
        return self.query('OAUX? ' + str(num))

    def to_local(self):
        import pyvisa
        self.inst.control_ren(pyvisa.constants.VI_GPIB_REN_ADDRESS_GTL)

    x_y = ValueDeviceOption('X,Y', 'V', get_value, None, 2)

    analog_in = [
        ValueDeviceOption(
            'ANALOG IN ' + str(i), 'V',
            lambda x, mod=i: x.get_analog_input(mod)
            )
        for i in range(1, 5)]

    analog_out = [
        ValueDeviceOption(
            'ANALOG OUT ' + str(i), 'V',
            lambda x, mod=i: x.get_analog_output(mod),
            lambda x, val, mod=i: x.set_analog_output(mod, val)
            )
        for i in range(1, 5)]
