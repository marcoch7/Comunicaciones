import numpy as np
#Abrir archivo txt para transmitir
with open('info_.txt','r') as rf:
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

# S = vH
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

flag_a = 0
flag_b = 0
flag_temp = 0
def moreen(array, f_a, f_b, f_temp):
    if(f_a):
        if(f_b):
            array = [0,0,0,0,0,0]
        for i in range(6):
            if(i == 0):
                if((f_temp > 32 and f_temp < 65)):
                    array[0] = 1
                else:
                    array[0] = 0 
            elif(i==1):
                if((f_temp > 16 and f_temp < 32) or (f_temp > 48 and f_temp < 65)):
                    array[1] = 1
                else:
                    array[1] = 0 
            elif(i==2):
                if((f_temp > 8 and f_temp < 17) or (f_temp > 24 and f_temp < 33) or (f_temp > 40 and f_temp < 49) or (f_temp > 56)):
                    array[2] = 1
                else:
                    array[2] = 0 
            elif(i==3):
                if((f_temp > 3 and f_temp < 9) or (f_temp > 12 and f_temp < 17) or (f_temp > 20 and f_temp < 25) or (f_temp > 28 and f_temp < 33) or (f_temp > 36 and f_temp < 41) or (f_temp > 44 and f_temp < 49) or (f_temp > 52 and f_temp < 57) or (f_temp > 60)):
                    array[3] = 1
                else:
                    array[3] = 0   
            elif(i==4):
                if((f_temp > 2 and f_temp < 5) or (f_temp > 6 and f_temp < 9) or (f_temp > 10 and f_temp < 13) or (f_temp > 14 and f_temp < 17) or (f_temp > 18 and f_temp < 21) or (f_temp > 22 and f_temp < 25) or (f_temp > 26 and f_temp < 29) or (f_temp > 30 and f_temp < 33) or (f_temp > 34 and f_temp < 37) or (f_temp > 38 and f_temp < 41) or (f_temp > 42 and f_temp < 45) or (f_temp > 46 and f_temp < 49) or (f_temp > 50 and f_temp < 53) or (f_temp > 54 and f_temp < 57) or (f_temp > 58 and f_temp < 61) or (f_temp > 62 and f_temp < 65)):
                    array[4] = 1
                else:
                    array[4] = 0  
            elif(i==5):
                if(array[5] == 0):
                    array[5] = 1
                else:
                    array[5] = 0           
        return array 
    else:
        return array   
       

#print("\nANTES Sb: ")    
#print(Sb)    
#print("\nSe: ")   
#print(Se) 
prueba = 0
em = 0 
indexe = []
if(len(Se)>0):
    for i in range(len(Se)):
        flag_a = 0
        temp = en.copy()
        Sb.append(np.dot(en,H))
        comparison = Sb[i] == Se[i]
        equal = comparison.all()
        em = 0
        a = 0
        if(equal):
            e0.append(temp)
        else:  
            while(a == 0):
                Sb[i] = np.dot(en,H)
                comparison = Sb[i] == Se[i]
                equal = comparison.all()
                if(equal):
                    a = 1
                    e0.append(temp)
                else:
                    shift(en)
                    em += 1
                    if(em == 6):
                        flag_a = 1
                        flag_b = 1
                        flag_temp = 0
                        moreen(en,flag_a,flag_b,flag_temp)
                    if(em > 6):
                        flag_b = 0
                        flag_temp += 1
                        moreen(en,flag_a,flag_b,flag_temp)
                        prueba = 1

               
                             

#print("\nDESPUES Sb: ")    
#print(Sb)    
#print("\nSe: ")   
#print(Se)
print("\ne0: ")   
print(e0)
print("\nindexv: ")
print(indexv)
#print("\nv0: ")
#print(v0)

# Correccion de errores
if(len(e0)>0):
    for i in range(len(e0)): 
        for j in range(len(e0[0])):
            if(e0[i][j] == 1):
                indexe.append(j)
        if(v0[indexv[i]][indexe[i]] == 0):
            v0[indexv[i]][indexe[i]] = 1     
        else: 
            v0[indexv[i]][indexe[i]] = 0  
    #print("\nindexe:")
    #print(indexe) 
    #print("\nv0 corregido:")     
    #print(v0)
    
#Pasar v0 corregido de matrix a array
v0f = []
for bits in v0:
   for i in range(len(bits)):
        if(i>2):
            if(bits[i] == 0):
                v0f.append('0')
            else:
                v0f.append('1')     
#print("\nv0f:")    
#print(v0f)     
#print("\ncanal:")
#print(channel)

#Decodificar los bits en paquetes de 8 bits
decoded_bits = []
for i in range(int(len(v0f)/8)):
    aux = ''.join(v0f[i*8:(i*8)+8])
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
print(len(v0f))
if(prueba):
    print("\nentroooooooo")