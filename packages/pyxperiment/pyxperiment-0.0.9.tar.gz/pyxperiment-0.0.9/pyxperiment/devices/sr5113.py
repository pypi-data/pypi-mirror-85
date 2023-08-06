"""
    pyxperiment/devices/sr5113.py: Support for SR5113 Preamplifier

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
    ListOption, ValueDeviceOption, StateDeviceOption
)

class SR5113Preamplifier(VisaInstrument):
    """
    SR5113 Preamplifier support
    """

    @staticmethod
    def driver_name():
        return 'SR5113 Preamplifier'

    def __init__(self, rm, resource):
        super().__init__(rm, resource)

    def query_id(self):
        return self.query('ID')

    def device_name(self):
        return 'SR' + self.query_id() + ' Low-noise Preamplifier'

    def write(self, data):
        self.query(data)

    def recover(self):
        self.query('OR')

    source = ListOption(
        'Source', ['A', 'A-B'], 'IN', 'IN '
        )

    time_constant = ListOption(
        'Time constant', ['1 second', '10 seconds'], 'TC', 'TC '
        )

    coupling = ListOption(
        'Input coupling', ['AC', 'DC'], 'CP', 'CP '
        )

    dynamic_reserve = ListOption(
        'Dynamic reserve', ['Low noise', 'High reserve'], 'DR', 'DR '
        )

    filter_values = [
        'Flat',
        'Bandpass',
        '6 dB/oct LP',
        '12 dB/oct LP',
        '6/12 dB/oct LP',
        '6 dB/oct HP',
        '12 dB/oct HP',
        '6/12 dB/oct HP'
        ]

    filter_mode = ListOption(
        'Filter mode', filter_values, 'FLT', 'FLT '
        )

    coarse_gain_values = [
        '5', '10', '25', '50',
        '100', '250', '500', '1000',
        '2500', '5000', '10000', '25000',
        '50000'
        ]

    coarse_gain = ListOption(
        'Filter mode', coarse_gain_values, 'CG', 'CG '
        )

    fine_gain_values = [
        '5', '10', '25', '50',
        '100', '250', '500', '1000',
        '2500', '5000', '10000', '25000',
        '50000'
        ]

    fine_gain = ListOption(
        'Fine gain', fine_gain_values, 'FG', 'FG '
        )

    vernier = ListOption(
        'Vernier', [str(x) for x in range(16)], 'GV', 'GV '
        )

    frequency_values = [
        '0.03 Hz', '0.1 Hz',
        '0.3 Hz', '1 Hz',
        '3 Hz', '10 Hz',
        '30 Hz', '100 Hz',
        '300 Hz', '1 kHz',
        '3 kHz', '10 kHz',
        '30 kHz', '100 kHz',
        '300 kHz'
        ]

    frequency = ListOption(
        'Vernier', frequency_values, 'GV', 'GV '
        )
