import time 
import random
import string
import textwrap

from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP

import ast

n = 32

# IMPLEMENTATION OF RSA BLOCK CIPHER WITH n-byte BLOCKS
def encrypt(message):
    if len(message) == 0:
        return
    public_key = RSA.import_key(open("./data/public.pem").read())
    cipher_rsa = PKCS1_OAEP.new(public_key)
    message = [message[i:i+n] for i in range(0, len(message), n)]
    ciphertext = list()
    total_length = 0
    for block in message:
        one_block = cipher_rsa.encrypt(block)
        ciphertext.append(one_block)
        total_length += len(one_block)
    print("*** CIPHERTEXT LENGTH:", total_length)
    return ciphertext

def decrypt(ciphertext):
    if len(ciphertext) == 0:
        return
    private_key = RSA.import_key(open("./data/private.pem").read())
    decipher_rsa = PKCS1_OAEP.new(private_key)
    decrypted = ""
    for block in ciphertext:
        decrypted += str(decipher_rsa.decrypt(block))
    return decrypted

def main():
    n = 4096
    message = "".join(random.choice(string.ascii_lowercase) for x in range(n)).encode("utf-8")

    # --------------------KEY-GENERATION--------------------
    # print("Generating keys...")
    # start_time = time.time()
    # key = RSA.generate(2048)
    # stop_time = time.time()
    # print("KEY GENERATION: ", stop_time - start_time, "seconds")
    # f = open("./data/private.pem", "wb")
    # f.write(key.export_key("PEM"))
    # f.close()
    # f = open("./data/public.pem", "wb")
    # f.write(key.publickey().export_key("PEM"))
    # f.close()
    # print("Keys generated successfully.")

    start_time = time.time()
    enc = encrypt(message)
    finish_time = time.time()
    print("Encryption took", finish_time - start_time, "seconds.")
    start_time = time.time()
    dec = decrypt(enc)
    finish_time = time.time()
    print("Decryption took", finish_time - start_time, "seconds.")

if __name__ == "__main__":
    main()
