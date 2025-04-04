#!/bin/bash

sudo install -v -o root -g root -m 755 extras/ecalc.desktop /usr/share/applications/
sudo install -v -o root -g root -m 644 icon/Wineass-Ios7-Redesign-Calculator.png to /usr/share/icons/ecalc.png
sudo install -v

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

sudo install -v -o root -g root -m 755 dist/ecalc /usr/local/bin/ecalc