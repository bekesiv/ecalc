#!/bin/bash

cd ..
mkdir -p .pyinstaller
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
fi
source .venv/bin/activate
python3 -m pip install -r requirements.txt
python3 -m pip install pyinstaller
cd .pyinstaller

pyinstaller \
    --onefile \
    --hidden-import=tkinter \
    --hidden-import=pillow \
    --hidden-import='PIL._tkinter_finder' \
    --add-data '../icon/Wineass-Ios7-Redesign-Calculator.png:icon' \
    --icon=../icon/Wineass-Ios7-Redesign-Calculator.png \
    ../ecalc.py
