@echo off
chcp 65001 >nul
rem Urcă proiectul în https://github.com/mihaialex93/tinu, pe ramura main.
rem Nu forțează nimic: dacă depozitul are deja alt conținut pe main, se oprește.
rem Rezultatul fiecărui pas se scrie în urcare-github.log.
cd /d "%~dp0"
set JURNAL=urcare-github.log
echo ==== %date% %time% ==== > "%JURNAL%"
where git >> "%JURNAL%" 2>&1
if errorlevel 1 (
  echo EROARE: Git nu este instalat. >> "%JURNAL%"
  goto :sfarsit
)
if not exist ".git" git init -b main >> "%JURNAL%" 2>&1
git remote remove origin >nul 2>nul
git remote add origin https://github.com/mihaialex93/tinu.git >> "%JURNAL%" 2>&1
git add -A >> "%JURNAL%" 2>&1
if exist mesaj-commit.txt (git commit -F mesaj-commit.txt >> "%JURNAL%" 2>&1) else (git commit -m "Actualizare site" >> "%JURNAL%" 2>&1)
git branch -M main >> "%JURNAL%" 2>&1
echo PAS: push >> "%JURNAL%"
git push -u origin main >> "%JURNAL%" 2>&1
echo COD_PUSH=%errorlevel% >> "%JURNAL%"
git log --oneline -3 >> "%JURNAL%" 2>&1
git status -sb >> "%JURNAL%" 2>&1
:sfarsit
echo GATA >> "%JURNAL%"
