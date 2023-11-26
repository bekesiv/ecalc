#! /usr/bin/env python

import customtkinter as ctk
import ast
from math import *
import os
import re

CONFIGURATION_FILENAME = f'{os.path.expanduser('~')}/ecalc.conf'
DEFAULT_POSITION = '600x340+300+600'
FONT_SIZE_RESULT = 20
FONT_SIZE_HISTORY = 16
FONT_SIZE_LABELS = 14
DEGREES='Degrees'
RADIANS='Radians'

class ResultFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.grid(row=1, column=0, columnspan=2, padx=8, pady=4, sticky="ew")
        self.grid_columnconfigure(1, weight=1)
        # Result Captions
        self.labelDec = ResultFrame._addLabel(self, 'Decimal', 0, 0)
        self.labelHex = ResultFrame._addLabel(self, 'Hexadecimal', 1, 0)
        # Result TextBoxes
        self.textboxDex = ResultFrame.addTextBox (self, 0, 1)
        self.textboxHex = ResultFrame.addTextBox (self, 1, 1)

    @classmethod
    def _addLabel(cls, parent, text, row, col):
        widget = ctk.CTkLabel(master=parent, text=text, font=('Calibry', FONT_SIZE_LABELS+2), anchor=ctk.W)
        widget.grid(row=row, column=col, padx=8, pady=4, sticky="ew")
        return widget

    @classmethod
    def addTextBox(cls, parent, row, col):
        widget = ctk.CTkEntry(master=parent, width=400, font=('Calibry', FONT_SIZE_RESULT), 
                              justify='right', state=ctk.DISABLED)
        widget.bind('<Button>', lambda button: parent._copyToClipboard(widget, button))
        widget.grid(row=row, column=col, padx=(12, 4), pady=4, sticky="ew")
        return widget

    @classmethod
    def _updateDisabledEntry(cls, widget, text):
        widget.configure(state=ctk.NORMAL)
        widget.delete(0, 'end')
        widget.insert(ctk.END, text)
        widget.configure(state=ctk.DISABLED)

    def _copyToClipboard(self, widget, button):
        content = widget.get()
        if button.num == 1 and content:
            self.master.copyToClipboard(content)
            origColor = ('#F9F9FA', '#343638')
            widget.configure(fg_color = 'darkblue')
            widget.after(200, lambda: widget.configure(fg_color = origColor))

    def getDec(self):
        return self.textboxDex.get()

    def getHex(self):
        return self.textboxHex.get()

    def writeResults(self, decValue, hexValue):
        ResultFrame._updateDisabledEntry(self.textboxDex, decValue)
        ResultFrame._updateDisabledEntry(self.textboxHex, hexValue)


class HistoryFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.grid(row=2, column=0, columnspan=2, padx=8, pady=(4,12), sticky="nsew")
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
        self.textboxExpression = HistoryFrame._addTextBox(self, 1, 0)
        self.textboxDec = HistoryFrame._addTextBox(self, 1, 1)
        self.textboxHex = HistoryFrame._addTextBox(self, 1, 2)
        # Due to the cross-independence, we can set this only aftetr all three textboxes created
        self.textboxExpression.configure(yscrollcommand=self._onTextScroll)
        self.textboxDec.configure(yscrollcommand=self._onTextScroll)
        self.textboxHex.configure(yscrollcommand=self._onTextScroll)

    @classmethod
    def _addLabel(cls, parent, text, row, col, spacer=False):
        widget = ctk.CTkLabel(master=parent, text=text, height=6 if spacer else 20, 
                              font=('Calibry', 4 if spacer else FONT_SIZE_LABELS), anchor=ctk.W)
        widget.grid(row=row, column=col, padx=12, pady=(4,2), sticky="ew")
        return widget

    @classmethod
    def _addTextBox(cls, parent, row, col):
        widget = ctk.CTkTextbox(master=parent, font=('Calibry', FONT_SIZE_HISTORY), 
                                spacing1=2, spacing3=2, activate_scrollbars=False)
        widget.grid(row=row, column=col, padx=(8, 4), pady=(0,8), sticky="nsew")
        widget.bind('<KeyPress>', lambda event: parent._onKeyPress(widget, event))
        widget.bind('<KeyRelease>', lambda event: parent._onKeyRelease(widget))
        return widget

    @classmethod
    def _addToHistory(cls, widget, text ):
        widget.tag_config('justified', justify=ctk.RIGHT)
        widget.insert(0.0, text + "\n", 'justified')

    def _onScrollBar(self, *args):
        '''Scrolls both text widgets when the scrollbar is moved'''
        self.textboxExpression.yview(*args)
        self.textboxDec.yview(*args)
        self.textboxHex.yview(*args)

    def _onTextScroll(self, *args):
        '''Moves the scrollbar and scrolls text widgets when the mousewheel is moved on a text widget'''
        self.scrollHistory.set(*args)
        self._onScrollBar('moveto', args[0])

    def _onKeyPress(self, widget, event):
        if event.keysym == 'Return':
            try:
                self.master.copyToClipboard(widget.get(ctk.SEL_FIRST, ctk.SEL_LAST))
            except:
                pass
        widget.configure(state=ctk.DISABLED)

    def _onKeyRelease(self, widget):
        # This make sure we never enable widget before disabling it...
        widget.after(50, lambda: widget.configure(state=ctk.NORMAL))

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
        self.setGeometry()
        self.minsize(600, 300)
        self.grid_rowconfigure((0, 1), weight=0)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.after(201, lambda: self.iconbitmap('_internal/Wineass-Ios7-Redesign-Calculator.ico'))
        # Switch
        self.switchDRValue = ctk.StringVar(value=DEGREES)
        self.switchDR = ctk.CTkSwitch(master=self, text=DEGREES, command=self._onUpdateSwitch, 
                                    variable=self.switchDRValue, onvalue=RADIANS, offvalue=DEGREES)
        self.switchDR.grid(padx=(12, 4), pady=4)
        self.switchDR.deselect()
        # Input TextBox
        self.bInput = ctk.CTkEntry(master=self, font=('Calibry', FONT_SIZE_RESULT), justify='right', 
                                   placeholder_text='Type Expression Here')
        self.bInput.bind('<KeyRelease>', self._onKey)
        # bInput is destroyed when main windows is destroyed, this is when we save geometry data
        self.bInput.bind("<Destroy>", self._saveWindowPosition)
        self.bInput.grid(row=0, column=1, ipadx=8, ipady=4, padx=12, pady=(8, 4), sticky="ew")
        self.bInput.after(50, self.bInput.focus_set)
        # Result and History are organized into frames
        self.frameResult = ResultFrame(self)
        self.frameHistory = HistoryFrame(self)
        self.bind('<Escape>', lambda e, w=self: w.destroy())
        # Toast Notification
        self.notificationToast = ctk.CTkEntry(master=self, width=220, height=40, font=('Calibry', 20), 
                                              placeholder_text='Copied to Clipboard', justify='center')
        self.notificationToast.configure(state=ctk.DISABLED)

    def start(self):
        self.mainloop()

    def _onUpdateSwitch(self):
        self.switchDR.configure(text=self.switchDRValue.get())
        self._onChangeInput()

    def _onKey(self, keypressed):
        if keypressed.keysym == 'Return':
            self.frameHistory.addToAllHistories(self.getInputValue(), 
                                                self.frameResult.getDec(), 
                                                self.frameResult.getHex())
            self.clearInput()
        else:
            self._onChangeInput()

    def _onChangeInput(self):
        decValue = ''
        hexValue = ''
        formula = self.calculate(self.getInputValue())
        if formula:
            try:
                decValue = eval(compile(ast.parse(formula, mode='eval'), filename='', mode='eval'))
            except:
                decValue = 'error'
            # decvalue can be good and hexvalue can be error separately
            try:
                hexValue = hex(int(decValue))
            except:
                hexValue = 'error'
        self.frameResult.writeResults(decValue, hexValue)

    def _saveWindowPosition(self, event):
        with open(CONFIGURATION_FILENAME, "w") as conf:
            conf.write(self.geometry())

    def setGeometry(self):
        try:
            with open(CONFIGURATION_FILENAME, "r") as conf:
                self.geometry(conf.readlines()[0])
        except:
                self.geometry(DEFAULT_POSITION)

    def getInputValue(self):
        return self.bInput.get()

    def clearInput(self):
        self.bInput.delete(0, 'end')

    def copyToClipboard(self, content):
        self.clipboard_clear()
        self.clipboard_append(content)
        self.update()
        self.showNotificationToast()

    def showNotificationToast(self):
        centerx = int((self.winfo_width() - self.notificationToast.winfo_reqwidth()) / 2)
        self.notificationToast.place(x=centerx, y=80)
        self.notificationToast.after(800, self.notificationToast.place_forget)

    def calculate(self, formula):
        retVal = formula.replace('^', '**')
        if self.switchDRValue.get() == DEGREES:
            pattern = re.compile(r'(sin|cos|tan)\(([^)]+)\)')
            replacement = r'\1(radians(\2))'
            retVal = pattern.sub(replacement, retVal)
        return retVal

if __name__ == '__main__':
    Calculator().start()
