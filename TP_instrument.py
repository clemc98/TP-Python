# -*- coding: utf-8 -*-
"""
Created on Thu Oct  1 15:16:30 2020

@author: ThibautJacqmin
"""
#r = pyvisa.ResourceManager()
#print('Liste des appareils connectés :\n', r.list_resources())

import pyvisa
import matplotlib.pyplot as plt
import numpy as np


class Instrument():
    def __init__(self, instrument_address=""):
        ressource_manager = pyvisa.ResourceManager()
        instrument_list = list(ressource_manager.list_resources())
        if instrument_address in instrument_list:
            self.instrument = ressource_manager.open_resource(
                instrument_address)
            print(
                f"Loaded instrument is {self.instrument.manufacturer_name} {self.instrument.model_name}")
        else:
            print("Instrument does not exist. The addresses of connected instruments are \n" +
                  "\n".join(instrument_list))

    def query(self, str):
        return self.instrument.query(str, delay=0.1)

    def write(self, str):
        self.instrument.write(str)


class DS1054(Instrument):
    """
        Classe pilote de l'oscilloscope Rigol DS1054
    """

    def __init__(self, instrument_address=""):
        super(DS1054, self).__init__(instrument_address)
        self.instrument.write(':WAV:FORMAT ASCII')

    def get_idn(self):
        return self.query('*IDN?')

    def get_vert_scale(self, channel):
        return float(self.query(f':CHANnel{channel}:SCALe?'))

    def set_vert_scale(self, channel, value):
        self.write(f':CHANnel{channel}:SCALe {str(value)}')

    def get_voffset(self, channel):
        return float(self.query(f':CHANnel{channel}:OFFSet?'))

    def set_voffset(self, channel, value):
        self.write(f':CHANnel{channel}:OFFSet {value}')

    def get_timebase(self):
        return float(self.query(':TIMebase:MAIN:SCALe?'))

    def set_timebase(self, value):
        self.write(f':TIMebase:MAIN:SCALe {value}')

    def get_channel(self):
        return self.query(':WAVeform:SOURce?')

    def set_channel(self, channel):
        self.write(f':WAVeform:SOURce {channel}')

    def get_curve(self, channel):
        self.set_channel(channel)
        print(f'Acquisition de la voie {self.get_channel()}')
        data = np.array(self.query(':WAVEform:DATA?')
                        [11:].split(','), dtype=float)
        times = np.linspace(0, self.get_timebase() * 12, len(data))
        return times, data

    def plot_channel(self, channel):
        times, data = self.get_curve(channel)
        plt.plot(times, data)
        return times, data

    def get_amplitude(self, channel):
        times, data = self.get_curve(channel)
        print(times)


class DG1022(Instrument):
    """
        Classe pilote de l'oscilloscope Rigol DG1022
    """

    def __init__(self, instrument_address=""):
        super(DG1022, self).__init__(instrument_address)

    def set_sinusoide(self, freq, amplitude, offset):
        self.write("VOLT:UNIT:VPP")
        self.write(f"APPL:SIN {freq},{amplitude},{offset}")
        self.write("OUTP ON")


"""
ENCODAGE
"""

amplitude_values = np.array(
    [i for i in range(2, 22, 2)])  # valeurs crete-crete de 2V a 20V
bit_values = [format(i, 'b')
              for i in range(0, 10)]  # valeurs bin binaires de 0 a 9


#oscillo = DS1054("USB0::0x1AB1::0x04CE::DS1ZA203715553::INSTR")
oscillo = DS1054('USB0::0x1AB1::0x04CE::DS1ZA171307560::INSTR')
#generateur = DG1022("USB0::0x1AB1::0x0588::DG1D123203121::INSTR")
#generateur.set_sinusoide(5000, 3, 0)

# oscillo.get_amplitude(1)
#freq = 1.5e3
"""
chiffre = 14

dizaine = chiffre // 10
reste = chiffre % 10

print(dizaine, reste)
print(dizaine, reste)
"""

st = ""
st_bytes = ' '.join(format(ord(x), 'b') for x in st)
"""
for i in st_bytes:
    if len(st_bytes[i]) < 8:
        difference = 8 - len(st_bytes[i])
        st_bytes =  
"""
print(st_bytes)
difference = 8 - len(st_bytes)
print(difference)
