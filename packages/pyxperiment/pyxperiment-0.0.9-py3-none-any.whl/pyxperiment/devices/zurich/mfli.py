"""
    pyxperiment/devices/zurich/mfli.py:
    Support for Zurich Instruments MFLI DSP Lock-In Amplifier

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
from pyxperiment.core.utils import bidict
from pyxperiment.controller.zurich_instrument import ZurichInstrument
from pyxperiment.controller.device_options import (
    ValueDeviceOption, BooleanOption, ListDeviceOption, TimeoutOption
)

class ZurichMFLI(ZurichInstrument):
    """
    Zurich Instruments MFLI Lock-In Amplifier support
    """

    def __init__(self, rm, resource):
        super().__init__(resource, 'MFLI')

        self.set_options([
            self.osc_frequency,
            self.osc_amplitude,
            self.osc_enable,
            self.osc_range,
            self.out_differential,
            self.out_enable,
            self.demod_tc,
            self.demod_order,
            self.input_range,
            self.input_scale,
            self.demod_phase,
            self.demod_harmonic,
            self.demod_value_x_y,
            TimeoutOption(self.demod_value_x_y)
        ] + self.aux_in + self.aux_out_offset)

    @staticmethod
    def driver_name():
        return 'Zurich Instruments MFLI Lock-In Amplifier'

    osc_frequency = ValueDeviceOption(
        'Oscillator frequency', 'Hz',
        get_func=lambda instr: instr.get_double('/%s/OSCS/0/FREQ'),
        set_func=lambda instr, value: instr.set_double('/%s/OSCS/0/FREQ', value),
    )

    osc_amplitude = ValueDeviceOption(
        'Oscillator amplitude', 'V',
        get_func=lambda instr: instr.get_double('/%s/SIGOUTS/0/AMPLITUDES/1'),
        set_func=lambda instr, value: instr.set_double('/%s/SIGOUTS/0/AMPLITUDES/1', value),
    )

    osc_enable = BooleanOption(
        'Oscillator enable',
        get_func=lambda instr: instr.get_int('/%s/SIGOUTS/0/ENABLES/1'),
        set_func=lambda instr, value: instr.set_int('/%s/SIGOUTS/0/ENABLES/1', value),
    )

    osc_range_values = {
        '10 mV':'10e-3',
        '100 mV':'100e-3',
        '1 V':'1',
        '10 V':'10'
    }

    def get_osc_range(self):
        value = self.get_double('/%s/SIGOUTS/0/RANGE')
        dec_val = Decimal(value).quantize(Decimal('1e-6'))
        if self.out_differential.get_value():
            dec_val = dec_val / Decimal('2')
        for range_value in self.osc_range_values.items():
            if Decimal(range_value[1]) == dec_val:
                return range_value[0]
        raise ValueError('Unkwown range ' + value)

    osc_range = ListDeviceOption(
        'Oscillator range', osc_range_values,
        get_func=lambda instr: instr.get_osc_range(),
        set_func=lambda instr, value:
        instr.set_double('/%s/SIGOUTS/0/RANGE', instr.osc_range_values[value]),
    )

    out_differential = BooleanOption(
        'Differential output',
        get_func=lambda instr: instr.get_int('/%s/SIGOUTS/0/DIFF'),
        set_func=lambda instr, value: instr.set_int('/%s/SIGOUTS/0/DIFF', value),
    )

    out_enable = BooleanOption(
        'Output enable',
        get_func=lambda instr: instr.get_int('/%s/SIGOUTS/0/ON'),
        set_func=lambda instr, value: instr.set_int('/%s/SIGOUTS/0/ON', value),
    )

    demod_tc = ValueDeviceOption(
        'Tc', 's',
        get_func=lambda instr: instr.get_double('/%s/DEMODS/0/TIMECONSTANT'),
        set_func=lambda instr, value: instr.set_double('/%s/DEMODS/0/TIMECONSTANT', value),
        sweepable=False
    )

    demod_order_values = bidict({
        '6 dB/oct':'1',
        '12 dB/oct':'2',
        '18 dB/oct':'3',
        '24 dB/oct':'4',
        '30 dB/oct':'5',
        '36 dB/oct':'6',
        '42 dB/oct':'7',
        '48 dB/oct':'8'
    })

    demod_order = ListDeviceOption(
        'Slope order', demod_order_values,
        get_func=lambda instr:
        instr.demod_order_values.inverse[instr.get_int('/%s/DEMODS/0/ORDER')],
        set_func=lambda instr, value:
        instr.set_int('/%s/DEMODS/0/ORDER', instr.demod_order_values[value]),
    )

    input_range_values = {
        '1 mV':'1e-3',
        '3 mV':'3e-3',
        '10 mV':'10e-3',
        '30 mV':'30e-3',
        '100 mV':'100e-3',
        '300 mV':'300e-3',
        '1 V':'1',
        '3 V':'3'
    }

    def get_input_range(self):
        value = self.get_double('/%s/SIGINS/0/RANGE')
        dec_val = Decimal(value).quantize(Decimal('1e-6'))
        for range_value in self.input_range_values.items():
            if Decimal(range_value[1]) == dec_val:
                return range_value[0]
        raise ValueError('Unkwown range ' + value)

    input_range = ListDeviceOption(
        'Input range', input_range_values,
        get_func=lambda instr: instr.get_input_range(),
        set_func=lambda instr, value:
        instr.set_double('/%s/SIGINS/0/RANGE', instr.input_range_values[value]),
    )

    input_scale = ValueDeviceOption(
        'Input scale', None,
        get_func=lambda instr: instr.get_double('/%s/SIGINS/0/SCALING'),
        set_func=lambda instr, value: instr.set_double('/%s/SIGINS/0/SCALING', value),
        sweepable=False
    )

    demod_phase = ValueDeviceOption(
        'Phase', 'deg',
        get_func=lambda instr: instr.get_double('/%s/DEMODS/0/PHASESHIFT'),
        set_func=lambda instr, value: instr.set_double('/%s/DEMODS/0/PHASESHIFT', value),
        sweepable=False
    )

    demod_harmonic = ValueDeviceOption(
        'Harmonic', None,
        get_func=lambda instr: instr.get_int('/%s/DEMODS/0/HARMONIC'),
        set_func=lambda instr, value: instr.set_int('/%s/DEMODS/0/HARMONIC', value),
        sweepable=False
    )

    aux_in = [
        ValueDeviceOption(
            'ANALOG IN ' + str(i+1), 'V',
            get_func=lambda instr, num=i: instr.get_double('/%s/AUXINS/0/VALUES/' + str(num))
            )
        for i in range(0, 2)]

    aux_out_offset = [
        ValueDeviceOption(
            'ANALOG OUT ' + str(i+1), 'V',
            get_func=lambda instr, num=i:
            instr.get_double('/%s/AUXOUTS/' + str(num) + '/OFFSET'),
            set_func=lambda instr, value, num=i:
            instr.set_double('/%s/AUXOUTS/' + str(num) + '/OFFSET', value)
            )
        for i in range(0, 4)]

    aux_out_value = [
        ValueDeviceOption(
            'ANALOG OUT VALUE ' + str(i+1), 'V',
            get_func=lambda instr, num=i:
            instr.get_double('/%s/AUXOUTS/' + str(num) + '/VALUE'),
            )
        for i in range(0, 4)]

    def get_value(self):
        value = self.ds.getSample('/%s/DEMODS/0/SAMPLE' % self.node_name)
        return [str(value['x'][0]), str(value['y'][0])]

    demod_value_x_y = ValueDeviceOption(
        'X,Y', 'V', get_value, None, 2)

    pid_p_value = [
        ValueDeviceOption(
            'PID' + str(i+1) + ' P', 'Hz/deg',
            get_func=lambda instr, num=i:
            instr.get_double('/%s/PIDS/' + str(num) + '/P'),
            set_func=lambda instr, value, num=i:
            instr.set_double('/%s/PIDS/' + str(num) + '/P', value),
            sweepable=False
            )
        for i in range(0, 4)]

    pid_i_value = [
        ValueDeviceOption(
            'PID' + str(i+1) + ' I', 'Hz/deg/s',
            get_func=lambda instr, num=i:
            instr.get_double('/%s/PIDS/' + str(num) + '/I'),
            set_func=lambda instr, value, num=i:
            instr.set_double('/%s/PIDS/' + str(num) + '/I', value),
            sweepable=False
            )
        for i in range(0, 4)]

    pid_d_value = [
        ValueDeviceOption(
            'PID' + str(i+1) + ' D', 'Hz/deg*s',
            get_func=lambda instr, num=i:
            instr.get_double('/%s/PIDS/' + str(num) + '/D'),
            set_func=lambda instr, value, num=i:
            instr.set_double('/%s/PIDS/' + str(num) + '/D', value),
            sweepable=False
            )
        for i in range(0, 4)]

    pid_setpoint = [
        ValueDeviceOption(
            'PID' + str(i+1) + ' Setpoint', 'V',
            get_func=lambda instr, num=i:
            instr.get_double('/%s/PIDS/' + str(num) + '/SETPOINT'),
            set_func=lambda instr, value, num=i:
            instr.set_double('/%s/PIDS/' + str(num) + '/SETPOINT', value),
            sweepable=False
            )
        for i in range(0, 4)]

    pid_keep_value = [
        BooleanOption(
            'PID' + str(i+1) + ' Keep I Value',
            get_func=lambda instr, num=i:
            instr.get_int('/%s/PIDS/' + str(num) + '/keepint'),
            set_func=lambda instr, value, num=i:
            instr.set_int('/%s/PIDS/' + str(num) + '/keepint', value),
            )
        for i in range(0, 4)]

    pid_limit_upper = [
        ValueDeviceOption(
            'PID' + str(i+1) + ' Limit upper', 'V',
            get_func=lambda instr, num=i:
            instr.get_double('/%s/PIDS/' + str(num) + '/LIMITUPPER'),
            set_func=lambda instr, value, num=i:
            instr.set_double('/%s/PIDS/' + str(num) + '/LIMITUPPER', value),
            sweepable=False
            )
        for i in range(0, 4)]

    pid_limit_lower = [
        ValueDeviceOption(
            'PID' + str(i+1) + ' Limit upper', 'V',
            get_func=lambda instr, num=i:
            instr.get_double('/%s/PIDS/' + str(num) + '/LIMITLOWER'),
            set_func=lambda instr, value, num=i:
            instr.set_double('/%s/PIDS/' + str(num) + '/LIMITLOWER', value),
            sweepable=False
            )
        for i in range(0, 4)]

    pid_enable = [
        BooleanOption(
            'PID' + str(i+1) + ' Enable',
            get_func=lambda instr, num=i:
            instr.get_int('/%s/PIDS/' + str(num) + '/ENABLE'),
            set_func=lambda instr, value, num=i:
            instr.set_int('/%s/PIDS/' + str(num) + '/ENABLE', value),
            )
        for i in range(0, 4)]
