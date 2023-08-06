"""
    pyxperiment/controller/device_control.py:
    The control classes implementing data acquisition and storage from
    different devices

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

import traceback
import logging

class DeviceControl():
    """
    Common properties for instrument control
    """

    def __init__(self, device):
        self.device = device
        self._index = 0
        self._values = []
        self.curr_value = None

    @property
    def device_name(self):
        """Название устройства"""
        return self.device.device_name()

    @property
    def location(self):
        """Адрес подключения к устройству"""
        return self.device.location

    @property
    def value(self):
        """Текущее значение"""
        return self.curr_value

    @property
    def index(self):
        """Количество проведенных итераций чтения/записи"""
        return self._index

    @property
    def values(self):
        return self._values

    def reset(self):
        """Empty this data storage"""
        pass

    def init_update(self):
        pass

    def update(self):
        pass

    def to_remote(self):
        """Disable local controls for device"""
        self.device.to_remote()

    def to_local(self):
        """Enable local controls for device"""
        self.device.to_local()

class WritableControl(DeviceControl):
    """Класс управления устройством задачи параметров"""

    def __init__(self, device, values, timeout):
        DeviceControl.__init__(self, device)
        self._values = values
        self.timeout = timeout
        self.curr_value = self.device.get_value()

    def reset(self):
        self._current = 0
        self._index = 0
        self.device.set_value(self._values[self._current])

    def revert(self):
        self._values = self._values[::-1]# do not modify the original list
        self.reset()

    def forward(self):
        """Переход к следующему значению"""
        self._index += 1
        if self._current+1 < len(self._values):
            self._current += 1
            self.device.set_value(self._values[self._current])
            return True
        return False

    def backward(self):
        """Возврат к предыдущему значению"""
        if self._current-1 >= 0:
            self._current -= 1
            self.device.set_value(self._values[self._current])
            return True
        return False

    def update(self):
        self.curr_value = self.device.get_value()

    @property
    def point_set(self):
        """Проверить, установлена ли следующая точка после forward или backward"""
        if callable(getattr(self.device, 'finished', None)):
            # Нужно проверять состояние устройства
            return self.device.finished()
        else:
            # Если устройство не поддерживает "finished", значит значение установлено
            return True

class ObservableControl(DeviceControl):
    """Класс управления устройством чтения параметров используемым для оси X
    (типа температуры или магнитного поля, которое разворачивается не по команде)
    """
    def __init__(self, device, start_value, target_value, timeout):
        DeviceControl.__init__(self, device)
        self.start_value = start_value
        self.target_value = target_value
        self._values = [start_value, target_value]
        self.timeout = timeout
        self.curr_value = self.device.get_value()

    def reset(self):
        self._current = 0
        self._index = 0
        self._values = [self.target_value]
        #self.device.set_value(self.start_value)

    def revert(self):
        self.start_value, self.target_value = self.target_value, self.start_value
        self.reset()

    def forward(self):
        self._index += 1
        if self._current == 0:
            self._current += 1
            self.device.set_value(self.target_value)
            return True
        elif self._current == 2:
            return False
        else:
            if self.device.finished():
                self._current = 2
            return True

    def backward(self):
        if self._current == 2:
            self.curr_value = self.device.get_value()
            self.device.set_value(self.start_value)
            self._current = 0
            return True
        elif self.device.finished():
            return False
        else:
            self.curr_value = self.device.get_value()
            return True

    def update(self):
        self.curr_value = self.device.get_value()
        self._values.insert(len(self._values)-1, self.curr_value)

class ReadableControl(DeviceControl):
    """Класс управления устройством чтения параметров"""

    def __init__(self, device):
        DeviceControl.__init__(self, device)
        self.reset()
        self.curr_value = self.device.get_value()
        self._channels_num = self.device.channels_num

    def reset(self):
        self._values = []

    def update(self):
        try:
            self._values.append(self.device.get_value())
        except:
            logging.exception("Error while reading device:")
            traceback.print_exc()
            self.device.reset()
            self._values.append(self.device.get_value())
        self.curr_value = self._values[-1]

    def num_channels(self):
        return self._channels_num

    def data(self, channel=0):
        if self._channels_num == 1:
            return self._values
        else:
            return [a[channel] for a in self._values]

class AsyncReadableControl(ReadableControl):

    def init_update(self):
        try:
            self.device.init_get_value()
        except:
            logging.exception("Error while reading device:")
            traceback.print_exc()
            self.device.reset()
            self.device.init_get_value()

    def update(self):
        try:
            self._values.append(self.device.end_get_value())
        except:
            logging.exception("Error while reading device:")
            traceback.print_exc()
            self.device.reset()
            self._values.append(self.device.get_value())
        self.curr_value = self._values[-1]

class SweepReadableControl(DeviceControl):
    """
    The control class for a device, carrying it's own internal
    internal x sweep generation. Each acquisition results in a dataset.
    """
    def __init__(self, device):
        DeviceControl.__init__(self, device)
        self._channels_num = self.device.channels_num
        self.reset()
        self.curr_value = []

    def reset(self):
        self._values = []

    def update(self):
        try:
            self.curr_value = self.device.get_sweep()
        except:
            logging.exception("Error while reading device:")
            traceback.print_exc()
            self.device.reset()
            self.curr_value = self.device.get_sweep()
        self._values.append(self.curr_value)

    def num_channels(self):
        return self._channels_num

    def data(self, channel=0, sweep=-1):
        if self._channels_num == 1:
            return self._values[sweep]
        return self._values[sweep][channel]

    def get_sweep_x(self):
        if not callable(getattr(self.device, 'get_sweep_x', None)):
            return range(len(self.data()))
        return self.device.get_sweep_x()

class DoubleWritableControl(DeviceControl):
    """Класс управления устройством задачи параметров"""

    def __init__(self, device1, device2, values1, values2, timeout):
        DeviceControl.__init__(self, device1)
        self._values = values1
        self._device_two = device2
        self._values_two = values2
        self.timeout = timeout
        self.curr_value = self.device.get_value()

    def reset(self):
        self._current = 0
        self._index = 0
        self.device.set_value(self._values[self._current])
        self._device_two.set_value(self._values_two[self._current])

    def revert(self):
        self._values.reverse()
        self._values_two.reverse()
        self.reset()

    def forward(self):
        """Переход к следующему значению"""
        self._index += 1
        if self._current+1 < len(self._values):
            self._current += 1
            self.device.set_value(self._values[self._current])
            self._device_two.set_value(self._values_two[self._current])
            return True
        else:
            return False

    def backward(self):
        """Возврат к предыдущему значению"""
        if self._current-1 >= 0:
            self._current -= 1
            self.device.set_value(self._values[self._current])
            self._device_two.set_value(self._values_two[self._current])
            return True
        else:
            return False

    def update(self):
        self.curr_value = self.device.get_value()

    @property
    def point_set(self):
        """Проверить, установлена ли следующая точка после forward или backward"""
        if callable(getattr(self.device, 'finished', None)):
            # Нужно проверять состояние устройства
            if not self.device.finished():
                return False
        if callable(getattr(self._device_two, 'finished', None)):
            # Нужно проверять состояние устройства
            if not self._device_two.finished():
                return False
        # Если устройство не поддерживает "finished", значит значение установлено
        return True
