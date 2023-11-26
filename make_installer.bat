echo off
setlocal enabledelayedexpansion

set "package=customtkinter"
call :GetPackageLocation

set "builddir=pyinstaller"
mkdir "%builddir%"
cd "%builddir%"
pyinstaller --noconfirm --onedir --windowed --icon "../_internal/Wineass-Ios7-Redesign-Calculator.ico" --add-data "!location!/customtkinter;customtkinter/"  "../ecalc.py"
cd ..
copy _internal\*.ico %builddir%\Dist\ecalc\_internal\
echo Installer package is created in "%builddir%\dist\ecalc" directory

goto :EOF

rem Subroutine to get location of a Python package
rem Batch version of the linux command: 
rem pip show $1 | grep 'Location:' | cut -d ':' -f 2
:GetPackageLocation
rem Run pip show and filter the line containing 'Location:'
for /f "tokens=*" %%a in ('pip show !package! ^| findstr /i "Location:"') do (
    set "location=%%a"
    rem Remove leading and trailing spaces
    set "location=!location:*: =!"
    set "location=!location:\=/!"
    echo Location of !package!: !location!
)
goto :EOF

endlocal
