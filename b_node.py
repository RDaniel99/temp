from multiprocessing.connection import Client
from multiprocessing.connection import Listener
import constants as consts
import crypto_utils as crypt

addressAB = ('localhost', 6001)
addressBA = ('localhost', 6002)

listenerToA = Listener(addressAB, authkey=bytes('0101001', 'utf-8'))

# primim modul si cheia

K = ''
curr_mode = 0
connToAJustReceive = listenerToA.accept()
print('connection accepted from A: ', listenerToA.last_accepted)
while True:
    msg = connToAJustReceive.recv()
    if msg == 'close':
        connToAJustReceive.close()
        break

    if curr_mode == 0:
        curr_mode = msg
        continue

    K = msg

K = crypt.decrypt_block(consts.Kprim, K)

print(K)

listenerToA.close()

connToAJustSend = Client(addressBA, authkey=bytes('0101001', 'utf-8'))
connToAJustSend.send('close')
connToAJustSend.close()

listenerToA = Listener(addressAB, authkey=bytes('0101001', 'utf-8'))
connToAJustReceive = listenerToA.accept()
print('connection accepted from A: ', listenerToA.last_accepted)

fileText = ""
vinit = consts.V_INITIAL
while True:
    msg = connToAJustReceive.recv()
    if msg == 'close':
        connToAJustReceive.close()
        break

    block = msg

    if curr_mode == 1:
        fileText += crypt.decrypt_block(K, block)
    else:
        block = crypt.decrypt_block(K, block)
        block = crypt.xor_on_strings(block, vinit)
        vinit = block
        
        fileText += block

print(fileText)