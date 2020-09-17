import numpy as np
#Abrir archivo txt para transmitir
with open('info.txt','r') as rf:
    info = rf.read()
  
#Convertir a ASCII
results_in_ASCII = list(info.encode(encoding='us-ascii'))

#Convertir a binario
result_in_binary = []
for symbol in results_in_ASCII:
    result_in_binary.append((bin(symbol)[2:]).zfill(8))
print("b4 channel: \n")   
print(result_in_binary)

channel = []
for bits in result_in_binary:
   for i in range(len(bits)):
            channel.append(bits[i])
print("canal: \n")    
print(channel)        

#Canal binario simetrico
"""channel = []
p_e = 0.01  # porcentaje de error
for bits in result_in_binary:
   for i in range(len(bits)):
        prob = np.random.rand(1)
        if (prob > p_e):
            channel.append(bits[i])
        else:
            if (bits[i] == "1"):
                channel.append("0")
            else:
                channel.append("1")"""

#Hasta aqui llega la codificacion, los caracteres se envian en codigo ascii en paquetes de 8 bits

# Matrix G
G = np.array([[1,1,0,1,0,0],[0,1,1,0,1,0],[1,0,1,0,0,1]])
print("G:\n")
print(G)

# m0
m0 = []
n0 = []
k = 0
j = 0
for i in range(len(channel)):
    if(k<3):
        n0.append(int(channel[i]))
        k += 1
    else: 
        j += 1  
        m0.append(n0)
        n0 = []
        n0.append(int(channel[i]))
        k = 1
print("m0: \n")        
print(m0) 

# u0
print("u0: \n")
u0 = []
for i in range(len(m0)):
    u = np.dot(m0[i],G)
    u0.append(u)
print(u0)

# agregar error

ud = []
p_e = 0.01
for bits in u0:
   for i in range(len(bits)):
        prob = np.random.rand(1)
        numero=bits[i]
        modulo=numero%2
        if (prob > p_e):
            if modulo==0:   
                ud.append(0)
            else:
                ud.append(1)
        else:
            if (bits[i] == "1"):
                ud.append(int(0))
            else:
                ud.append(int(1))           
print("u desconvertidos: \n")    
print(ud) 
print("\n")

# v0
v0 = []
n0 = []
k = 0
j = 0
for i in range(len(ud)):
    if(k<6):
        n0.append(int(ud[i]))
        k += 1
    else: 
        j += 1  
        v0.append(n0)
        n0 = []
        n0.append(int(ud[i]))
        k = 1
print("v0: \n")        
print(v0) 


# Matrix H

H = np.array([[1,0,0],[0,1,0],[0,0,1],[1,1,0],[0,1,1],[1,0,1]])
print("H:\n")
print(H)

# S
print("S: \n")
S = []
for i in range(len(v0)):
    So = np.dot(v0[i],H)
    S.append(So)

Se = []
for i in range(len(S)): 
    k = 0
    for j in range(len(S[0])):
        numero = S[i][j]
        modulo = numero%2
        if modulo==0:   
            S[i][j] = 0
        else:
            S[i][j] = 1  
        if(S[i][j] == 1 and k == 0):
            Se.append(S[i])    
            k = 1    
    print("S:\n")        
    print(S)
    print("en:\n")        
    print(Se)

# e
# Se = vH
en = [1, 0, 0, 0, 0, 0]
c = len(Se)
print(c)
Sb = Se   # stores syndrome = eH

def shift(array):   
    for i in range(0, 1):    
        #Stores the last element of array    
        last = en[len(en)-1]       
        for j in range(len(en)-1, -1, -1):    
        #Shift element of array by one    
            en[j] = en[j-1]         
        #Last element of the array will be added to the start of the array.    
        en[0] = last
        return en

print("en post\n")    
print(en)    
for i in range(len(Se)):
    Sb[i] = np.dot(en,H)
    comparison = Sb[i] == Se[i]
    equal = comparison.all()
    l = 1
    if(equal):
        print("Exito, el vector de error es:\n")
        print(en) 
    else:
        shift(en)
        Sb[i] = np.dot(en,H)
        comparison = Sb[i] == Se[i]
        equal = comparison.all()    
    """while(equal == 0 and l == 0):
        Sb[i] = np.dot(en,H)
        comparison = Sb[i] == Se[i]
        equal = comparison.all()
        if(equal):
            print("Exito, el vector de error es:\n")
            print(en) 
            l = 0  
        else:
            print("no era \n")
            shift(en)""" 

















#Decodificar los bits en paquetes de 8 bits
decoded_bits = []
for i in range(int(len(channel)/8)):
    aux = ''.join(channel[i*8:(i*8)+8])
    decoded_bits.append(aux)


#Decodificar mensaje
decoded_message = ''
for bits in decoded_bits:
    n = int(bits, 2)
    decoded_message += n.to_bytes(1, 'big').decode('us-ascii', 'replace')
    


#Escribir el archivo decodificado y transmitido
with open('transmision.txt','w') as wf:
    wf.write(decoded_message)

print('Transmitiendo ...')
print('Hecho!')