"""
    pyxperiment/data_format/columned_data_format.py:
    Implements the data storaging for columned scans

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

from .text_data_format import TextDataWriter

class ColumnedDataWriter(TextDataWriter):
    """
    Implements the data storaging for columned scans
    """

    def after_sweep(self, num, data_context):
        if num == 1:
            self.save_internal(data_context)
            self.start_new_file()

    def save_internal(self, data_context):
        """Сохранение данных в файл"""
        wr_data = []
        for wr_w in data_context.writables[1].values:
            for i in range(data_context.curves_num):
                wr_data.append(wr_w)

        index = data_context.writables[1].index * data_context.curves_num + (data_context._curve - 1)

        rd_data = []
        curves = data_context.all_data.get_data()
        for i in range(len(curves[0].read_data()[0])):
            rd_data.append(list((curve.read_data()[0][i] if i < len(curve.read_data()[0]) else 'NaN') for curve in curves))
        time_data = [curve.time_markers()[0] for curve in curves]
        self.save_file(time_data, wr_data, rd_data)
