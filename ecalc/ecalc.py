#! /usr/bin/env python

import customtkinter as ctk
import ast
from math import *

class ResultFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.grid(row=1, column=0, columnspan=3, padx=8, pady=4, sticky="ew")
        self.grid_columnconfigure(1, weight=1)
        # Result Captions
        self.lResultDec = ResultFrame._addResultLabel(self, 'Decimal', 0, 0)
        self.lResultHex = ResultFrame._addResultLabel(self, 'Hexadecimal', 1, 0)
        # Result TextBoxes
        self.bResultDec = ResultFrame._addResultTextBox (self, self._onClickResultDec, 0, 1)
        self.bResultHex = ResultFrame._addResultTextBox (self, self._onClickResultHex, 1, 1)

    @classmethod
    def _addResultLabel(cls, master, text, row, col):
        widget = ctk.CTkLabel(master=master, text=text, font=('Calibry', 16), anchor=ctk.W)
        widget.grid(row=row, column=col, padx=8, pady=4, sticky="ew")
        return widget

    @classmethod
    def _addResultTextBox(cls, master, command, row, col):
        widget = ctk.CTkEntry(master=master, width=400, font=('Calibry', 20), justify='right', state=ctk.DISABLED)
        widget.bind('<Button>', command)
        widget.grid(row=row, column=col, padx=0, pady=4, sticky="ew")
        return widget

    @classmethod
    def _updateDisabledEntry(cls, widget, text):
        widget.configure(state=ctk.NORMAL)
        widget.delete(0, 'end')
        widget.insert(ctk.END, text)
        widget.configure(state=ctk.DISABLED)

    def _onClickResultDec(self, dummy):
        self._copyToClipboard(self.bResultDec)

    def _onClickResultHex(self, dummy):
        self._copyToClipboard(self.bResultHex)

    def _copyToClipboard(self, widget):
        self.master.clipboard_clear()
        self.master.clipboard_append(widget.get())
        self.master.update()
        origColor = ('#F9F9FA', '#343638')
        widget.configure(fg_color = 'darkblue')
        widget.after(200, lambda: widget.configure(fg_color = origColor))

    def getDec(self):
        return self.bResultDec.get()

    def getHex(self):
        return self.bResultHex.get()

    def writeResults(self, value):
        ResultFrame._updateDisabledEntry(self.bResultDec, value)
        try:
            hexValue = hex(int(value))
        except:
            hexValue = 'error'
        ResultFrame._updateDisabledEntry(self.bResultHex, hexValue)

class Calculator(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode('Dark')
        ctk.set_default_color_theme('blue')
        # Main Window
        self.title('eCalc')
        self.geometry('600x340')
        self.minsize(600, 300)
        self.grid_rowconfigure((0, 1, 2, 4), weight=0)
        self.grid_rowconfigure((3), weight=1)
        self.grid_columnconfigure(0, weight=2)
        self.grid_columnconfigure((1, 2), weight=1)
        self.bind('<Escape>', lambda e, w=self: w.destroy())
        # Input TextBox
        self.bInput = ctk.CTkEntry(master=self, width=800, font=('Calibry', 20), 
                                   placeholder_text='Type Expression Here', justify='right')
        self.bInput.bind('<KeyRelease>', self._onChangeInput)
        self.bInput.grid(row=0, column=0, columnspan=3, ipadx=8, ipady=4, padx=8, pady=4, sticky="ew")
        self.bInput.after(30, self.bInput.focus_set)
        self.bInput.focus_set()
        # Result widgets are organized into a frame
        self.frame = ResultFrame(self)
        # History Captions
        self.lExpressionHistory = Calculator._addHistoryLabel(self, 'Expression History', 2, 0)
        self.lHistoryDec = Calculator._addHistoryLabel(self, 'Decimal History', 2, 1)
        self.lHistoryHex = Calculator._addHistoryLabel(self, 'Hexadecimal History', 2, 2)
        # History textBoxes
        self.bExpressionHistory = Calculator._addHistoryTextBox(self, 3, 0)
        self.bHistoryDec = Calculator._addHistoryTextBox(self, 3, 1)
        self.bHistoryHex = Calculator._addHistoryTextBox(self, 3, 2)
        # Dummy Label for Spacer at bottom
        self.lSpacer = Calculator._addHistoryLabel(self, '', 4, 0, True)
        # TODO: Synced scroll of the three results window

    def start(self):
        self.mainloop()

    @classmethod
    def _addHistoryLabel(cls, master, text, row, col, spacer=False):
        widget = ctk.CTkLabel(master=master, text=text, height=8 if spacer else 20, 
                              font=('Calibry', 6 if spacer else 16), anchor=ctk.W)
        widget.grid(row=row, column=col, padx=16, pady=4, sticky="ew")
        return widget

    @classmethod
    def _addHistoryTextBox(cls, master, row, col):
        widget = ctk.CTkTextbox(master=master, font=('Calibry', 16), spacing1=2, spacing3=2)
        widget.grid(row=row, column=col, padx=8, pady=0, sticky="nsew")
        return widget

    def _getInputValue(self):
        return self.bInput.get()

    def _onChangeInput(self, keypressed):
        if keypressed.keysym == 'Return':
            self.bExpressionHistory.tag_config('justified', justify=ctk.RIGHT)
            self.bExpressionHistory.insert(0.0, self._getInputValue() + "\n", 'justified') 
            self.bHistoryDec.tag_config('justified', justify=ctk.RIGHT)
            self.bHistoryDec.insert(0.0, self.frame.getDec() + "\n", 'justified') 
            self.bHistoryHex.tag_config('justified', justify=ctk.RIGHT)
            self.bHistoryHex.insert(0.0, self.frame.getHex() + "\n", 'justified') 
            self.bInput.delete(0, 'end')
        else:
            self._updateResults()

    def _updateResults(self):
            formula = self._getInputValue().replace('^', '**')
            try:
                result = eval(compile(ast.parse(formula, mode='eval'), filename='', mode='eval'))
            except:
                result = 'error'
            self.frame.writeResults(result)

if __name__ == '__main__':
    Calculator().start()
