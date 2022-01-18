import os
import random
import math
import numpy as np

import sys

from .math_module import MathModule

class EncryptionModule:
    def __init__(self, mode = "ECB", generate_new_keys = True):
        self.__mm = MathModule()

        self.__data_directory = "./data"
        self.__public_key_file = "public_key.txt"
        self.__private_key_file = "private_key.txt"
        self.__block_size = 32   # in bytes
        self.__chosen_mode = mode
        self.__bits = 860   # for 2048-bit key values - TODO: not really, the size might be greater than the number of bytes the number actually needs (use 1024) 

        # Initializing an initialization vector, which is a self.__block_size byte long random number
        self.__iv = random.randrange(2 ** (8 * self.__block_size - 1), 2 ** (8 * self.__block_size) - 1)    # used for CBC mode of operation

        print("[INFO] Using", self.__chosen_mode, "mode with", self.__block_size, "byte block size.")

        # If generate_new_keys is False, but there are no private and
        # public key files generated then the program generates them anyway.
        if generate_new_keys:
            self.__generate_pair_of_keys()
        else:
            # Check whether the data directory exists
            if not os.path.isdir(self.__data_directory):
                os.mkdir(self.__data_directory)
            
            private_key_filename = self.__data_directory + "/" + self.__private_key_file
            public_key_filename = self.__data_directory + "/" + self.__public_key_file
            
            if not (os.path.isfile(private_key_filename) and os.path.isfile(public_key_filename)):
               self.__generate_pair_of_keys() 

    def get_mode(self):
        return self.__chosen_mode

    def get_block_size(self):
        return self.__block_size

    def set_mode(self, mode):
        if mode != "ECB" and mode != "CBC":
            return
        self.__chosen_mode = mode

    def set_block_size(self, new_size):
        self.__block_size = new_size

    def generate_pair_of_keys(self):
        '''
        This method generates a pair of keys - public and private
        and saves them in two separate files. Since both the public
        and the private key contains the information about the n value
        being a product of two chosen large primes, then the first line
        in the created files will be this value and the second line will
        be either e (public key case) or d (private key case) value.
        '''

        print("[INFO] Generation a new pair of keys...")

        # p, q = self.__m.choose_random_primes()
        p = self.__mm.generate_large_prime(self.__bits)
        q = self.__mm.generate_large_prime(self.__bits)

        n = p * q
        phi = (p - 1) * (q - 1)

        e = self.__choose_encryption_value(phi)
        d = self.__mm.calculate_multiplicative_inverse(e, phi)
        
        # Save generated keys to corresponding files
        if not os.path.isdir(self.__data_directory):
            os.mkdir(self.__data_directory)

        self.__save_public_key(n, e)
        self.__save_private_key(n, d)

        print("[INFO] Generation of new pair of keys finished.")

    def encrypt(self, message):
        '''
        This method encrypts a given message in a specified 
        mode of operation (ECB or CBC) using the public key
        that was previously generated and saved to a file.
        '''

        if self.__chosen_mode == "ECB":
            return self.__encrypt_ECB(message)
        elif self.__chosen_mode == "CBC":
            return self.__encrypt_CBC(message) 

    def decrypt(self, ciphertext):
        '''
        This method decrypts a given ciphertext in a specified 
        mode of operation (ECB or CBC) using the private key
        that was previously generated and saved to a file.
        '''

        if self.__chosen_mode == "ECB":
            return self.__decrypt_ECB(ciphertext)
        elif self.__chosen_mode == "CBC":
            return self.__decrypt_CBC(ciphertext)

    def __encrypt_ECB(self, message):
        '''
        Description:
        1) We create an empty list of message blocks (blocks of size equal to self.__block_size bytes),
        2) We create and initialize a message_block_value with the ASCII value of the message's first character,
        3) Then we iterate over the rest of message's characters and add their ASCII values to the subsequent blocks,
        4) One block contains a number which is in a form of 4 concatenated ASCII decimal values of the characters,
        5) This number (one block) is then taken to power of e and applied modulo n on,
        6) The obtained value will be the one ciphertext block value of of one message block,
        '''

        if len(message) == 0:
            return

        n, e = self.__load_public_key()
        blocks = list()
        block_value = ord(message[0])
        for i in range(1, len(message)):            
            # If the mas block size is reached add the ciphertext to the list and reset it
            if i % self.__block_size == 0:
                blocks.append(block_value)
                block_value = 0

            # Multiply by 1000 to shift the number by 3 digits to the left
            block_value = block_value * 1000 + ord(message[i])

        # Adding the last block
        blocks.append(block_value)

        # Encrypt all of the numbers
        for i in range(len(blocks)):
            block = str(pow(blocks[i], e, n))
            blocks[i] = block

        ciphertext = " ".join(blocks)

        return ciphertext

    def __decrypt_ECB(self, ciphertext):
        '''
        Description:
        1) The ciphertext is a string made of blocks of integer values separated by spaces.
        2) We split this ciphertext string into a list of string blocks, which represent some integer value,
        3) We convert those string blocks into integer blocks and obtain a list of integer values,
        4) We iterate over that list and decrypt the blocks one by one by applying the power to d and modulo n,
        5) Then we receive a list of decrypted blocks of integer values,
        6) We transform the list of decrypted integer values block by block into a string of characters.
        '''

        if len(ciphertext) == 0:
            return

        n, d = self.__load_private_key()
        blocks = ciphertext.split()

        for i in range(len(blocks)):
            blocks[i] = int(blocks[i])

        decrypted_message = ""

        for i in range(len(blocks)):
            decrypted_block = pow(blocks[i], d, n)
            blocks[i] = decrypted_block

            tmp = ""

            for c in range(self.__block_size):
                tmp = chr(blocks[i] % 1000) + tmp
                blocks[i] //= 1000
            decrypted_message += tmp

        return decrypted_message

    def __encrypt_CBC(self, message):
        '''
        Description:
        1) We create an empty list of message blocks (blocks of size equal to self.__block_size bytes),
        2) We create and initialize a message_block_value with the ASCII value of the message's first character,
        3) Then we iterate over the rest of message's characters and add their ASCII values to the subsequent blocks,
        4) One block contains a number which is in a form of 4 concatenated ASCII decimal values of the characters,
        5) This number (one block) is then XOR'ed with the previous block's encrypted value and then taken to the power e and applied modulo n
           (in case of the first block we use the initialization vector for the XOR operation),
        6) The obtained value will be the one ciphertext block value of of one message block,
        '''

        if len(message) == 0:
            return

        n, e = self.__load_public_key()
        blocks = list()
        block_value = ord(message[0])
        for i in range(1, len(message)):            
            # If the mas block size is reached add the ciphertext to the list and reset it
            if i % self.__block_size == 0:
                blocks.append(block_value)
                block_value = 0

            # Multiply by 1000 to shift the number by 3 digits to the left
            block_value = block_value * 1000 + ord(message[i])

        # Adding the last block
        blocks.append(block_value)

        # Encrypt all of the numbers
        xor_value = self.__iv
        for i in range(len(blocks)):
            blocks[i] ^= xor_value
            encrypted_value = pow(blocks[i], e, n)
            xor_value = encrypted_value
            block = str(encrypted_value)
            blocks[i] = block

        ciphertext = " ".join(blocks)

        return ciphertext


    def __decrypt_CBC(self, ciphertext):
        '''
        Description:
        1) The ciphertext is a string made of blocks of integer values separated by spaces.
        2) We split this ciphertext string into a list of string blocks, which represent some integer value,
        3) We convert those string blocks into integer blocks and obtain a list of integer values,
        4) We iterate over that list and decrypt the blocks one by one by applying the power d and then modulo n,
            4.1) After each block's decryption we apply a XOR operation with the previous block's encrypted value
                 (in case of the first block we use the initialization vector for the XOR operation),
        5) Then we receive a list of decrypted blocks of integer values,
        6) We transform the list of decrypted integer values block by block into a string of characters.
        '''

        if len(ciphertext) == 0:
            return

        n, d = self.__load_private_key()
        blocks = ciphertext.split()

        for i in range(len(blocks)):
            blocks[i] = int(blocks[i])

        decrypted_message = ""


        xor_value = self.__iv
        for i in range(len(blocks)):
            decrypted_value = pow(blocks[i], d, n) ^ xor_value
            xor_value = blocks[i]
            blocks[i] = decrypted_value

            tmp = ""

            for j in range(self.__block_size):
                tmp = chr(blocks[i] % 1000) + tmp
                blocks[i] //= 1000
            decrypted_message += tmp

        return decrypted_message

    def __choose_encryption_value(self, phi):
        '''
        This method chooses an encryption value between
        1 and phi exclusive, which is relatively prime with phi.
        '''

        while True:
            e = random.randrange(2, phi)
            if (math.gcd(e, phi) == 1):
                break
        return e

    def __save_private_key(self, n, d):
        '''
        This method saves a private key to a file in a
        hesadecimal format.
        '''

        filename = self.__data_directory + "/" + self.__private_key_file
        file = open(filename, "w")
        n_hex_str = self.__convert_int_to_hex_string(n)
        d_hex_str = self.__convert_int_to_hex_string(d)
        file.write(n_hex_str + "\n")
        file.write(d_hex_str + "\n")
        file.close()

    def __save_public_key(self, n, e):
        '''
        This method saves a public key to a file in a
        hesadecimal format.
        '''

        filename = self.__data_directory + "/" + self.__public_key_file
        file = open(filename, "w")
        n_hex_str = self.__convert_int_to_hex_string(n)
        e_hex_str = self.__convert_int_to_hex_string(e)
        file.write(n_hex_str + "\n")
        file.write(e_hex_str + "\n")
        file.close()

    def __load_private_key(self):
        '''
        This method loads a private key from a file in which it was
        saved in a hexadecimal format.
        '''

        private_key_filename = self.__data_directory + "/" + self.__private_key_file
        file = open(private_key_filename, "r")    
        lines = file.read().splitlines()
        n = self.__convert_hex_string_to_int(lines[0])
        d = self.__convert_hex_string_to_int(lines[1])
        file.close()
        return (n, d)

    def __load_public_key(self):
        '''
        This method loads a public key from a file in which it was
        saved in a hexadecimal format.
        '''

        public_key_filename = self.__data_directory + "/" + self.__public_key_file
        file = open(public_key_filename, "r")    
        lines = file.read().splitlines()
        n = self.__convert_hex_string_to_int(lines[0])
        e = self.__convert_hex_string_to_int(lines[1])
        file.close()
        return (n, e)

    def __convert_hex_string_to_int(self, hex_str):
        return int(hex_str, 16)

    def __convert_int_to_hex_string(self, value):
        return str(hex(value)[2:])








































        # TOO LONG EXECUTION (__choose_encryption_value)
        # Find value from the set (1, phi) relatively prime with phi
        # candidates = list()
        # for i in range(2, phi):
        #     if (math.gcd(i, phi) == 0):
        #         candidates.append(i)
        # if len(candidates) == 0:
        #     print("No numbers from the set (1, phi) that are relatively prime with phi were found.")
        #     return
        # index = random.randint(0, len(candidates) - 1)
        # e = candidates[index]