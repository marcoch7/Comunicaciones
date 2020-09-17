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

# desconvertir xd

ud = []
for bits in u0:
   for i in range(len(bits)):
            ud.append(bits[i])
print("u desconvertidos: \n")    
print(ud)  


    
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