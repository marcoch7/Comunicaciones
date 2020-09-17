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


channel = []
for bits in result_in_binary:
   for i in range(len(bits)):
            channel.append(bits[i])
     


#Hasta aqui llega la codificacion, los caracteres se envian en codigo ascii en paquetes de 8 bits

# Matrix G
G = np.array([[1,1,0,1,0,0],[0,1,1,0,1,0],[1,0,1,0,0,1]])

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

# u0
u0 = []
for i in range(len(m0)):
    u = np.dot(m0[i],G)
    u0.append(u)

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


# Matrix H

H = np.array([[1,0,0],[0,1,0],[0,0,1],[1,1,0],[0,1,1],[1,0,1]])

# S
S = []
for i in range(len(v0)):
    So = np.dot(v0[i],H)
    S.append(So)

Se = []
indexv = []
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
            indexv.append(i)   

# e
# Se = vH
en = [1, 0, 0, 0, 0, 0]
e0 = []
Sb = []   # stores syndrome = eH

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

print("\nANTES Sb: ")    
print(Sb)    
print("\nSe: ")   
print(Se)  
indexe = []
if(len(Se)>0):
    for i in range(len(Se)):
        print("\nen IN")
        print(en)
        Sb.append(np.dot(en,H))
        comparison = Sb[i] == Se[i]
        equal = comparison.all()
        print("\nequal")
        print(equal)
        a = 0
        print("\nen OUT")
        print(en)
        if(equal):
            print("\nentra al if")
            e0.append(en)
        else: 
            print("\nentra al else")   
            while(a == 0):
                print("\nentra al while") 
                Sb[i] = np.dot(en   ,H)
                comparison = Sb[i] == Se[i]
                equal = comparison.all()
                if(equal):
                    a = 1
                    e0.append(en)
                else:
                    shift(en)

print("\nDESPUES Sb: ")    
print(Sb)    
print("\nSe: ")   
print(Se)
print("\ne0: ")   
print(e0)
print("\nindexv: ")
print(indexv)
print("\nv0: ")
print(v0)

# Correccion de errores
for i in range(len(e0)): 
    for j in range(len(e0[0])):
        if(e0[i][j] == 1):
            indexe.append(j+1)
print("\nindexe:")
print(indexe)    












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