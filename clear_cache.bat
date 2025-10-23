@echo off
REM TTZ.KT AI - Cache Clear Script (Windows)
REM Use this when you get "attribute 'UPPER'" error

echo Clearing Python cache...

REM Remove __pycache__ directories
for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d"

REM Remove .pyc files
del /s /q *.pyc 2>nul

REM Remove .streamlit cache
if exist .streamlit\cache rd /s /q .streamlit\cache

echo.
echo Cache cleared!
echo.
echo Now restart your app:
echo   streamlit run app.py
echo.
pause
