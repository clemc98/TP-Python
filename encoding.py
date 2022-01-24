bit_values = {'0000':1, '0001':2, '0010':3, '0011':4, '0100':5, '0101':6, '0110':7, '0111':8, '1000':9, '1001':10, '1010':11, '1011':12, '1100':13, '1101':14, '1110':15, '1111':16} 

#formatage d'un groupe de caractères en deux blocs de 4 bits
st  = 'toto'
st_voltage = []
st_bytes = ' '.join(format(ord(x), 'b') for x in st)


for i in range(len(st)):
#prend les blocs de 4 bits pour chaque lettre  
    st_bytes_bloc = ''.join(format(ord(st[i]), 'b'))
    fin = st_bytes_bloc[-4:]
    debut = st_bytes_bloc.replace(fin, '') #on passe d'un str de len <= 8 à un str de len <=4
    print(debut, fin)
    
#rajoute un ou plusieurs zéros au 
    while len(debut) < 4 :
        debut = '0' + debut    
    print(debut, fin,'\n')
    
#on donne les valeurs 
    st_voltage.append([bit_values.get(debut), bit_values.get(fin)])
    print('La valeur associée à    ', st[i],'    est', st_voltage[i],'V \n')
