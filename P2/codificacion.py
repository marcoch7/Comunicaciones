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

#Canal binario simetrico
channel = []
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
                channel.append("1")

#Hasta aqui llega la codificacion, los caracteres se envian en codigo ascii en paquetes de 8 bits

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