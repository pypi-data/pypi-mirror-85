"""
    pyxperiment/devices/ztec/zt410.py:
    Support for ZTEC ZT-410 PCI Oscilloscope/Digitizer

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
from decimal import Decimal

from pyxperiment.controller import Instrument
from pyxperiment.controller.validation import SimpleRangeValidator
from pyxperiment.controller.device_options import ValueDeviceOption, BooleanOption, ListDeviceOption

class ZtecZT410ADC(Instrument):
    """
    ZTEC ZT-410 PCI Oscilloscope/Digitizer
    """

    @classmethod
    def load_libs(cls):
        import os
        if hasattr(cls, 'ZCARD_DLL'):
            return
        # Will only work under x86 Win7
        # Load all DLLs explicitely from their locations
        cls.ZCARD_DLL = ctypes.CDLL(os.path.join(os.path.dirname(__file__), 'zcard.dll'))
        cls.ZBIND_DLL = ctypes.CDLL(os.path.join(os.path.dirname(__file__), 'zbind.dll'))
        cls.ZTSCOPESIM_DLL = ctypes.CDLL(os.path.join(os.path.dirname(__file__), 'ztscopesim.dll'))
        cls.ZTSCOPEC_DLL = ctypes.CDLL(os.path.join(os.path.dirname(__file__), 'ztscopeC.dll'))
        # Card detect function
        cls.zcard = cls.ZCARD_DLL.zcard
        # Basic I/O functions
        cls.zbind_send = cls.ZBIND_DLL.zbind_send
        cls.zbind_receive = cls.ZBIND_DLL.zbind_receive
        # Specific functions
        cls.ztscopeC_init = cls.ZTSCOPEC_DLL.ztscopeC_init
        cls.ztscopeC_error_description = cls.ZTSCOPEC_DLL.ztscopeC_error_description
        cls.ztscopeC_channel_enable = cls.ZTSCOPEC_DLL.ztscopeC_channel_enable
        cls.ztscopeC_vertical = cls.ZTSCOPEC_DLL.ztscopeC_vertical
        cls.ztscopeC_trigger = cls.ZTSCOPEC_DLL.ztscopeC_trigger
        cls.ztscopeC_acquisition = cls.ZTSCOPEC_DLL.ztscopeC_acquisition
        cls.ztscopeC_capture_waveform = cls.ZTSCOPEC_DLL.ztscopeC_capture_waveform
        cls.ztscopeC_read_waveform_preamble = cls.ZTSCOPEC_DLL.ztscopeC_read_waveform_preamble
        cls.ztscopeC_read_waveform = cls.ZTSCOPEC_DLL.ztscopeC_read_waveform
        cls.ztscopeC_versions = cls.ZTSCOPEC_DLL.ztscopeC_versions
        cls.ztscopeC_close = cls.ZTSCOPEC_DLL.ztscopeC_close

    ZT_TRUE = ctypes.c_uint8(1)
    ZT_FALSE = ctypes.c_uint8(0)

    ZT410_INST = ctypes.c_uint32(int("0x11000001", 0))
    ZTSCOPEC_IMP_50 = ctypes.c_float(50.0)
    ZTSCOPEC_IMP_1M = ctypes.c_float(1e6)

    @staticmethod
    def driver_name():
        return 'ZTEC ZT410 Oscilloscope/Digitizer'

    def device_name(self):
        return self._id[0] + ' ' + self._id[1] + ' Digitizer'

    @property
    def location(self):
        """Get device visa address"""
        return self.resource.value.decode('ascii')

    @property
    def channels_num(self):
        return 1

    def __get_error(self, code):
        error_desc = ctypes.create_string_buffer(1024)
        self.ztscopeC_error_description(ctypes.c_uint16(code), error_desc)
        return repr(error_desc.value)

    def __init__(self, rm, resource):
        super().__init__('')
        self.load_libs()
        self.resource = ctypes.create_string_buffer(256)
        comm_bus = ctypes.c_uint16()
        ret = self.zcard(
            self.resource,
            ctypes.byref(comm_bus),
            ctypes.c_uint32(256),
            ctypes.c_uint32(0)
            )
        if ret != 0:
            raise Exception("zcard error: " + self.__get_error(ret))

        self.model_number = ctypes.c_uint32()
        self.handle = ctypes.c_int32()
        ret = self.ztscopeC_init(
            self.resource,
            ctypes.c_uint16(0),
            ctypes.c_uint16(0),
            comm_bus,
            ctypes.byref(self.model_number),
            ctypes.byref(self.handle)
            )
        if ret != 0:
            raise Exception("init error: " + self.__get_error(ret))

        self._id = ctypes.create_string_buffer(256)
        revision = ctypes.create_string_buffer(256)
        configuration = (ctypes.c_uint16 * 4)()
        ret = self.ztscopeC_versions(
            self.handle,
            self._id,
            revision,
            configuration
            )
        self._id = self._id.value.decode('ascii').split(',')

        self.x_value = []
        self.__init_sweeping()
        self.set_options([
            self.sample_rate,
            self.points,
            self.horizontal_ref,
            self.horizontal_time,
            self.channel_1_enable,
            self.channel_2_enable,
        ] + self.ch_range + self.ch_offset + self.ch_atten + self.ch_imp + self.ch_coup)


    def __init_sweeping(self):
        ret = self.ztscopeC_trigger(
            self.handle,
            ctypes.c_uint16(0),
            ctypes.c_float(0),
            ctypes.c_uint16(0)
            )
        if ret != 0:
            raise Exception("trigger error: " + self.__get_error(ret))

        ret = self.ztscopeC_acquisition(
            self.handle,
            ctypes.c_uint16(0),
            ctypes.c_uint16(2),
            ctypes.c_uint16(0),
            ctypes.c_uint16(0),
            ctypes.c_uint16(1)
            )
        if ret != 0:
            raise Exception("acquisition error: " + self.__get_error(ret))

    def get_sweep(self):
        ret = self.ztscopeC_capture_waveform(
            self.handle,
            ctypes.c_uint16(65535)
            )
        if ret != 0:
            raise Exception("capture_waveform error: " + self.__get_error(ret))
        wf_type = ctypes.c_uint16()
        wf_points = ctypes.c_uint32()
        wf_aq_count = ctypes.c_uint16()
        wf_time_int = ctypes.c_float()
        wf_time_off = ctypes.c_float()
        wf_volt_int = ctypes.c_float()
        wf_volt_off = ctypes.c_float()
        ret = self.ztscopeC_read_waveform_preamble(
            self.handle,
            ctypes.c_uint16(0),
            ctypes.byref(wf_type),
            ctypes.byref(wf_points),
            ctypes.byref(wf_aq_count),
            ctypes.byref(wf_time_int),
            ctypes.byref(wf_time_off),
            ctypes.byref(wf_volt_int),
            ctypes.byref(wf_volt_off),
            )
        if ret != 0:
            raise Exception("read_waveform_preamble error: " + self.__get_error(ret))
        buffer = (ctypes.c_float * wf_points.value)()
        time_buf = (ctypes.c_float * wf_points.value)()
        ret = self.ztscopeC_read_waveform(
            self.handle,
            ctypes.c_uint16(0),
            buffer,
            time_buf,
            ctypes.c_uint16(1)
            )
        if ret != 0:
            raise Exception("read_waveform error: " + self.__get_error(ret))
        self.x_value = [time_buf[i] for i in range(wf_points.value)]
        return [buffer[i] for i in range(wf_points.value)]

    def _rspcmp_to_type(self, rsp_cmd):
        if rsp_cmd == '%f':
            return ctypes.c_float()
        elif rsp_cmd == '%u':
            return ctypes.c_uint32()
        elif rsp_cmd == '%hu':
            return ctypes.c_uint16()
        return None

    def query(self, cmd):
        ind = cmd.rfind('%')
        qry_cmd = (cmd[:2]+'8'+cmd[3:ind]).encode()
        rsp_cmd = cmd[ind:]
        result = self._rspcmp_to_type(rsp_cmd)
        ret = self.zbind_send(self.handle, self.ZT_TRUE, qry_cmd)
        if ret != 0:
            raise Exception("zbind_send error: " + self.__get_error(ret))
        ret = self.zbind_receive(self.handle, self.ZT_TRUE, rsp_cmd.encode(), ctypes.byref(result))
        if ret != 0:
            raise Exception("zbind_receive error: " + self.__get_error(ret))
        return str(result.value)

    def query_ch(self, cmd, ch):
        ind = cmd.rfind('%')
        qry_cmd = (cmd[:2]+'8'+cmd[3:ind]).encode()
        rsp_cmd = cmd[ind:]
        result = self._rspcmp_to_type(rsp_cmd)
        ch = ctypes.c_uint16(int(ch))
        ret = self.zbind_send(self.handle, self.ZT_TRUE, qry_cmd, ch)
        if ret != 0:
            raise Exception("zbind_send error: " + self.__get_error(ret))
        ret = self.zbind_receive(self.handle, self.ZT_TRUE, rsp_cmd.encode(), ctypes.byref(result))
        if ret != 0:
            raise Exception("zbind_receive error: " + self.__get_error(ret))
        return str(result.value)

    def write(self, cmd, value):
        ind = cmd.rfind('%')
        if cmd[ind:] == '%f':
            value = ctypes.c_double(float(value))
        elif cmd[ind:] == '%u':
            value = ctypes.c_uint32(int(Decimal(value)))
        elif cmd[ind:] == '%hu':
            value = ctypes.c_uint16(int(value))
        ret = self.zbind_send(self.handle, self.ZT_FALSE, cmd.encode(), value)
        if ret != 0:
            raise Exception("zbind_send error: " + self.__get_error(ret))

    def write_ch(self, cmd, ch, value):
        ind = cmd.rfind('%')
        if cmd[ind:] == '%f':
            value = ctypes.c_double(float(value))
        elif cmd[ind:] == '%u':
            value = ctypes.c_uint32(int(Decimal(value)))
        elif cmd[ind:] == '%hu':
            value = ctypes.c_uint16(int(value))
        ch = ctypes.c_uint16(int(ch))
        ret = self.zbind_send(self.handle, self.ZT_FALSE, cmd.encode(), ch, value)
        if ret != 0:
            raise Exception("zbind_send error: " + self.__get_error(ret))

    ZT410_CMD_CHAN_STAT = '0x0410%hu%hu'

    ZT410_CMD_HORZ_RATE = '0x0405%f'
    ZT410_CMD_HORZ_POINTS = '0x0511%u'
    ZT410_CMD_HORZ_REF = '0x0514%f'
    ZT410_CMD_HORZ_TIME = '0x0515%f'

    ZT410_CMD_VERT_RANGE = '0x0407%hu%f'
    ZT410_CMD_VERT_OFFSET = '0x040C%hu%f'
    ZT410_CMD_VERT_ATTEN = '0x0411%hu%f'
    ZT410_CMD_VERT_COUP = '0x0412%hu%hu'
    ZT410_CMD_VERT_IMP = '0x0413%hu%f'

    ZT410_INPUT_CH1 = 0
    ZT410_INPUT_CH2 = 1

    def get_sweep_x(self):
        return self.x_value

    def __del__(self):
        ZtecZT410ADC.ztscopeC_close(self.handle)
        del self.handle

    sample_rate = ValueDeviceOption(
        'Sample rate', 'Hz',
        get_func=lambda instr: instr.query(instr.ZT410_CMD_HORZ_RATE),
        set_func=lambda instr, value: instr.write(instr.ZT410_CMD_HORZ_RATE, value),
        validator=SimpleRangeValidator(1e4, 400e6),
        sweepable=False
    )

    points = ValueDeviceOption(
        'Points', None,
        get_func=lambda instr: instr.query(instr.ZT410_CMD_HORZ_POINTS),
        set_func=lambda instr, value: instr.write(instr.ZT410_CMD_HORZ_POINTS, value),
        validator=SimpleRangeValidator(100, 16000000, 1),
        sweepable=False
    )

    horizontal_ref = ValueDeviceOption(
        'Sweep Offset reference', '',
        get_func=lambda instr: instr.query(instr.ZT410_CMD_HORZ_REF),
        set_func=lambda instr, value: instr.write(instr.ZT410_CMD_HORZ_REF, value),
        validator=SimpleRangeValidator(0, 1),
        sweepable=False
    )

    horizontal_time = ValueDeviceOption(
        'Sweep Offset time', 's',
        get_func=lambda instr: instr.query(instr.ZT410_CMD_HORZ_TIME),
        set_func=lambda instr, value: instr.write(instr.ZT410_CMD_HORZ_TIME, value),
        validator=SimpleRangeValidator(0, 655),
        sweepable=False
    )

    channel_1_enable = BooleanOption(
        'Enable channel 1',
        get_func=lambda instr: instr.query_ch(instr.ZT410_CMD_CHAN_STAT, instr.ZT410_INPUT_CH1),
        set_func=lambda instr, value: instr.write_ch(instr.ZT410_CMD_CHAN_STAT, instr.ZT410_INPUT_CH1, value)
    )

    channel_2_enable = BooleanOption(
        'Enable channel 2',
        get_func=lambda instr: instr.query_ch(instr.ZT410_CMD_CHAN_STAT, instr.ZT410_INPUT_CH2),
        set_func=lambda instr, value: instr.write_ch(instr.ZT410_CMD_CHAN_STAT, instr.ZT410_INPUT_CH2, value)
    )

    ch_range = [
        ValueDeviceOption(
            'Range CH' + str(i+1), 'V',
            get_func=lambda instr, ch=i:
            instr.query_ch(instr.ZT410_CMD_VERT_RANGE, ch),
            set_func=lambda instr, value, ch=i:
            instr.write_ch(instr.ZT410_CMD_VERT_RANGE, ch, value)
            )
        for i in range(0, 2)]

    ch_offset = [
        ValueDeviceOption(
            'Offset CH' + str(i+1), 'V',
            get_func=lambda instr, ch=i:
            instr.query_ch(instr.ZT410_CMD_VERT_OFFSET, ch),
            set_func=lambda instr, value, ch=i:
            instr.write_ch(instr.ZT410_CMD_VERT_OFFSET, ch, value)
            )
        for i in range(0, 2)]

    ch_atten = [
        ValueDeviceOption(
            'Attenuation CH' + str(i+1), None,
            get_func=lambda instr, ch=i:
            instr.query_ch(instr.ZT410_CMD_VERT_ATTEN, ch),
            set_func=lambda instr, value, ch=i:
            instr.write_ch(instr.ZT410_CMD_VERT_ATTEN, ch, value)
            )
        for i in range(0, 2)]

    ch_coup = [
        ListDeviceOption(
            'Coupling CH' + str(i+1), ['AC', 'DC'],
            get_func=lambda instr, ch=i:
            'DC' if instr.query_ch(instr.ZT410_CMD_VERT_COUP, ch) == '1' else 'AC',
            set_func=lambda instr, value, ch=i:
            instr.write_ch(instr.ZT410_CMD_VERT_COUP, ch, '1' if value == 'DC' else '0')
            )
        for i in range(0, 2)]

    ch_imp = [
        ListDeviceOption(
            'Impedance CH' + str(i+1) + ', Ohm', ['50.0', '1000000.0'],
            get_func=lambda instr, ch=i:
            instr.query_ch(instr.ZT410_CMD_VERT_IMP, ch),
            set_func=lambda instr, value, ch=i:
            instr.write_ch(instr.ZT410_CMD_VERT_IMP, ch, value)
            )
        for i in range(0, 2)]
        