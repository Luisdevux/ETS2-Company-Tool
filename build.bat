@echo off
echo Compilando ETS2CompanyTool...
python -m PyInstaller --onefile --windowed --name ETS2CompanyTool main.py
echo.
echo Pronto! Executavel atualizado em: dist\ETS2CompanyTool.exe
pause
