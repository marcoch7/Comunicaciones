import numpy as np
import matplotlib.pyplot as plt

#Abrir archivo txt para transmitir
with open('info.txt','r') as rf:
    info = rf.read()
  
#Convertir a ASCII
results_in_ASCII = list(info.encode(encoding='us-ascii'))

#Convertir a binario
result_in_binary = []
for symbol in results_in_ASCII:
    result_in_binary.append((bin(symbol)[2:]).zfill(8))

#Mismo canal de transmición 
channel = []
for bits in result_in_binary:
   for i in range(len(bits)):
            channel.append(bits[i])
     

#Hasta aqui llega la codificacion, los caracteres se envian en codigo ascii en paquetes de 8 bits

# Matriz G
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

#Empieza modulacion

#print(u0)
bits = []
for block in u0:
    for i in range(int(len(block)/2)):
        bits.append(block[2*i:(2*i)+2])
        
#print(bits)

pts = 50

T_bit = 2E-6

#print(T_bit)

def pulse(T):
    pulse = np.array([])
    for element in T:
        pulse = np.append(pulse,[1])
    return pulse

tp = np.linspace(0, T_bit, pts)

pulse = pulse(tp)

t = np.linspace(0, len(bits)*T_bit, len(bits)*pts)

senal = np.zeros(t.shape) 

# Senal modulada PAM

for p,b in enumerate(bits):
    p_e = 0.10  # porcentaje de error
    if (b[0]%2  == 0 and b[1]%2 == 0): #00
        senal[p*pts:(p+1)*pts] = -10*pulse
    elif (b[0]%2  == 0 and b[1]%2 != 0): #01
        senal[p*pts:(p+1)*pts] = -5*pulse
    elif (b[0]%2  != 0 and b[1]%2 == 0): #10
        senal[p*pts:(p+1)*pts] = 5*pulse
    elif (b[0]%2  != 0 and b[1] != 0): #11
        senal[p*pts:(p+1)*pts] = 10*pulse
    #agregar el ruido
    for i in range(p*pts,((p+1)*pts)):
        prob = np.random.rand(1) 
        if (prob <= p_e):
            decimal=np.random.rand(1)
            if(b[0]%2  == 0 and b[1]%2 == 0):
                entero=np.random.randint(6,14)
                numeroerror=-entero-decimal
                senal[i]=numeroerror
            if(b[0]%2  == 0 and b[1]%2 != 0):
                entero=np.random.randint(1,9)
                numeroerror=-entero-decimal
                senal[i]=numeroerror
            if(b[0]%2  != 0 and b[1]%2 == 0):
                entero=np.random.randint(1,9)
                numeroerror=entero+decimal
                senal[i]=numeroerror
            if(b[0]%2  != 0 and b[1] != 0):
                entero=np.random.randint(6,14)
                numeroerror=entero+decimal
                senal[i]=numeroerror


senal = senal[int(pts/2):]
t = t[:-int(pts/2)]

# Visualizacion de los primeros bits modulados
pb = 10
plt.plot(t[0:pb*pts],senal[0:pb*pts])
plt.title('Visualizacion de los primeros 10 bloques de bits modulados con ruido')
plt.ylabel('Amplitud')
plt.xlabel('tiempo(s)')
plt.savefig('senalconruido.png')
plt.close()



#Empieza demodulacion

#Muestreo

muestreo = []
for i in range(len(bits)):
    muestreo.append(senal[i*len(tp)])

#Decision y simbolo a bits

des = []
for valor in muestreo:
    if(valor < -7.5):
        zz = [0,0]
        des.append(zz)
    elif(valor > -7.5 and valor < 0):
        zo = [0,1]
        des.append(zo)
    elif(valor > 0 and valor < 7.5):
        oz = [1,0]
        des.append(oz)
    elif(valor > 7.5):
        oo = [1,1]
        des.append(oo)


#bloques de 6 bits nuevamente
u0_d = []
for i in range(len(u0)):
    aux = des[i*3:(i*3)+3]
    eight = np.array([])
    for bits in aux:
        for i in range(len(bits)):
            eight = np.append(eight,int(bits[i]))
    u0_d.append(eight)


# Matriz H

H = np.array([[1,0,0],[0,1,0],[0,0,1],[1,1,0],[0,1,1],[1,0,1]])

# S = vH
S = []
for i in range(len(u0_d)):
    So = np.dot(u0_d[i],H)
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

#print("\nANTES Sb: ")    
#print(Sb)    
#print("\nSe: ")   
#print(Se) 
i = 0 
indexe = []
if(len(Se)>0):
    for i in range(len(Se)):
        temp = en.copy()
        Sb.append(np.dot(en,H))
        comparison = Sb[i] == Se[i]
        equal = comparison.all()
        a = 0
        em = 0
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
                    if(em == 10):
                        break




# Correccion de errores
if(len(e0)>0):
    for i in range(len(e0)): 
        for j in range(len(e0[0])):
            if(e0[i][j] == 1):
                indexe.append(j)
        if(u0[indexv[i]][indexe[i]] == 0):
            u0[indexv[i]][indexe[i]] = 1     
        else: 
            u0[indexv[i]][indexe[i]] = 0  
    
#Pasar v0 corregido de matrix a array
v0f = []
for bits in u0:
   for i in range(len(bits)):
        if(i>2):
            if(bits[i] == 0):
                v0f.append('0')
            else:
                v0f.append('1')     

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