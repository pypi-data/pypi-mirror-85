"""
    pyxperiment/data_format/text_data_format.py:
    Implements the data stroraging into plain text files

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

import os
import re
import datetime
import numpy as np
from pyxperiment.controller.device_control import SweepReadableControl

class TextDataWriter(object):
    """A class for formatted data output into text files"""

    def __init__(self, name_exp):
        self.name_exp = name_exp
        self.dirname = os.path.dirname(name_exp)
        self.base_name = os.path.basename(name_exp)
        self.regexp = self.base_name.replace('*', '([0-9]+)').replace('.', r'\.')

        if not os.path.exists(self.dirname):
            os.makedirs(self.dirname)
        self.__get_file_number__()

    def __get_file_number__(self):
        max_file_num = 0
        for file in os.listdir(self.dirname):
            match = re.match(self.regexp, file)
            if match != None:
                max_file_num = max(max_file_num, int(match.group(1)))
        self.file_num = max_file_num + 1

    def start_new_file(self):
        """Recheck next avialiable file number"""
        self.__get_file_number__()

    def get_filename(self):
        """Get current filename"""
        return os.path.join(self.dirname, self.base_name.replace('*', str(self.file_num)))

    def save_file(self, timecol, xcol, data):
        file_name = self.get_filename()
        with open(file_name, "w") as text_file:
            for i in range(len(xcol)):
                if i >= len(timecol):
                    print('NaN', end=' ', file=text_file)
                elif isinstance(timecol[i], datetime.datetime):
                    print(datetime.datetime.isoformat(timecol[i]), end=' ', file=text_file)
                else:
                    print(str(int(timecol[i]*1000)), end=' ', file=text_file)
                print(str(xcol[i]), end=' ', file=text_file)
                if i < len(timecol):
                    print(*[str(data_line[i]) for data_line in data], file=text_file)
                else:
                    print(*['NaN' for data_line in data], file=text_file)

    def print_device_info(self, info, file):
        """Saves sweep info for single device"""
        device_name = next(filter(lambda x: x[0] == 'Name', info))
        print('Device: ' + device_name[1], end='\n', file=file)
        for field in filter(lambda x: x[0] != 'Name', info):
            print('\t' + field[0] + ': ' + field[1], end='\n', file=file)

    def save_info_file(self, yinfo, xinfo, sweep_info):
        """Saves sweep info into separate file"""
        file_name = self.get_filename().replace('.dat', '.info')
        with open(file_name, "w") as text_file:
            print('Y devices: ', end='\n', file=text_file)
            for device_info in yinfo:
                self.print_device_info(device_info, text_file)
            print('X devices: ', end='\n', file=text_file)
            for device_info in xinfo:
                self.print_device_info(device_info, text_file)
            for field in sweep_info:
                print(field[0] + ': ' + str(field[1]), end='\n', file=text_file)

    def save_sweep(self, index, channel, num, x_values, y_values):
        """Saves a sweep device data in a separate file"""
        file_name = self.get_filename().replace(
            '.dat', '_' + str(index) + '_' + str(channel) + '_' + str(num) + '.dat'
            )
        #data = np.array([x_values, y_values], dtype='S')
        with open(file_name, "w") as text_file:
        #    np.savetxt(text_file, data.T, fmt=['%s', '%s'])
            for i in range(len(x_values)):
                print(*[x_values[i], y_values[i]], file=text_file)

    def after_sweep(self, num, data_context):
        if num == 0:
            self.save_internal(data_context)
            self.start_new_file()

    def save_internal(self, data_context):
        """Сохранение данных в файл"""
        rd_data = []
        for rd in data_context.readables:
            for ch in range(rd.num_channels()):
                rd_data.append(rd.data(ch))
        self.save_file(data_context._time, data_context.writables[0].values, rd_data)
        # Save all sweeps (if present)
        sweep_readables = list(
            filter(lambda x: isinstance(x, SweepReadableControl), data_context._readables))
        # TODO: use data storage
        for readable in sweep_readables:
            index = data_context.readables.index(readable)
            x_values = readable.get_sweep_x()
            for num in range(len(readable._values)):
                for channel in range(readable.num_channels()):
                    self.save_sweep(index, channel, num+1, x_values, readable.data(channel, num))
