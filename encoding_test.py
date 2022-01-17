import numpy as np


amplitude_values = np.array([i for i in range(1, 17, 1)])
bit_values = {'0000', '0001', '0010', '0011', '0100', '0101', '0110', '0111', '1000', '1001', '1010', '1011', '1100', '1101', '1110', '1111'} 

                                            


st  = 'a'
st_bytes = ' '.join(format(ord(x), 'b') for x in st)
fin = st_bytes[-4:]
debut = st_bytes[:3]

print(debut, fin)

print(st_bytes)
diff = 8 - len(st_bytes)
print(diff)

voltage = bit_values.index(fin)
print(voltage)
