"""
    pyxperiment/devices/tektronixAFG3xxx.py:
    Support for Tektronix AFG3000 series waveform generator

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
from pyxperiment.controller.device_options import BooleanOption, ValueDeviceOption

class TektronixAFG3xxx(VisaInstrument):
    """
    Support for Tektronix AFG3000 series waveform generator
    """

    @staticmethod
    def driver_name():
        return 'Tektronix AFG3000 Generator'

    def __init__(self, rm, resource):
        super().__init__(rm, resource)
        self._idn = self.query_id().split(',')
        if self.get_mode() != 'DC':
            self.set_mode('DC')
        self.set_options([
            self.impedance,
            self.output,
            self.offset
        ])

    def device_name(self):
        return self._idn[0] + ' ' + self._idn[1] + ' Generator'

    impedance = ValueDeviceOption(
        'Impedance', 'Ohm',
        get_func=lambda instr: instr.query('OUTP:IMP?'),
        set_func=lambda instr, value: instr.write('OUTP:IMP '+str(value)),
        sweepable=False
    )

    output = BooleanOption(
        'Output',
        get_func=lambda instr: instr.query('OUTP?'),
        set_func=lambda instr, value: instr.write('OUTP ' + value)
    )

    def set_mode(self, mode):
        self.write('FUNC ' + mode)

    def get_mode(self):
        return self.query('FUNC?')

    def get_offset(self):
        return self.query('VOLT:OFFS?')

    def set_offset(self, value):
        self.write('VOLT:OFFS ' + str(value) + 'V')

    offset = ValueDeviceOption(
        'Offset', 'V',
        get_func=get_offset,
        set_func=set_offset
    )
    