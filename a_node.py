from multiprocessing.connection import Client
from multiprocessing.connection import Listener
import constants as consts
import crypto_utils as crypt

addressKMA = ('localhost', 6000)
addressAB = ('localhost', 6001)
addressBA = ('localhost', 6002)
listenerToKM = Listener(addressKMA, authkey=bytes('0101001', 'utf-8'))
listenerToB = Listener(addressBA, authkey=bytes('0101001', 'utf-8'))

# primim K de la KM
K = ''
connToKMJustReceive = listenerToKM.accept()
print('connection accepted from KM: ', listenerToKM.last_accepted)
while True:
    msg = connToKMJustReceive.recv()
    if msg == 'close':
        connToKMJustReceive.close()
        break
    K = msg

listenerToKM.close()

# trimitem mesaj catre B cu modul si cheia in aceasta ordine

connToBJustSend = Client(addressAB, authkey=bytes('0101001', 'utf-8'))
connToBJustSend.send(consts.mode)
connToBJustSend.send(K)
connToBJustSend.send('close')
connToBJustSend.close()

K = crypt.decrypt_block(consts.Kprim, K)

print(K)

# primim msj de confirmare de la B pt inceperea comunicarii

connToBJustReceive = listenerToB.accept()
print('connection accepted from B: ', listenerToB.last_accepted)

while True:
    msg = connToBJustReceive.recv()
    if msg == 'close':
        connToBJustReceive.close()
        break

listenerToB.close()

file = open("file.txt")

line = file.read().replace("\n", " ")
file.close()

line = crypt.add_padding_to_string(line)
print(len(line))

connToBJustSend = Client(addressAB, authkey=bytes('0101001', 'utf-8'))

if consts.mode == 1:
    i = 0
    j = 16

    while i < len(line):
        block = line[i:j]
        connToBJustSend.send(crypt.encrypt_block(K, block))
        i += 16
        j += 16
else:
    vinit = consts.V_INITIAL

    i = 0
    j = 16
    
    while i < len(line):
        block = line[i:j]
        block = crypt.xor_on_strings(block, vinit)
        vinit = block

        connToBJustSend.send(crypt.encrypt_block(K, block))

        i += 16
        j += 16

connToBJustSend.send('close')
connToBJustSend.close()