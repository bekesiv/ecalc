#! /usr/bin/env python

import customtkinter as ctk
import ast
from math import *
import os
import re

APP_VERSION = '1.2.1'
CONFIGURATION_FILENAME = f'{os.path.expanduser('~')}/ecalc.conf'
DEFAULT_POSITION = '500x164+300+600'
ORIGINAL_COLOR = ('#979DA2', '#565B5E')
DEGREES='Degrees'
RADIANS='Radians'
DECIMAL='Decimal'
HEXADECIMAL='Hexadecimal'
BINARY='Binary'


class Input(ctk.CTkComboBox):
    def __init__(self, master):
        super().__init__(master)
        self.values = []
        self.configure(values=self.values, command=self.onDropdown, fg_color='#222222',
                       font=('Calibry', 16), dropdown_font=('Calibry', 16), 
                       justify='right', hover=True)
        self.grid(row=0, column=1, padx=8, pady=6, sticky="ew")
        self.bind('<KeyPress>', self.onKeyPress)
        self.bind('<KeyRelease>', self.onKeyRelease)
        self.set('')
        self.clearFlag = False
        self.after(50, self.focus_set)

    def onDropdown(self, choice):
        self.master.onChangeInput()

    def onKeyPress(self, keypressed):
        if keypressed.keysym != 'Return' and self.clearFlag:
            self.set('')

    def onKeyRelease(self, keypressed):
        if keypressed.keysym == 'Return':
            self.master.onEnter()
            self.clearFlag = True
            self.master.flashWidgets()
        else:
            self.master.onChangeInput()

    def addHistory(self):
        self.values.insert(0, self.get())
        self.configure(values=self.values)

    def flash(self, duration=100):
        self.configure(border_color='lightgrey', button_color='lightgrey')
        self.after(duration, lambda: self.configure(border_color=ORIGINAL_COLOR, button_color=ORIGINAL_COLOR))


class Result(ctk.CTkComboBox):
    def __init__(self, master, base, row):
        super().__init__(master)
        self.values = []
        self.configure(values=self.values, command=self.onDropdown, #height=32, 
                       font=('Calibry', 16), dropdown_font=('Calibry', 16), justify='right',
                       hover=True)
        self.grid(row=row, column=1, padx=8, pady=6, sticky="ew")
        self.bind('<KeyRelease>', self.onKeyEvent)
        self.bind('<KeyPress>', self.onKeyEvent)
        self.base = base
        self.write('')
        # Label
        label = ctk.CTkLabel(master=master, text=base, font=('Calibry', 16), anchor=ctk.W)
        label.grid(row=row, column=0, padx=8, pady=4, sticky="ew")

    def onKeyEvent(self, keypressed):
        self.master.onChangeInput()

    def onDropdown(self, choice):
        self.master.onChangeInput(choice)

    def write(self, content):
        if self.base != DECIMAL and content:
            try:
                content = hex(int(content)) if self.base == HEXADECIMAL else bin(int(content))
            except:
                content = 'error'
        self.set(content)

    def addHistory(self):
        self.values.insert(0, self.get())
        self.configure(values=self.values)

    def flash(self, duration=100):
        self.configure(border_color='lightgrey', button_color='lightgrey')
        self.after(duration, lambda: self.configure(border_color=ORIGINAL_COLOR, button_color=ORIGINAL_COLOR))


class Calculator(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode('Dark')
        ctk.set_default_color_theme('blue')
        # Main Window
        self.title(f'eCalc - {APP_VERSION}')
        self.setGeometry()
        self.resizable(False, False)
        self.bind('<Escape>', lambda e, w=self: w.destroy())
        # self.grid_rowconfigure((0, 1, 2), weight=0)
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.after(201, lambda: self.iconbitmap('_internal/Wineass-Ios7-Redesign-Calculator.ico'))
        # Switch
        self.switchDRValue = ctk.StringVar(value=DEGREES)
        self.switchDR = ctk.CTkSwitch(master=self, text=DEGREES, command=self.onUpdateSwitch, font=('Calibry', 15),
                                    variable=self.switchDRValue, onvalue=RADIANS, offvalue=DEGREES)
        self.switchDR.grid(row=0, column=0, padx=(12, 4), pady=4)
        self.switchDR.deselect()
        # switch is destroyed when main windows is destroyed, this is when we save geometry data
        self.switchDR.bind("<Destroy>", self.saveWindowPosition)
        # Input
        self.input = Input(self)
        # Results
        self.resultDec = Result(self, DECIMAL, 1)
        self.resultHex = Result(self, HEXADECIMAL, 2)
        self.resultBin = Result(self, BINARY, 3)

    def start(self):
        self.mainloop()

    def saveWindowPosition(self, event):
        with open(CONFIGURATION_FILENAME, "w") as conf:
            conf.write(self.geometry())

    def setGeometry(self):
        try:
            with open(CONFIGURATION_FILENAME, "r") as conf:
                self.geometry(conf.readlines()[0])
        except:
                self.geometry(DEFAULT_POSITION)

    def onEnter(self):
        self.input.addHistory()
        self.resultDec.addHistory()
        self.resultHex.addHistory()
        self.resultBin.addHistory()

    def onUpdateSwitch(self):
        self.switchDR.configure(text=self.switchDRValue.get())
        self.onChangeInput()

    def onChangeInput(self, value=None):
        self.input.clearFlag = False
        if value:
             self.input.set(value)
        result = self.calculate(self.input.get())
        self.resultDec.write((result))
        self.resultHex.write((result))
        self.resultBin.write((result))
        self.input.focus_set()

    def flashWidgets(self):
        self.input.flash()
        self.resultDec.flash()
        self.resultHex.flash()
        self.resultBin.flash()

    def calculate(self, formula):
        retVal = formula.replace('^', '**').replace(',', '.')
        if formula:
            if self.switchDRValue.get() == DEGREES:
                pattern = re.compile(r'(sin|cos|tan)\(([^)]+)\)')
                replacement = r'\1(radians(\2))'
                retVal = pattern.sub(replacement, retVal)
            try:
                retVal = eval(compile(ast.parse(retVal, mode='eval'), filename='', mode='eval'))
            except:
                retVal = 'error'
        return retVal

if __name__ == '__main__':
    Calculator().start()
