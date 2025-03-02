#!/bin/bash

source .venv/bin/activate
pyinstaller \
    --onefile \
    --hidden-import=tkinter \
    --hidden-import=pillow \
    --hidden-import='PIL._tkinter_finder' \
    --add-data '_internal/Wineass-Ios7-Redesign-Calculator.png:_internal' \
    --icon=_internal/Wineass-Ios7-Redesign-Calculator.png ecalc.py
