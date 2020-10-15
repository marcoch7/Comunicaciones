import numpy as np
from scipy.interpolate import interp1d
from numpy import array, sign, zeros
from matplotlib.pyplot import plot,show,grid
import matplotlib.pyplot as plt
from scipy import integrate
from scipy.signal import hilbert, chirp

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


bits = []
for block in u0:
    for i in range(int(len(block)/2)):
        bits.append(block[2*i:(2*i)+2])
        
# Cantidad de puntos por simbolo
pts = 50

T_bit = 1/100
# Tiempo de simbolo
T_sim = T_bit
# Constante 
cnst = np.sqrt(2/T_sim)

tp = np.linspace(0, T_bit, pts)

t = np.linspace(0, len(bits)*T_bit, len(bits)*pts)  

senal = np.zeros(t.shape) 
fc = 5/T_bit

# Señal sinusoidal
tp = np.linspace(0, T_bit, 50)
cosine = np.cos(2*np.pi *fc * tp)

# Senal modulada 4-ASK
for p,b in enumerate(bits):
    if (b[0]%2  == 0 and b[1]%2 == 0): #00
        senal[p*pts:(p+1)*pts] = -10*cnst*cosine
    elif (b[0]%2  == 0 and b[1]%2 != 0): #01
        senal[p*pts:(p+1)*pts] = -5*cnst*cosine
    elif (b[0]%2  != 0 and b[1]%2 == 0): #10
        senal[p*pts:(p+1)*pts] = 5*cnst*cosine
    elif (b[0]%2  != 0 and b[1]%2 != 0): #11
        senal[p*pts:(p+1)*pts] = 10*cnst*cosine
    # agregar el ruido
    p_e = 0.1 # porcentaje de ruido
    for i in range(p*pts,((p+1)*pts)):
        prob = np.random.rand(1) 
        if (prob <= p_e):
            decimal=np.random.rand(1)
            if(b[0]%2  == 0 and b[1]%2 == 0):
                entero=np.random.randint(4*cnst,12*cnst)
                numeroerror=-entero-decimal
                senal[i]=numeroerror
            if(b[0]%2  == 0 and b[1]%2 != 0):
                entero=np.random.randint(4*cnst,10*cnst)
                numeroerror=-entero-decimal
                senal[i]=numeroerror
            if(b[0]%2  != 0 and b[1]%2 == 0):
                entero=np.random.randint(4*cnst,10*cnst)
                numeroerror=entero+decimal
                senal[i]=numeroerror
            if(b[0]%2  != 0 and b[1] != 0):
                entero=np.random.randint(4*cnst,12*cnst)
                numeroerror=entero+decimal
                senal[i]=numeroerror

#senal = senal[int(pts/2):]
#t = t[:-int(pts/2)]
# Visualizacion de los primeros bits modulados
pb = 5
plt.plot(t[0:pb*pts],senal[0:pb*pts])
plt.title('Visualizacion de los primeros 5 bloques de bits modulados con ruido')
plt.ylabel('Amplitud')
plt.xlabel('tiempo(s)')
plt.savefig('p7_senalconruido.png')
plt.close()


########################################################################
def envelopes_idx(array,dmin,dmax):
    """
    s : 1d-array, data signal from which to extract high and low envelopes
    dmin, dmax : int, size of chunks, use this if size of data is too big
    """

    # locals min      
    lmin = (np.diff(np.sign(np.diff(array))) > 0).nonzero()[0] + 1 
    # locals max
    lmax = (np.diff(np.sign(np.diff(array))) < 0).nonzero()[0] + 1 

    # global max of dmax-chunks of locals max 
    lmin = lmin[[i+np.argmin(array[lmin[i:i+dmin]]) for i in range(0,len(lmin),dmin)]]
    # global min of dmin-chunks of locals min 
    lmax = lmax[[i+np.argmax(array[lmax[i:i+dmax]]) for i in range(0,len(lmax),dmax)]]

    return lmin,lmax

#pb = 1
#high_idx, low_idx = envelopes_idx(senal[0:pb*pts], 1, 1)
## plot
#
#plt.plot(t[0:pb*pts],senal[0:pb*pts],label='signal')
#plt.plot(t[high_idx], senal[high_idx], 'r', label='low')
#plt.plot(t[low_idx], senal[low_idx], 'g', label='high')    
#plt.savefig('senal_sin_ruido_3.png')
#plt.close()
########################################################################


#Empieza demodulacion

#Muestreo
muestreo = []
symb = 0
count = 0
valores = []
for i in range(len(bits)):
    if(senal[i*50] < 0):            # valor negativo
        symb = 1
    else:
        symb = 0  
    high_i, low_i = envelopes_idx(senal[i*pts:(i+1)*pts], 1, 1)  
    if(symb == 1):
        l = 0
        for j in range(len(high_i)):
            l = l + senal[pts*i + high_i[j]]
        l = l/len(high_i)
        valores.append(l)
    else:   
        h = 0
        for j in range(len(low_i)):
            h = h + senal[pts*i + low_i[j]]
        h = h/len(low_i) 
        valores.append(h)
#Decision y simbolo a bits
des = []
k = 0
for valor in valores:
    if(valor < -cnst*7.5):
        zz = [0,0]
        des.append(zz)
    elif(valor>-cnst*7.5 and valor<0):
        zo = [0,1]
        des.append(zo)
    elif(valor<cnst*7.5 and valor>0):
        oz = [1,0]
        des.append(oz)
    elif(valor > cnst*7.5):
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



