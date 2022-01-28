# -*- coding: utf-8 -*-
"""
Created on Fri Jan 28 16:05:58 2022

@author: cfgar
"""


bit_values = {'0000':1, '0001':2, '0010':3, '0011':4, '0100':5, '0101':6, '0110':7, '0111':8, '1000':9, '1001':10, '1010':11, '1011':12, '1100':13, '1101':14, '1110':15, '1111':16} 

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

       
modulation = MOM()
texte = 'Toto'

encodage = modulation.encoding(texte)
print(encodage,'\n')
decodage = modulation.decoding(encodage)
print(decodage)