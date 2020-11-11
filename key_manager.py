import crypto_utils as crypt
import constants as consts
from multiprocessing.connection import Listener
from multiprocessing.connection import Client

import random
import string

def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    print("Random string of length", length, "is:", result_str)

K = 'OCheieDoarEuStiu'

print('[KM] Started')

addressKMA = ('localhost', 6000)
connToAJustSend = Client(addressKMA, authkey=bytes('0101001', 'utf-8'))

msg = crypt.encrypt_block(consts.Kprim, K)

connToAJustSend.send(msg)
connToAJustSend.send('close')
connToAJustSend.close()