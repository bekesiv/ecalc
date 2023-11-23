#! /usr/bin/env python

import customtkinter as ctk


class Calculator(object):
    def __init__(self):
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")
        self.app = ctk.CTk()
        self.app.title("eCalc")
        self.app.geometry("800x400")
        self.app.resizable(False, False)
        # bInput = ctk.CTkEntry(master=app, width=800, font=('Calibry', 20), placeholder_text='Type Expression Here', state=ctk.DISABLED)
        self.bInput = ctk.CTkEntry(master=self.app, width=800, font=('Calibry', 20), placeholder_text='Type Expression Here', justify="right")
        self.bInput.bind('<KeyRelease>', self.evaluateExpression)
        self.bInput.pack(pady=20, padx=20)
        self.bInput.after(10, self.bInput.focus_set)
        self.bInput.focus_set()
        self.bResultDec = ctk.CTkTextbox(master=self.app, font=('Calibry', 20))
        # bInput.place(relx=0.1, rely=0.2, anchor=ctk.CENTER)
        self.bResultDec.pack(pady=30, padx=20)
        

    def start(self):        
        self.app.mainloop()


    def evaluateExpression(self, keypressed):
        self.bResultDec.delete('1.0', ctk.END)
        if keypressed.keysym=='Escape':
            exit(0)
        elif keypressed.keysym=='Return':
            self.bInput.delete(0, 'end')
        else:
            self.bResultDec.insert(ctk.END, self.bInput.get())
