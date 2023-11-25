#! /usr/bin/env python

import customtkinter as ctk
import ast
from math import *

# TODO: Notification Toast about copying content to clipboard

FONT_SIZE_RESULT = 20
FONT_SIZE_HISTORY = 16
FONT_SIZE_LABELS = 14

class ResultFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.grid(row=1, column=0, padx=8, pady=4, sticky="ew")
        self.grid_columnconfigure(1, weight=1)
        # Result Captions
        self.labelDec = ResultFrame._addLabel(self, 'Decimal', 0, 0)
        self.labelHex = ResultFrame._addLabel(self, 'Hexadecimal', 1, 0)
        # Result TextBoxes
        self.textboxDex = ResultFrame.addTextBox (self, self._onClickDec, 0, 1)
        self.textboxHex = ResultFrame.addTextBox (self, self._onClickHex, 1, 1)

    @classmethod
    def _addLabel(cls, master, text, row, col):
        widget = ctk.CTkLabel(master=master, text=text, font=('Calibry', FONT_SIZE_LABELS+2), anchor=ctk.W)
        widget.grid(row=row, column=col, padx=8, pady=4, sticky="ew")
        return widget

    @classmethod
    def addTextBox(cls, master, command, row, col):
        widget = ctk.CTkEntry(master=master, width=400, font=('Calibry', FONT_SIZE_RESULT), 
                              justify='right', state=ctk.DISABLED)
        widget.bind('<Button>', command)
        widget.grid(row=row, column=col, padx=0, pady=4, sticky="ew")
        return widget

    @classmethod
    def _updateDisabledEntry(cls, widget, text):
        widget.configure(state=ctk.NORMAL)
        widget.delete(0, 'end')
        widget.insert(ctk.END, text)
        widget.configure(state=ctk.DISABLED)

    def _copyToClipboard(self, widget):
        self.master.clipboard_clear()
        self.master.clipboard_append(widget.get())
        self.master.update()
        origColor = ('#F9F9FA', '#343638')
        widget.configure(fg_color = 'darkblue')
        widget.after(200, lambda: widget.configure(fg_color = origColor))

    def _onClickDec(self, dummy):
        self._copyToClipboard(self.textboxDex)

    def _onClickHex(self, dummy):
        self._copyToClipboard(self.textboxHex)

    def getDec(self):
        return self.textboxDex.get()

    def getHex(self):
        return self.textboxHex.get()

    def updateResults(self, formula):
        try:
            result = eval(compile(ast.parse(formula, mode='eval'), filename='', mode='eval'))
        except:
            result = 'error'
        self.writeResults(result)

    def writeResults(self, value):
        ResultFrame._updateDisabledEntry(self.textboxDex, value)
        try:
            hexValue = hex(int(value))
        except:
            hexValue = 'error'
        ResultFrame._updateDisabledEntry(self.textboxHex, hexValue)


class HistoryFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.grid(row=2, column=0, padx=8, pady=(4,12), sticky="nsew")
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=2)
        self.grid_columnconfigure((1, 2), weight=1)
        self.grid_columnconfigure(3, weight=0)
        # History Captions
        self.labelExpression = HistoryFrame._addLabel(self, 'Expression History', 0, 0)
        self.labelDec = HistoryFrame._addLabel(self, 'Decimal History', 0, 1)
        self.labelHex = HistoryFrame._addLabel(self, 'Hexadecimal History', 0, 2)
        # Scrollbar
        self.scrollHistory = ctk.CTkScrollbar(master=self, command=self._onScrollBar)
        self.scrollHistory.grid(row=1, column=3, padx=(0,4), pady=0, sticky="ns")
        # History textBoxes
        self.textboxExpression = HistoryFrame._addTextBox(self, self._onResultKeyPressed, 1, 0)
        self.textboxDec = HistoryFrame._addTextBox(self, self._onDecKeyPressed, 1, 1)
        self.textboxHex = HistoryFrame._addTextBox(self, self._onHexKeyPressed, 1, 2)
        # Due to the cross-independence, we can set this only aftetr all three textboxes created
        self.textboxExpression.configure(yscrollcommand=self._onTextScroll)
        self.textboxDec.configure(yscrollcommand=self._onTextScroll)
        self.textboxHex.configure(yscrollcommand=self._onTextScroll)

    @classmethod
    def _addLabel(cls, master, text, row, col, spacer=False):
        widget = ctk.CTkLabel(master=master, text=text, height=6 if spacer else 20, 
                              font=('Calibry', 4 if spacer else FONT_SIZE_LABELS), anchor=ctk.W)
        widget.grid(row=row, column=col, padx=8, pady=(4,2), sticky="ew")
        return widget

    @classmethod
    def _addTextBox(cls, master, command, row, col):
        widget = ctk.CTkTextbox(master=master, font=('Calibry', FONT_SIZE_HISTORY), 
                                spacing1=2, spacing3=2, activate_scrollbars=False)
        widget.grid(row=row, column=col, padx=(8, 4), pady=(0,8), sticky="nsew")
        widget.bind('<KeyPress>', command)
        widget.bind('<KeyRelease>', command)
        return widget

    def _onScrollBar(self, *args):
        '''Scrolls both text widgets when the scrollbar is moved'''
        self.textboxExpression.yview(*args)
        self.textboxDec.yview(*args)
        self.textboxHex.yview(*args)

    def _onTextScroll(self, *args):
        '''Moves the scrollbar and scrolls text widgets when the mousewheel is moved on a text widget'''
        self.scrollHistory.set(*args)
        self._onScrollBar('moveto', args[0])

    # TODO: preserve the content of the historybox, and save copy the selection to clipboard...
    # Can be maybe by disabling it when line selected, and then enabling when focus lost...
    def _onResultKeyPressed(self, keypressed):
        if keypressed.keysym == 'Return':
            pass

    def _onDecKeyPressed(self, keypressed):
        if keypressed.keysym == 'Return':
            pass

    def _onHexKeyPressed(self, keypressed):
        if keypressed.keysym == 'Return':
            pass

    @classmethod
    def _addToHistory(cls, widget, text ):
        widget.tag_config('justified', justify=ctk.RIGHT)
        widget.insert(0.0, text + "\n", 'justified')

    def addToAllHistories(self, result, decval, hexval):
        HistoryFrame._addToHistory(self.textboxExpression, result)
        HistoryFrame._addToHistory(self.textboxDec, decval)
        HistoryFrame._addToHistory(self.textboxHex, hexval)
        self._onScrollBar('moveto', 0.0)


class Calculator(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode('Dark')
        ctk.set_default_color_theme('blue')
        # Main Window
        self.title('eCalc')
        self.geometry('600x340')
        self.minsize(600, 300)
        self.grid_rowconfigure((0, 1), weight=0)
        self.grid_rowconfigure((2), weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.bind('<Escape>', lambda e, w=self: w.destroy())
        self.after(201, lambda :self.iconbitmap('resources/Wineass-Ios7-Redesign-Calculator.ico'))
        # Input TextBox
        self.bInput = ctk.CTkEntry(master=self, width=800, font=('Calibry', FONT_SIZE_RESULT), 
                                   placeholder_text='Type Expression Here', justify='right')
        self.bInput.bind('<KeyRelease>', self._onChangeInput)
        self.bInput.grid(row=0, column=0, ipadx=8, ipady=4, padx=8, pady=(8, 4), sticky="ew")
        self.bInput.after(50, self.bInput.focus_set)
        # Result and History are organized into frames
        self.frameResult = ResultFrame(self)
        self.frameHistory = HistoryFrame(self)

    def start(self):
        self.mainloop()

    def getInputValue(self):
        return self.bInput.get()

    def clearInput(self):
        self.bInput.delete(0, 'end')

    def _onChangeInput(self, keypressed):
        if keypressed.keysym == 'Return':
            self.frameHistory.addToAllHistories(self.getInputValue(), 
                                                self.frameResult.getDec(), 
                                                self.frameResult.getHex())
            self.clearInput()
        else:
            self.frameResult.updateResults(self.getInputValue().replace('^', '**'))

if __name__ == '__main__':
    Calculator().start()
