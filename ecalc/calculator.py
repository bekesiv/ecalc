#! /usr/bin/env python

import customtkinter as ctk
import ast
from math import *

class Calculator(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode('Dark')
        ctk.set_default_color_theme('blue')
        # Main Window
        self.title('eCalc')
        self.geometry('800x400')
        self.minsize(600, 300)
        self.grid_rowconfigure((0, 1, 2, 4), weight=0)
        self.grid_rowconfigure((3), weight=1)
        self.grid_columnconfigure(0, weight=2)
        self.grid_columnconfigure((1, 2), weight=1)
        self.bind('<Escape>', lambda e, w=self: w.destroy())
        # Input TextBox
        self.bInput = ctk.CTkEntry(master=self, width=800, font=('Calibry', 20), placeholder_text='Type Expression Here', justify='right')
        self.bInput.bind('<KeyRelease>', self.onChangeInput)
        self.bInput.grid(row=0, column=0, columnspan=3, ipadx=8, ipady=4, padx=8, pady=4, sticky="ew")
        self.bInput.after(30, self.bInput.focus_set)
        self.bInput.focus_set()
        # Below controls are organized into a frame
        self.frame = ctk.CTkFrame(master=self)
        self.frame.grid(row=1, column=0, columnspan=3, padx=8, pady=4, sticky="ew")
        self.frame.grid_columnconfigure(1, weight=1)
        # Decimal Result Caption
        self.lResultDec = ctk.CTkLabel(master=self.frame, text='Result', font=('Calibry', 16), anchor=ctk.W)
        self.lResultDec.grid(row=0, column=0, padx=8, pady=4, sticky="ew")
        # Decimal TextBox
        self.bResultDec = ctk.CTkEntry(master=self.frame, width=400, font=('Calibry', 20), justify='right', state=ctk.DISABLED)
        self.bResultDec.bind('<Button>', self.onClickResultDec)
        self.bResultDec.grid(row=0, column=1, padx=0, pady=4, sticky="ew")
        # Hexadecimal Result Caption
        self.lResultHex = ctk.CTkLabel(master=self.frame, text='Hexadecimal', font=('Calibry', 16), anchor=ctk.W)
        self.lResultHex.grid(row=1, column=0, padx=8, pady=4, sticky="ew")
        # Hexadecimal TextBox
        self.bResultHex = ctk.CTkEntry(master=self.frame, width=400, font=('Calibry', 20), justify='right', state=ctk.DISABLED)
        self.bResultHex.bind('<Button>', self.onClickResultHex)
        self.bResultHex.grid(row=1, column=1, padx=0, pady=4, sticky="ew")
        # Expression History Caption
        self.lExpressionHistory = ctk.CTkLabel(master=self, text='Expression History', font=('Calibry', 16), anchor=ctk.W)
        self.lExpressionHistory.grid(row=2, column=0, padx=16, pady=4, sticky="ew")
        # Decimal History Caption
        self.lHistoryDec = ctk.CTkLabel(master=self, text='Decimal History', font=('Calibry', 16), anchor=ctk.W)
        self.lHistoryDec.grid(row=2, column=1, padx=16, pady=4, sticky="ew")
        # Hexadecimal History Caption
        self.lHistoryHex = ctk.CTkLabel(master=self, text='Hexadecimal History', font=('Calibry', 16), anchor=ctk.W)
        self.lHistoryHex.grid(row=2, column=2, padx=16, pady=4, sticky="ew")
        # Expression History
        self.bExpressionHistory = ctk.CTkTextbox(master=self, font=('Calibry', 16), spacing1=2, spacing3=2)
        self.bExpressionHistory.grid(row=3, column=0, padx=8, pady=0, sticky="nsew")
        # Decimal History
        self.bHistoryDec = ctk.CTkTextbox(master=self, font=('Calibry', 16), spacing1=2, spacing3=2)
        self.bHistoryDec.grid(row=3, column=1, padx=8, pady=0, sticky="nsew")
        # Hexadecimal History
        self.bHistoryHex = ctk.CTkTextbox(master=self, font=('Calibry', 16), spacing1=2, spacing3=2)
        self.bHistoryHex.grid(row=3, column=2, padx=8, pady=0, sticky="nsew")
        # Dummy Label for Spacer at bottom
        self.lSpacer = ctk.CTkLabel(master=self, text='', height=10, font=('Calibry', 6), anchor=ctk.W)
        self.lSpacer.grid(row=4, column=0, columnspan=2, padx=8, pady=4, sticky="nsew")
        # TODO: Synced scroll of the three results window

    def start(self):
        self.mainloop()

    def onChangeInput(self, keypressed):
        if keypressed.keysym == 'Return':
            self.bExpressionHistory.tag_config('justified', justify=ctk.RIGHT)
            self.bExpressionHistory.insert(0.0, self.bInput.get() + "\n", 'justified') 
            self.bHistoryDec.tag_config('justified', justify=ctk.RIGHT)
            self.bHistoryDec.insert(0.0, self.bResultDec.get() + "\n", 'justified') 
            self.bHistoryHex.tag_config('justified', justify=ctk.RIGHT)
            self.bHistoryHex.insert(0.0, self.bResultHex.get() + "\n", 'justified') 
            self.bInput.delete(0, 'end')
        else:
            self.updateResults()

    def onClickResultDec(self, dummy):
        self.copyToClipboard(self.bResultDec)

    def onClickResultHex(self, dummy):
        self.copyToClipboard(self.bResultHex)

    def copyToClipboard(self, widget):
        self.clipboard_clear()
        self.clipboard_append(widget.get())
        self.update()
        origColor = ('#F9F9FA', '#343638')
        widget.configure(fg_color = 'darkblue')
        widget.after(200, lambda: widget.configure(fg_color = origColor))

    @classmethod
    def updateDisabledEntry(cls, widget, text):
        widget.configure(state=ctk.NORMAL)
        widget.delete(0, 'end')
        widget.insert(ctk.END, text)
        widget.configure(state=ctk.DISABLED)

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
            
