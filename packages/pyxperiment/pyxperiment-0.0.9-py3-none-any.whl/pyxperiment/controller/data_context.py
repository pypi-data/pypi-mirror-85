"""
    pyxperiment/controller/data_context.py:
    Performs data collection and instrument manipulation

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

import threading
import time
import datetime
import concurrent.futures
import queue

from .data_storage import DataStorage
from .device_control import (
    WritableControl, ReadableControl, ObservableControl,
    SweepReadableControl, DoubleWritableControl, AsyncReadableControl
)

class DataContext(object):
    """
    Performs data collection and instrument manipulation
    """

    def __init__(self):
        self.__writables = list()
        self._readables = list()
        self.elapsed = 0
        self._max_delay = 0
        self._update_semaphore = threading.BoundedSemaphore(1)
        self.__is_paused = False
        self.__msg_flag = False
        self.__msg_queue = queue.Queue()
        self.status = ''
        self.finished = False
        self.__backsweep = False
        self.all_data = DataStorage()
        self.curve_callback = None

    def rearm(self):
        self.status = ''
        self.finished = False

    # Конфигурация
    def add_observable(self, writable, values, timeout):
        """Добавить устройство, используемое для чтения параметров, по оси Х
        """
        self.__writables.append(ObservableControl(writable, values[0], values[1], timeout))

    def add_writable(self, writable, values, timeout):
        """Добавить устройство, используемое для задания параметра
        """
        self.__writables.append(WritableControl(writable, values, timeout))

    def add_double_writable(self, writable1, writable2, values1, values2, timeout):
        """Добавить устройство, используемое для задания параметра
        """
        self.__writables.append(DoubleWritableControl(writable1, writable2, values1, values2, timeout))

    def add_readables(self, readables):
        """Добавить устройство, используемое для чтения величины
        """
        for device in readables:
            if getattr(device, 'get_sweep', None):
                self._readables.append(SweepReadableControl(device))
            elif not getattr(device, 'init_get_value', None) or len(readables) == 1:
                self._readables.append(ReadableControl(device))
            else:
                self._readables.append(AsyncReadableControl(device))

    def add_curve_callback(self, callback):
        self.curve_callback = callback

    def set_data_writer(self, dataWriter):
        self.dataWriter = dataWriter

    def set_curves_num(self, num, delay, backsweep):
        self._curves_num = num
        self._curve = 1
        self.curves_delay = delay
        self.__backsweep = backsweep

    @property
    def curves_num(self):
        """Общее число повторов каждой записи"""
        return self._curves_num

    @property
    def currentCurve(self):
        """Текущий номер повтора записи"""
        return self._curve

    @property
    def backsweep(self):
        """Сканировать на обратном ходе"""
        return self.__backsweep

    @property
    def maxDelay(self):
        """Максимальная задержка считывания точки на этой кривой"""
        return self._max_delay

    @property
    def writables(self):
        """Получить список управляемых устройств"""
        return self.__writables

    @property
    def readables(self):
        """Получить список считываемых устройств"""
        return self._readables

    def _delay(self, secs):
        """Временная задержка, проверка управляющих команд пауза/стоп"""
        if secs > 0:
            time.sleep(secs)
        if self.__stop_flag:
            raise InterruptedError("Stopped by user")

    def _process_writable(self, wr):
        executor = concurrent.futures.ThreadPoolExecutor(max_workers=8)
        init_readables = list(
            filter(lambda x: isinstance(x, AsyncReadableControl), self._readables))

        self._curve = 1
        while self._curve <= self.curves_num:
            self.status = 'Starting iterations'
            wr.reset()
            self._time = []
            # Сброс и первое чтение
            for rd in self._readables:
                rd.reset()
            # Add the new curve to the storage
            self.all_data.add_curve(self._time, wr, self._readables)

            self.status = 'Sweeping'# Sweeping forward
            start_time = datetime.datetime.now()
            reference_time = time.perf_counter()
            desired_time = wr.timeout / 1000.0

            while True:
                elapsed_time = time.perf_counter() - reference_time
                self.elapsed = desired_time - elapsed_time
                self._max_delay = min(self._max_delay, self.elapsed)
                to_sleep = self.elapsed
                if to_sleep > 0:
                    while to_sleep > 0.02:
                        time.sleep(0.001)
                        elapsed_time = time.perf_counter() - reference_time
                        to_sleep = desired_time - elapsed_time
                # Инициализация - для GPIB важно отослать все команды до того как начал считывание, так как считывание блокирует интерфейс
                future = executor.submit(wr.update)
                if init_readables:
                    concurrent.futures.wait([executor.submit(rd.init_update) for rd in init_readables])
                # Собственно считывание
                futures = [executor.submit(rd.update) for rd in self._readables]
                futures.append(future)
                concurrent.futures.wait(futures)
                self._time.append(time.perf_counter() - reference_time)
                if not wr.forward():
                    break
                if self.__stop_flag:
                    self.dataWriter.save_internal(self)
                    raise InterruptedError("Stopped by user")
                if self.__is_paused:
                    self._update_semaphore.acquire()
                if self.__msg_flag:
                    if not self.__msg_queue.empty():
                        msg = self.__msg_queue.get_nowait()
                        self.dataWriter.save_internal(self)
                    self.__msg_flag = False
                desired_time += wr.timeout / 1000.0
            self._time[0] = start_time
            self._time[-1] = datetime.datetime.now()
            # Inform data writer that the fast curve has finished
            self.dataWriter.after_sweep(0, self)
            # Call the callback (if set)
            if self.curve_callback:
                self.curve_callback()
            # Разворачиваем назад
            self._curve += 1
            if self._curve <= self.curves_num:
                self._sweep_to_start(0)
                self.status = 'Delay before next iteration'
                self._delay(self.curves_delay)
        self._curve = self.curves_num

    def _sweep_to_start(self, num):
        wr = self.writables[num]
        # неоднородно
        if wr.device_name == 'Time':
            wr.reset()
        elif num == 0 and self.__backsweep:
            for rd in self._readables:
                rd.reset()
            wr.revert()
        elif wr.values[0] == wr.values[-1]:
            for rd in self._readables:
                rd.reset()
            wr.reset()
        else:
            self.status = 'Sweepeing ' + ('slow' if num > 0 else '') + 'device back to start...'
            while True:
                wr.update()
                if not wr.backward():
                    break
                self._delay(wr.timeout / 1000.0 / 10)

    def _process_slow_writable(self, num):
        wr = self.writables[num]
        if num == 0:
            self._process_writable(wr)
            return

        self.status = 'Starting iterations slow'
        self.all_data = DataStorage()
        # Разворачиваем вперед
        wr.reset()
        while True:
            # If slow writable needs extra time to set point, we wait for it
            wr.update()
            while not wr.point_set:
                self.status = 'Waiting for slow X device to set point...'
                self._delay(0.1)
                wr.update()
            # Ожидание перед началом итерации
            self.status = 'Delay slow device before iteration...'
            current_time = time.perf_counter()
            target_time = current_time + wr.timeout / 1000.0
            while (target_time - current_time) > 0.5:
                self._delay(0.5)
                wr.update()
                current_time = time.perf_counter()
            if target_time > current_time:
                self._delay(target_time - current_time)
                wr.update()
            # Сканируем быстрым устройством
            self._process_slow_writable(num-1)
            # Передвигаем медленное устройство на следующую точку
            if not wr.forward():
                break
            # Разворачиваем назад более быстрое устройство
            self._sweep_to_start(num-1)
        self.dataWriter.after_sweep(num, self)

    def __update_task(self):
        for device in self._readables + self.__writables:
            device.to_remote()
        try:
            self.all_data = DataStorage()
            self._process_slow_writable(len(self.writables)-1)
            self.status = 'Complete'
        except InterruptedError:
            self.status = InterruptedError.strerror
        for device in self._readables + self.__writables:
            device.to_local()
        self.finished = True

    def save(self):
        """Сохранение данных по внешней команде"""
        self.__msg_queue.put(1)
        self.__msg_flag = True

    def start(self):
        self.__stop_flag = False
        self.thread = threading.Thread(target=self.__update_task)
        self.thread.start()

    def pause(self, state):
        if self.__is_paused != state:
            self.__is_paused = state
            if state:
                self._update_semaphore.acquire()
            elif not state:
                self._update_semaphore.release()

    @property
    def isPaused(self):
        return self.__is_paused

    def stop(self):
        self.__stop_flag = True
        self.pause(False)
        self.thread.join()
        if isinstance(self.writables[0], ObservableControl):
            self.writables[0].device.stop()

    def __to_start_task(self):
        try:
            self._sweep_to_start(0)
            self.status = 'Complete'
        except InterruptedError:
            self.status = InterruptedError.strerror
        for rd in self._readables:
            rd.to_local()
        for wr in self.__writables:
            wr.to_local()

    def sweepToStart(self):
        self.__stop_flag = False
        self.thread = threading.Thread(target=self.__to_start_task)
        self.thread.start()

    def data(self, num, channel=0):
        return list(map(float, self.readables[num].data(channel)))

    def xval(self):
        return list(map(float, self.writables[0].values))

    @property
    def filename(self):
        return self.dataWriter.get_filename()

    def get_all_data(self):
        return self.all_data
