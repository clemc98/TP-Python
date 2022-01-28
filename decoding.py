bit_values = {'0000':1, '0001':2, '0010':3, '0011':4, '0100':5, '0101':6, '0110':7, '0111':8, '1000':9, '1001':10, '1010':11, '1011':12, '1100':13, '1101':14, '1110':15, '1111':16} 

# function to return key for any value in dict bit_values
def get_key(val):
	for key, value in bit_values.items():
		if val == value:
			return key
	return "key doesn't exist"

#function to transform any 8bit binary info to str
def bin2text(s): 
    return "".join([chr(int(s,2))])

#couple d'amplitudes crete crete captées par l'oscillo
amplitude_voltage = [7, 2]

#passage des éléments en volts aux éléments str du dictionnaire resp. en bits
voltage_bytes = get_key(amplitude_voltage[0]) + get_key(amplitude_voltage[0+1])
print(voltage_bytes)

#enleve le 0 artificiellement rajouté avant
while voltage_bytes[0] == '0':
    voltage_bytes = voltage_bytes.replace(voltage_bytes[0],'', 1)
print(voltage_bytes)

#transforme en chaîne de caractères
voltage_to_str = bin2text(voltage_bytes)
print(voltage_to_str)
