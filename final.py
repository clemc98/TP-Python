import pyvisa
import matplotlib.pyplot as plt
import numpy as np
import math

bit_values = {'0000':6.25, '0001':12.5, '0010':18.75, '0011':25, '0100':31.25, '0101':37.5, '0110':43.75, '0111':50, '1000':56.25, '1001':62.5, '1010':68.75, '1011':75, '1100':81.25, '1101':87.5, '1110':93.75, '1111':100} 

r = pyvisa.ResourceManager()
print('Liste des appareils connectés :\n', r.list_resources(), '\n')

####################################################################
"""
CLASSE OSCILLO
"""

class Instrument:
    def __init__(self, adresse):
        r = pyvisa.ResourceManager()
        if adresse in r.list_resources():
            self.instrument = r.open_resource(adresse)
        else:
            print(" Appareil non connecté")

    def query(self, str_query):
        return self.instrument.query(str_query, delay=0.1)

    def write(self, str_write):
        return self.instrument.write(str_write)

###################################################################

class DS1054(Instrument) :
    def __init__(self,adresse):
        Instrument.__init__(self,adresse)

    def get_idn(self):
        return self.query('IDN')

    def get_vertical_scale(self,channel):
        return self.query(f':CHANnel{channel}:SCALe?')

    def get_vertical_offset(self,channel):
        return self.query(f':CHANnel{channel}:OFFset?')

    def set_vertical_offset (self, channel, value):
        return self.write(f':CHANnel{channel}:OFFset {value}')

    def get_timebase(self) :
        return self.query(f'TIMebase:MAIN:SCALe?')

    def set_timebase(self, value) :
         return self.write(f'TIMebase:MAIN:SCALe {value}')

    def get_curve(self,channel):
        self.write(f':WAVeform:FORMat ASCII')
        self.write(f':WAVeform:SOURce {channel}')
        self.write(f':WAV:MODE NORM')
        y=self.query(f':WAV:DATA?')
        y=y[11:]
        y=y.split(',')
        y=[float(i) for i in y]
        y=np.array(y)
        # on a donc un tableau numpy de valeurs de tension
        # on a 12 carreaux en longueurs sur le scope
        x=np.linspace(0,float(self.get_timebase())*12,len(y))
        return x,y

    def plot_curve(self,channel):
        x,y=self.get_curve(channel)
        plt.plot(x,y)
        
###################################################################   
  
"""
CLASSE CODAGE-DECODAGE
"""
 
class MOM():
    pass          
        
    def encoding(self, texte):  #texte à encoder             
        st_voltage = []
        for i in range(len(texte)):
            #prend les blocs de 4 bits pour chaque lettre  
            st_bytes_bloc = ''.join(format(ord(texte[i]), 'b'))
            fin = st_bytes_bloc[-4:]
            debut = st_bytes_bloc.replace(fin, '') 
    
            #rajoute un ou plusieurs zéros au 
            while len(debut) < 4 :
                debut = '0' + debut 
                
            #on donne les valeurs 
            st_voltage.append([bit_values.get(debut), bit_values.get(fin)])
            
        #print('Le texte "',texte, '" correspond aux couples de valeurs en volts: \n', st_voltage,'\n')
        return st_voltage
    
############################################################################################################

    def volts_to_list(self, x, y, periode):
         
        volts_list =[[]]
        a=0
        i = 0
        seuil = (max(y)-min(y)) / (100 - 6.25)
        while (a + periode) <= len(x):
            #retourne valeur crete-crete de la fonction dans une periode donnee
            y_max_periode = (seuil*(max(y[a:a+periode]) - 6.25))*1e3
            y_min_periode = (seuil*(min(y[a:a+periode]) - 6.25))*1e3
            target = abs(y_max_periode - y_min_periode)      
            
            #compare la valeur crete crete avec dictionnaire de valeurs et retourne la valeur la plus proche
            min_diff = min(abs(v - target) for v in bit_values.values())
            closest_keys = [v for k,v in bit_values.items() if abs(v-target) == min_diff]
            
            #ajoute dans une liste les amplitudes crete-crete           
            if target != min(y):
                volts_list[i].append(closest_keys[0])          
            else:
                volts_list.append([])
                i += 1
                
            a += periode 
            
        return volts_list  

###############################################################################################    
        
    def decoding(self, amplitude_list):
        def get_key(val):# function to return key for any value in dict 
            for key, value in bit_values.items():
                if val == value:
                    return key
            return "key doesn't exist"
                
        def bin2text(s): #function to transform any 8bit binary info to str
            return "".join([chr(int(s,2))])
        
        voltage_st = ''
        for i in range(len(amplitude_list)):
            #passage de liste avec 2 éléments à str correspondante
            voltage_bytes = get_key(amplitude_list[i][0]) + get_key(amplitude_list[i][1])
            
            #enlève le(s) 0 du début
            while voltage_bytes[0] == '0': 
                voltage_bytes = voltage_bytes.replace(voltage_bytes[0],'', 1)
            
            #re-création de la phrase
            voltage_st = voltage_st + bin2text(voltage_bytes)
            
        #print('La liste',amplitude_list, 'correspond à la chaîne de caractère: \n "', voltage_st,'" \n')
        return voltage_st
 
###########################################################################################       


oscillo = DS1054('USB0::0x1AB1::0x04CE::DS1ZA163454295::INSTR')
oscillo.plot_curve(2)
periode = int((7/1500) / ((float(oscillo.get_timebase())*12)/1200))

"""
x, y = oscillo.get_curve(2)[0], oscillo.get_curve(2)[1]
seuil = (100 - 6.25)/(max(y)-min(y))
y_max_periode = (seuil*abs(y) + 6.25)
"""

modulation = MOM()
print(modulation.encoding('Toto'), '\n')
print(modulation.volts_to_list(oscillo.get_curve(2)[0], oscillo.get_curve(2)[1], periode))
