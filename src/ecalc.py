#!/usr/bin/env python
import os
import re
import ast
from math import radians, sin, cos, tan
import customtkinter as ctk # type: ignore
from typing import Any, Optional, Union
if os.name == 'posix':
    from PIL import Image, ImageTk

APP_TITLE = 'eCalc'
APP_VERSION = '1.2.6'
CONFIGURATION_FILENAME = f'{os.path.expanduser("~")}/ecalc.conf'
DEFAULT_POSITION = '500x164+300+600'
ORIGINAL_COLOR = ('#979DA2', '#565B5E')
DEGREES = 'Degrees'
RADIANS = 'Radians'
DECIMAL = 'Decimal'
HEXADECIMAL = 'Hexadecimal'
BINARY = 'Binary'

class Input(ctk.CTkComboBox):
    def __init__(self, master: Any) -> None:
        super().__init__(master)
        self.values: list[str] = []
        self.configure(values=self.values, command=self.onDropdown, fg_color='#222222',
                       font=('Calibry', 16), dropdown_font=('Calibry', 16),
                       justify='right', hover=True)
        self.grid(row=0, column=1, padx=8, pady=6, sticky="ew")
        self.bind('<KeyPress>', self.onKeyPress)
        self.bind('<KeyRelease>', self.onKeyRelease)
        self.set('')
        self.clear_flag = False
        self.after(50, self.focus_set)

    def onDropdown(self, choice: str) -> None:
        self.master.onChangeInput()

    def onKeyPress(self, keypressed: Any) -> None:
        if keypressed.keysym not in ('Return', 'KP_Enter') and self.clear_flag:
            self.set('')

    def onKeyRelease(self, keypressed: Any) -> None:
        if keypressed.keysym in ('Return', 'KP_Enter'):
            self.master.onEnter()
            self.clear_flag = True
            self.master.flashWidgets()
        else:
            self.master.onChangeInput()

    def addHistory(self) -> None:
        self.values.insert(0, self.get())
        self.configure(values=self.values)

    def flash(self, duration: int = 100) -> None:
        self.configure(border_color='lightgrey', button_color='lightgrey')
        self.after(duration, lambda: self.configure(border_color=ORIGINAL_COLOR, button_color=ORIGINAL_COLOR))


class Result(ctk.CTkComboBox):
    def __init__(self, master: Any, base: str, row: int) -> None:
        super().__init__(master)
        self.values: list[str] = []
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

    def onKeyEvent(self, keypressed: Any) -> None:
        self.master.onChangeInput()

    def onDropdown(self, choice: str) -> None:
        self.master.onChangeInput(choice)

    def write(self, content: str) -> None:
        if self.base != DECIMAL and content:
            try:
                content = hex(int(content)) if self.base == HEXADECIMAL else bin(int(content))
            except ValueError:
                content = 'error'
        self.set(content)

    def addHistory(self) -> None:
        self.values.insert(0, self.get())
        self.configure(values=self.values)

    def flash(self, duration: int = 100) -> None:
        self.configure(border_color='lightgrey', button_color='lightgrey')
        self.after(duration, lambda: self.configure(border_color=ORIGINAL_COLOR, button_color=ORIGINAL_COLOR))

    def getValue(self, index: int) -> str:
        return self.values[index - 1]

class Calculator(ctk.CTk):
    def __init__(self) -> None:
        super().__init__(className=APP_TITLE)
        ctk.set_appearance_mode('Dark')
        ctk.set_default_color_theme('blue')
        # Main Window
        self.title(f'{APP_TITLE} - {APP_VERSION}')
        self.setGeometry()
        self.resizable(False, False)
        self.bind('<Escape>', lambda e, w=self: w.destroy())
        # self.grid_rowconfigure((0, 1, 2), weight=0)
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)

        self.setAppIcon()

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

    def start(self) -> None:
        self.mainloop()

    def saveWindowPosition(self, event: Any) -> None:
        with open(CONFIGURATION_FILENAME, "w", encoding="utf-8") as conf:
            conf.write(self.geometry())

    def setAppIcon(self) -> None:
        icon_path = os.path.join(os.path.dirname(__file__), '../icon', 'Wineass-Ios7-Redesign-Calculator')
        if os.name == 'nt':
            self.after(201, lambda: self.iconbitmap(icon_path + '.ico'))
        elif os.name == 'posix':
            im = Image.open(icon_path + '.png')
            photo = ImageTk.PhotoImage(im)
            self.iconphoto(True, photo)

    def setGeometry(self) -> None:
        try:
            with open(CONFIGURATION_FILENAME, "r", encoding="utf-8") as conf:
                self.geometry(conf.readlines()[0])
        except FileNotFoundError:
            self.geometry(DEFAULT_POSITION)

    def onEnter(self) -> None:
        self.input.addHistory()
        self.resultDec.addHistory()
        self.resultHex.addHistory()
        self.resultBin.addHistory()

    def onUpdateSwitch(self) -> None:
        self.switchDR.configure(text=self.switchDRValue.get())
        self.onChangeInput()

    def onChangeInput(self, value: Optional[str] = None) -> None:
        self.input.clear_flag = False
        if value:
            self.input.set(value)
        result = self.calculate(self.input.get())
        self.resultDec.write(result)
        self.resultHex.write(result)
        self.resultBin.write(result)
        self.input.focus_set()

    def flashWidgets(self) -> None:
        self.input.flash()
        self.resultDec.flash()
        self.resultHex.flash()
        self.resultBin.flash()

    def calculate(self, formula: str) -> Union[str, float]:
        retVal = formula.replace('^', '**').replace(',', '.')
        if formula:
            if self.switchDRValue.get() == DEGREES:
                pattern = re.compile(r'(sin|cos|tan)\(([^)]+)\)')
                replacement = r'\1(radians(\2))'
                retVal = pattern.sub(replacement, retVal)
            try:
                pattern = re.compile(r'\$(\d+)')
                retVal = pattern.sub(lambda match: self.resultDec.getValue(int(match.group(1))), retVal)
                retVal = eval(compile(ast.parse(retVal, mode='eval'), filename='', mode='eval'))
            except Exception:
                retVal = 'error'
        return retVal

if __name__ == '__main__':
    Calculator().start()
