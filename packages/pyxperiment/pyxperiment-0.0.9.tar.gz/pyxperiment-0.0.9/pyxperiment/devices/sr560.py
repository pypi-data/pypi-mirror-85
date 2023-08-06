"""
TODO: restore functionality
class SR560Preamplifier(VisaInstrument):
    SR560 support

    @staticmethod
    def driver_name():
        return 'SR560 Low-noise Preamplifier'

    def __init__(self,rm,resource):
        super().__init__(rm,resource)
        self.write('LALL')

    def device_name(self):
        return 'SR560 Low-noise Preamplifier'

    def reset(self):
        self.write('*RST')

    def recover(self):
        self.write('ROLD')

    @control('Source',ControlType.LIST)
    @values_list(['A', 'A-B', 'B'])
    def source(self,value):
        self._write_value_from_list('SRCE ',value,self.source.values)

    @control('Coupling',ControlType.LIST)
    @values_list(['GND', 'DC', 'AC'])
    def coupling(self,value):
        self._write_value_from_list('CPLG ',value,self.coupling.values)

    @control('Reserve',ControlType.LIST)
    @values_list([
        'Low noise', 'High reserve', 'Calibrated (normal)'
        ])
    def reserve(self,value):
        self._write_value_from_list('DYNR ',value,self.reserve.values)

    @control('Vernier on',ControlType.BOOLEAN)
    def vernier_on(self,value):
        self.write('UCAL ' + ('1' if value else '0'))

    @control('Vernier',ControlType.VALUE)
    def vernier(self,value):
        value = int(value)
        if value > 0 and value < 101:
            self.write('UCGN ' + str(value))
        else:
            raise ValueError('Invalid vernier.')

    @control('Invert',ControlType.BOOLEAN)
    def invert(self,value):
        self.write('INVT ' + ('1' if value else '0'))

    @control('Filter mode',ControlType.LIST)
    @values_list([
        'No filter',
        '6 dB/oct LP',
        '12 dB/oct LP',
        '6 dB/oct HP',
        '12 dB/oct HP',
        '6 dB/oct BP'
        ])
    def filter_mode(self,value):
        self._write_value_from_list('FLTM ',value,self.filter_mode.values)

    @control('Low-pass filter',ControlType.LIST)
    @values_list([
        '0.03 Hz', '0.1 Hz',
        '0.3 Hz', '1 Hz',
        '3 Hz', '10 Hz',
        '30 Hz', '100 Hz',
        '300 Hz', '1 kHz',
        '3 kHz', '10 kHz',
        '30 kHz', '100 kHz',
        '300 kHz', '1 MHz'
        ])
    def lp_value(self,value):
        self._write_value_from_list('LFRQ ',value,self.lp_value.values)

    @control('High-pass filter',ControlType.LIST)
    @values_list(lp_value.values[:11])
    def hp_value(self,value):
        self._write_value_from_list('HFRQ ',value,self.hp_value.values)

    @control('Gain',ControlType.LIST)
    @values_list([
        '1', '2', '5',
        '10', '20', '50',
        '100', '200', '500',
        '1000', '2000', '5000',
        '10000', '20000', '50000'
        ])
    def gain(self,value):
        self._write_value_from_list('GAIN ',value,self.gain.values)

    def get_config_class(self):
        return SR560PreamplifierConfig
"""
                