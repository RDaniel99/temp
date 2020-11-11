from Crypto.Cipher import AES

def add_padding_to_string(string):
    while len(string) % 16 != 0:
        string += ' '

    return string

def encrypt_block(key, msg):
    key_bytes = bytes(key, encoding='utf-8')
    cipher = AES.new(key_bytes, AES.MODE_ECB)
    ciphertext = cipher.encrypt(bytes(msg, encoding='utf-8'))

    return ciphertext

def decrypt_block(key, msg):
    key_bytes = bytes(key, encoding='utf-8')
    cipher = AES.new(key_bytes, AES.MODE_ECB)
    plaintext = cipher.decrypt(msg)
    return plaintext.decode('utf-8')

def xor_on_strings(str1, str2):
    return ''.join([chr(ord(a) ^ ord(b)) for a,b in zip(str1, str2)])
