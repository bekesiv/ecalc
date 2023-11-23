#! /usr/bin/env python

import customtkinter as ctk
import ast
from math import *
import re

class Calculator(object):
    def __init__(self):
        ctk.set_appearance_mode('Dark')
        ctk.set_default_color_theme('blue')
        self.app = ctk.CTk()
        self.app.title('eCalc')
        self.app.geometry('800x400')
        self.app.resizable(False, False)

        self.bInput = ctk.CTkEntry(master=self.app, width=800, font=('Calibry', 20), placeholder_text='Type Expression Here', justify='right')
        self.bInput.bind('<KeyRelease>', self.onChangeInput)
        self.bInput.pack(pady=20, padx=20)
        self.bInput.after(20, self.bInput.focus_set)
        self.bInput.focus_set()

        self.lResultDec = ctk.CTkLabel(master=self.app, text='Result', font=('Calibry', 16))
        self.lResultDec.pack(pady=10, padx=20)

        self.bResultDec = ctk.CTkEntry(master=self.app, width=400, font=('Calibry', 20), state=ctk.DISABLED)
        self.bResultDec.bind('<Button>', self.onClickResultDec)
        self.bResultDec.pack(pady=10, padx=20)

        self.lResultHex = ctk.CTkLabel(master=self.app, text='Hexadecimal', font=('Calibry', 16))
        self.lResultHex.pack(pady=10, padx=20)

        self.bResultHex = ctk.CTkEntry(master=self.app, width=400, font=('Calibry', 20), state=ctk.DISABLED)
        self.bResultHex.pack(pady=10, padx=20)

    def start(self):
        self.app.mainloop()

    def onChangeInput(self, keypressed):
        if keypressed.keysym=='Escape':
            exit(0)
        elif keypressed.keysym=='Return':
            self.bInput.delete(0, 'end')
        else:
            self.updateResults()

    def onClickResultDec(self, dummy):
        Calculator.clearDisabledEntry(self.bResultDec)        

    @classmethod
    def updateDisabledEntry(cls, entry, text):
        entry.configure(state=ctk.NORMAL)
        entry.delete(0, 'end')
        entry.insert(ctk.END, text)
        entry.configure(state=ctk.DISABLED)

    def updateResults(self):
            formula = self.bInput.get().replace('^', '**')
            try:
                result = eval(compile(ast.parse(formula, mode='eval'), filename='', mode='eval'))
            except:
                result = 'error'
            Calculator.updateDisabledEntry(self.bResultDec, result)
            try:
                Calculator.updateDisabledEntry(self.bResultHex, result if result == 'error' else hex(int(result)))
            except:
                Calculator.updateDisabledEntry(self.bResultHex, 'error')
            
