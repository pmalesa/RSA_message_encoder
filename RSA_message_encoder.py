import os
import sys
from gui_module.message_encoder_gui import MessageEncoderGUI
from encryption_module.encryption_module import EncryptionModule

def main():
    me_gui = MessageEncoderGUI()
    me_gui.run()    

    return 0

if __name__ == "__main__":
    main()



# Zrób testy czasowe dla różnych długości wiadomości i różnych block size'ach (no i oczywiście 2 trybach)