@echo off
setlocal enabledelayedexpansion

if "%1"=="/?" goto :ShowHelp
if "%1"=="-h" goto :ShowHelp
if "%1"=="--help" goto :ShowHelp

set "package=customtkinter"
call :GetPackageLocation

set "builddir=pyinstaller"
mkdir "%builddir%"
cd "%builddir%"

set "upxDir="
if "%~1" neq "" (
    set "upxDir=--upx-dir=%1"
)

pyinstaller --noconfirm --onefile --windowed^
 --icon "icon/Wineass-Ios7-Redesign-Calculator.ico"^
 --add-data "!location!/customtkinter;customtkinter/"^
 --add-data "icon/Wineass-Ios7-Redesign-Calculator.ico:icon"^
 %upxDir% ^
 "src/ecalc.py"
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
exit /b

:ShowHelp
echo Usage: myscript.bat [UPX_DIRECTORY]
echo   UPX_DIRECTORY  Optional path to the UPX directory.
exit /b