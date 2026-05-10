@echo off
echo ====================================
echo   HumanTyper Pro - .EXE Builder
echo ====================================
echo.

echo [1/3] Installing dependencies...
pip install -r requirements.txt

echo.
echo [2/3] Building .exe with PyInstaller...
pyinstaller --onefile ^
            --windowed ^
            --name "HumanTyper_Pro" ^
            --icon=icon.ico ^
            autotyper.py

echo.
echo [3/3] Done!
echo Your .exe is in the "dist" folder: dist\HumanTyper_Pro.exe
echo.
pause
