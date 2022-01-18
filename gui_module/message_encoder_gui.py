from encryption_module.encryption_module import EncryptionModule

import tkinter as tk
from tkinter import ttk

class MessageEncoderGUI:
    def __init__(self):
        self.__em = EncryptionModule(mode = "ECB", generate_new_keys = False )

        # GUI parameters
        self.__padx = 8
        self.__pady = 8
        self.__button_color = "#538f39"
        self.__button_hover_color = "#86bd6d"
        self.__bg_color = "#7fb368"
        self.__label_font = "Helvetica 10 bold"
        self.__title_font = "Helvetica 14 bold"
        self.__title_bg_color = "#6d9c59"
        #--------------------------------------------        

        self.__window = tk.Tk()
        self.__window.title("RSA Message Encoder")

        self.__frm_main = tk.Frame(
            bg = self.__bg_color
        )
        self.__frm_main.pack()

        self.__lbl_title = tk.Label(
            master = self.__frm_main,
            relief = tk.GROOVE,
            text = "RSA Message Encoder",
            width = 50,
            height = 3,
            bg = self.__title_bg_color,
            fg = "black",
            font = self.__title_font
        )
        self.__lbl_title.grid(column = 1, row = 0, padx = self.__padx, pady = self.__pady)

        #--------------------MODE--------------------        
        self.__lbl_mode = tk.Label(
            master = self.__frm_main,
            relief = tk.FLAT,
            text = "Mode of operation",
            width = 15,
            height = 1,
            bg = self.__bg_color,
            fg = "black",
            font = self.__label_font      
        )
        self.__lbl_mode.grid(column = 0, row = 1, padx = self.__padx, pady = self.__pady)
  
        self.__cbx_mode = tk.ttk.Combobox(
            master = self.__frm_main,
            values = ["ECB", "CBC"],
            height = 2,
            width = 7,
            state = "readonly"
        )
        self.__cbx_mode.grid(sticky = "w", column = 1, row = 1, padx = self.__padx, pady = self.__pady)
        if self.__em.get_mode() == "ECB":
            self.__cbx_mode.current(0)
        else:
            self.__cbx_mode.current(1)
        #--------------------------------------------        

        #----------------BLOCK-SIZE------------------ 
        self.__lbl_block_size = tk.Label(
            master = self.__frm_main,
            relief = tk.FLAT,
            text = "Block size",
            width = 15,
            height = 1,
            bg = self.__bg_color,
            fg = "black",
            font = self.__label_font        
        )
        self.__lbl_block_size.grid(column = 0, row = 2, padx = self.__padx, pady = self.__pady)
        
        self.__txt_block_size = tk.Entry(
            master = self.__frm_main,
            relief = tk.GROOVE,
            width = 8,
            bg = "white",
            fg = "black"
        )
        self.__txt_block_size.grid(sticky = "w", column = 1, row = 2, padx = self.__padx, pady = self.__pady)
        self.__txt_block_size.insert(0, str(self.__em.get_block_size()))
        #--------------------------------------------
        
        #---------------GENERATE-KEYS----------------  
        self.__btn_generate_keys = tk.Button(
            master = self.__frm_main,
            relief = tk.GROOVE,
            text = "Generate keys",
            width = 10,
            height = 1,
            bg = self.__button_color,
            fg = "black",
            activebackground = self.__button_hover_color
        )
        self.__btn_generate_keys.grid(sticky = "w", column = 1, row = 3, padx = self.__padx, pady = self.__pady)
        self.__btn_generate_keys.bind("<ButtonRelease-1>", self.__btn_generate_keys_on_release) 
        #--------------------------------------------
               
        #------------------MESSAGE-------------------        
        self.__lbl_message = tk.Label(
            master = self.__frm_main,
            relief = tk.FLAT,
            text = "Message",
            width = 15,
            height = 2,
            bg = self.__bg_color,
            fg = "black",
            font = self.__label_font      
        )
        self.__lbl_message.grid(column = 0, row = 4, padx = self.__padx, pady = self.__pady)

        self.__txt_message = tk.Text(
            master = self.__frm_main,
            relief = tk.GROOVE,
            height = 5,
            bg = "white",
            fg = "black"
        )
        self.__txt_message.grid(column = 1, row = 4, padx = self.__padx, pady = self.__pady)

        self.__btn_encrypt = tk.Button(
            master = self.__frm_main,
            relief = tk.GROOVE,
            text = "Encrypt",
            width = 10,
            height = 1,
            bg = self.__button_color,
            fg = "black",
            activebackground = self.__button_hover_color
        )
        self.__btn_encrypt.grid(column = 2, row = 4, padx = self.__padx, pady = self.__pady)
        self.__btn_encrypt.bind("<ButtonRelease-1>", self.__btn_encrypt_on_release)   
        #--------------------------------------------        

        #-------------------CIPHER-------------------        
        self.__lbl_cipher = tk.Label(
            master = self.__frm_main,
            relief = tk.FLAT,
            text = "Ciphertext",
            width = 15,
            height = 2,
            bg = self.__bg_color,
            fg = "black",
            font = self.__label_font      
        )
        self.__lbl_cipher.grid(column = 0, row = 5, padx = self.__padx, pady = self.__pady)

        self.__txt_cipher = tk.Text(
            master = self.__frm_main,
            relief = tk.GROOVE,
            height = 5,
            bg = "white",
            fg = "black",
            state = "disabled"
        )
        self.__txt_cipher.grid(column = 1, row = 5, padx = self.__padx, pady = self.__pady)

        self.__btn_decrypt = tk.Button(
            master = self.__frm_main,
            relief = tk.GROOVE,
            text = "Decrypt",
            width = 10,
            height = 1,
            bg = self.__button_color,
            fg = "black",
            activebackground = self.__button_hover_color
        )
        self.__btn_decrypt.grid(column = 2, row = 5, padx = self.__padx, pady = self.__pady)
        self.__btn_decrypt.bind("<ButtonRelease-1>", self.__btn_decrypt_on_release)    
        #--------------------------------------------        

        #-----------------DECRYPTED------------------        
        self.__lbl_decrypted = tk.Label(
            master = self.__frm_main,
            relief = tk.FLAT,
            text = "Decrypted ciphertext",
            width = -1,
            height = 2,
            bg = self.__bg_color,
            fg = "black",
            font = self.__label_font      
        )
        self.__lbl_decrypted.grid(column = 0, row = 6, padx = self.__padx, pady = self.__pady)

        self.__txt_decrypted = tk.Text(
            master = self.__frm_main,
            relief = tk.GROOVE,
            height = 5,
            bg = "white",
            fg = "black",
            state = "disabled"
        )
        self.__txt_decrypted.grid(column = 1, row = 6, padx = self.__padx, pady = self.__pady)
        #--------------------------------------------        

        self.__btn_exit = tk.Button(
            master = self.__frm_main,
            relief = tk.GROOVE,
            text = "Exit",
            width = 10,
            height = 1,
            bg = self.__button_color,
            fg = "black",
            activebackground = self.__button_hover_color
        )
        self.__btn_exit.grid(column = 1, row = 7, padx = self.__padx, pady = self.__pady)   
        self.__btn_exit.bind("<ButtonRelease-1>", self.__exit_button_click)

    def __btn_generate_keys_on_release(self, event):
        self.__em.generate_pair_of_keys()

    def __btn_encrypt_on_release(self, event):
        message = self.__txt_message.get("1.0", tk.END)
        message.strip()
        message = message[:-1]
        print("Encrypted message:", message)
        ciphertext = self.__em.encrypt(message)
        self.__txt_cipher.configure(state = "normal")
        self.__txt_cipher.delete("1.0", tk.END)
        self.__txt_cipher.insert("1.0", ciphertext)
        self.__txt_cipher.configure(state = "disabled")

    def __btn_decrypt_on_release(self, event):
        ciphertext = self.__txt_cipher.get("1.0", tk.END)
        ciphertext.strip()
        decrypted_message = self.__em.decrypt(ciphertext)
        print("Decrypted message:", decrypted_message)
        self.__txt_decrypted.config(state = "normal")
        self.__txt_decrypted.delete("1.0", tk.END)
        self.__txt_decrypted.insert("1.0", decrypted_message)
        self.__txt_decrypted.config(state = "disabled")

    def __exit_button_click(self, event):
        self.__window.destroy()

    def run(self):
        self.__window.mainloop()

