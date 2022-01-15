from encryption_module.encryption_module import EncryptionModule

import tkinter as tk
from tkinter import ttk

class MessageEncoderGUI:
    def __init__(self):
        self.__em = EncryptionModule()

        self.__window = tk.Tk()

        self.__frm_main = tk.Frame(
            bg = "green"
        )
        self.__frm_main.pack()

        self.__lbl_title = tk.Label(
            master = self.__frm_main,
            relief = tk.GROOVE,
            text = "RSA Ecryption Program",
            width = 30,
            height = 5,
            bg = "orange",
            fg = "black"
        )
        self.__lbl_title.pack()

        self.__txt_test = tk.Text(
            master = self.__frm_main,
            relief = tk.GROOVE,
            bg = "orange",
            fg = "black"
        )
        self.__txt_test.pack()

        self.__btn_test = tk.Button(
            master = self.__frm_main,
            relief = tk.GROOVE,
            text = "Test",
            width = 15,
            height = 3,
            bg = "orange",
            fg = "black"
        )
        self.__btn_test.bind("<Button-1>", self.button_click)
        self.__btn_test.pack()    

    def button_click(self, event):
        self.__em.generate_pair_of_keys()
        # text = self.__txt_test.get("1.0", tk.END)
        # print(text)

    def run(self):
        self.__window.mainloop()
        
        # frame = ttk.Frame(window, height = 800, width = 600, padding = 10)
        # frame.grid()

        # tk.Label(frame, text = "RSA Encryption Program").grid(column = 0, row = 0)
        # tk.Button(frame, text = "Quit", command = window.destroy).grid(column = 0, row = 2)
        # tk.Entry(frame, width = 100).grid(column = 0, row = 1)
