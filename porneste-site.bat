@echo off
chcp 65001 >nul
rem Pornește pagina pe acest calculator, la adresa http://localhost:8000
rem Folosește serverul inclus în Python și răspunde doar pe acest calculator.
rem Se oprește prin închiderea acestei ferestre.
cd /d "%~dp0site"
start "" /b cmd /c "timeout /t 2 >nul & start http://localhost:8000"
where py >nul 2>nul && (py -m http.server 8000 --bind 127.0.0.1 & goto :eof)
where python >nul 2>nul && (python -m http.server 8000 --bind 127.0.0.1 & goto :eof)
echo.
echo Python nu este instalat pe acest calculator. Se descarcă de la python.org.
pause
