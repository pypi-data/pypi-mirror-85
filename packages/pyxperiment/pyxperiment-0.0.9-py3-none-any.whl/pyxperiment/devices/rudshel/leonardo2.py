"""
    pyxperiment/devices/rudshel/leonardo2.py:
    Support for RudShel Leonardo 2 Digitizer board

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

import ctypes

from pyxperiment.controller import VisaInstrument
from pyxperiment.controller.device_options import ValueDeviceOption

class URshBuffer(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ("type", ctypes.c_uint32),#  ип данных буфера
        ("size", ctypes.c_uint32),# данное поле используется после вызова UniDriverGetData(), чтобы отразить реальное количество скопированных данных в буфер
        ("psize", ctypes.c_uint32),# количество элементов в буфере
        ("id", ctypes.c_uint32),# уникальный идентификатор буфера (поле нельзя трогать, оно предназначено только для служебного использования)
        ("ptr", ctypes.c_void_p),# указатель на буфер
    ]

    def __init__(self):
        super().__init__()
        self.type = 0
        self.size = 0
        self.psize = 0
        self.id = 0
        self.ptr = 0

class URshChannel(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ("gain", ctypes.c_uint32),# коэффициент усиления
        ("control", ctypes.c_uint32),# специфические настройки канала
        ("adjustment", ctypes.c_double),# смещениe (в вольтах)
    ]

    def __init__(self, gain=1, control=0, adjustment=0.0):
        super().__init__()
        self.gain = gain
        self.control = control
        self.adjustment = adjustment

RSH_MAX_LIST_SIZE = 32

RSH_API_SUCCESS = 0

RSH_INIT_MODE_CHECK = ctypes.c_uint32(0)
RSH_INIT_MODE_INIT = ctypes.c_uint32(1)
RSH_INIT_MODE_REINIT = ctypes.c_uint32(2)

RSH_DATA_MODE_NO_FLAGS = ctypes.c_uint32(int("0x0", 0))
RSH_DATA_MODE_CONTAIN_DIGITAL_INPUT = ctypes.c_uint32(int("0x00001", 0))
RSH_DATA_MODE_GSPF_TTL = ctypes.c_uint32(int("0x10000", 0))

RSH_CONNECT_MODE_BASE = ctypes.c_uint32(0)
RSH_CONNECT_MODE_SERIAL_NUMBER = ctypes.c_uint32(1)
RSH_CONNECT_MODE_IP_ADDRESS = ctypes.c_uint32(2)
RSH_CONNECT_MODE_PLXCHIP_TYPE = ctypes.c_uint32(16)

RSH_GET_WAIT_BUFFER_READY_EVENT = ctypes.c_uint32(int("0x20001", 0))

class URshInitDMA(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        # код типа данных ( rshInitDMA )
        ("type", ctypes.c_uint32),
        # настройки типа старта платы
        ("startType", ctypes.c_uint32),
        # размер буфера в отсчётах (значение пересчитывается при инициализации в зависимости от сопутствующих настроек)
        ("bufferSize", ctypes.c_uint32),
        # частота дискретизации
        ("frequency", ctypes.c_double),
        # режим работы DMA
        ("dmaMode", ctypes.c_uint32),
        # специфические настройки для данного типа плат (например, диф режим)
        ("control", ctypes.c_uint32),
        # частота дискретизации внутри пачки
        ("frequencyFrame", ctypes.c_double),
        # параметры каналов
        ("channels", URshChannel * RSH_MAX_LIST_SIZE),
        # уровень синхронизации в Вольтах
        ("threshold", ctypes.c_double),
        # специфические настройки синхронизации
        ("controlSynchro", ctypes.c_uint32),
        ]

URshChanControlNotUsed = int("0x0", 0)
URshChanControlUsed = int("0x1", 0)

URshStartTypeProgram = ctypes.c_uint32(1)

rshInitDMA = -1379909629
rshBufferTypeS32 = ctypes.c_uint32(-1379913722)

RSH_LANGUAGE_ENGLISH = ctypes.c_uint32(0)

URshInitDmaDmaModeSingle = ctypes.c_uint32(0)
URshInitDmaDmaModePersistent = ctypes.c_uint32(1)

class RudshelLeonardo2ADC(VisaInstrument):

    @classmethod
    def load_libs(cls):
        if hasattr(cls, 'RUDSHEL_DLL'):
            return
        import os
        cls.RUDSHEL_DLL = ctypes.WinDLL(os.path.join(os.path.dirname(__file__), 'RshUniDriver.dll'))
        cls.get_device_handle = cls.RUDSHEL_DLL.UniDriverGetDeviceHandle
        cls.close_device_handle = cls.RUDSHEL_DLL.UniDriverCloseDeviceHandle
        cls.driver_connect = cls.RUDSHEL_DLL.UniDriverConnect
        cls.driver_is_capable = cls.RUDSHEL_DLL.UniDriverIsCapable
        cls.driver_init = cls.RUDSHEL_DLL.UniDriverInit
        cls.driver_start = cls.RUDSHEL_DLL.UniDriverStart
        cls.driver_stop = cls.RUDSHEL_DLL.UniDriverStop
        cls.driver_get_data = cls.RUDSHEL_DLL.UniDriverGetData
        cls.driver_get_uint = cls.RUDSHEL_DLL.UniDriverLVGetUInt
        cls.driver_allocate_buffer = cls.RUDSHEL_DLL.UniDriverAllocateBuffer
        cls.driver_get_error = cls.RUDSHEL_DLL.UniDriverLVGetError

    @staticmethod
    def driver_name():
        return 'Leonardo 2 Digitizer board'

    def device_name(self):
        return 'Leonardo 2 Digitizer board'

    @property
    def location(self):
        """Get device visa address"""
        return 'PCI (Leonardo2)'

    @property
    def channels_num(self):
        return len(self.active_channels)

    def get_error(self, code):
        error_desc = ctypes.create_string_buffer(1024)
        self.driver_get_error(ctypes.c_uint32(code), error_desc, ctypes.c_uint32(1024), RSH_LANGUAGE_ENGLISH)
        return repr(error_desc.value)

    def __init__(self, rm, resource):
        self.load_libs()
        self.deviceHandle = ctypes.c_uint32()
        self.active_channels = [1, 2, 3]
        self.buffer_size = 10240
        ret = self.get_device_handle(b'LEONARDO2PCI', ctypes.byref(self.deviceHandle))
        if ret != RSH_API_SUCCESS:
            raise Exception('UniDriverGetDeviceHandle returned' + self.get_error(ret))

        # Подключаемся к устройству.
        ret = self.driver_connect(self.deviceHandle, ctypes.c_uint32(1), RSH_CONNECT_MODE_BASE)
        if ret != RSH_API_SUCCESS:
            raise Exception('Error connecting to device ' + self.get_error(ret))

        self.init_sweeping()
        self._allocate_buffer()
        self.options = [
            ValueDeviceOption(
                'Buffer size', 'samples', self.get_buffer_size, self.set_buffer_size)
            ]

    def init_sweeping(self):
        p = URshInitDMA()
        p.type = rshInitDMA
        p.startType = URshStartTypeProgram
        p.dmaMode = URshInitDmaDmaModePersistent
        p.control = 1
        p.bufferSize = self.buffer_size
        p.frequency = 102400.0

        # настройка измерительных каналов
        for i in self.active_channels:
            p.channels[i].control = URshChanControlUsed
            p.channels[i].gain = 1

        # Инициализация параметров работы устройства и драйвера.
        st = self.driver_init(self.deviceHandle, RSH_INIT_MODE_INIT, ctypes.byref(p))
        # Параметры могут быть скорректированны, это отразится в структуре "p".
        if st != RSH_API_SUCCESS:
            self.close_device_handle(self.deviceHandle)
            raise Exception("UniDriverInit " + self.get_error(st))

    def _allocate_buffer(self):
        # подготовка буфера для данных
        # ставим желаемый тип буфера
        self.dataBufferLSB = URshBuffer()
        self.dataBufferLSB.type = rshBufferTypeS32

        # выделение памяти происходит внутри RshUniDriver
        st = self.driver_allocate_buffer(ctypes.byref(self.dataBufferLSB), self.channels_num*self.buffer_size)
        if st != RSH_API_SUCCESS:
            raise Exception("UniDriverAllocateBuffer " + self.get_error(st))

    def start_sweeping(self):
        st = self.driver_start(self.deviceHandle)
        if st != RSH_API_SUCCESS:
            raise Exception("UniDriverStart " + self.get_error(st))

    def stop_sweeping(self):
        st = self.driver_stop(self.deviceHandle)
        if st != RSH_API_SUCCESS:
            raise Exception("UniDriverStop " + self.get_error(st))

    def to_remote(self):
        self.start_sweeping()
        self.waitTime = ctypes.c_uint32(1000)

    def to_local(self):
        self.stop_sweeping()

    def get_sweep(self):
        # Ожидаем готовность буфера. В данном случае функция Get используется для передачи значения (время ожидания), а не для получения данных
        ret = self.driver_get_uint(self.deviceHandle, RSH_GET_WAIT_BUFFER_READY_EVENT, ctypes.byref(self.waitTime))
        if ret != RSH_API_SUCCESS:
            raise Exception('UniDriverLVGetUInt ' + self.get_error(ret))

        # Получаем буфер с данными (используется функция UniDriverGetData, для всех типов данных)
        ret = self.driver_get_data(self.deviceHandle, RSH_DATA_MODE_NO_FLAGS, ctypes.byref(self.dataBufferLSB))
        if ret != RSH_API_SUCCESS:
            raise Exception('UniDriverGetData ' + self.get_error(ret))
        #UniDriverLVGetDataDouble (deviceHandle,RSH_DATA_MODE_NO_FLAGS,CHANNEL_NUMBER*IBSIZE,&received,dataBufferVolts);

        buffer = ctypes.cast(self.dataBufferLSB.ptr, ctypes.POINTER(ctypes.c_int32))
        ret_buffer = []
        for i in range(self.channels_num):
            ret_buffer.append([int(buffer[j]) * 10.0 / 2147483648 for j in range(i, self.dataBufferLSB.size, self.channels_num)])
        return ret_buffer

    def get_buffer_size(self):
        return self.buffer_size

    def set_buffer_size(self, value):
        self.buffer_size = int(value)
        self.init_sweeping()
        self._allocate_buffer()

    def __del__(self):
        self.close_device_handle(self.deviceHandle)
