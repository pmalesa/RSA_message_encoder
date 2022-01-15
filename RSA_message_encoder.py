import os
import sys
from gui_module.message_encoder_gui import MessageEncoderGUI
from encryption_module.encryption_module import EncryptionModule

def main():
    em = EncryptionModule(mode = "ECB", generate_new_keys = False)

    message = "Hello, my name is Piotr Malesa and I am a student"
    print("Message:", message)
    ciphertext = em.encrypt(message)
    # print("Encrypted message:", ciphertext)
    decrypted_ciphertext = em.decrypt(ciphertext)
    print("Decrypted message:", decrypted_ciphertext)

    # me_gui = MessageEncoderGUI()
    # me_gui.run()    

    return 0

if __name__ == "__main__":
    main()
