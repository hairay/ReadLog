@echo off
start "" /B python "%~dp0outlook_forward_service.py" > "%~dp0forward_log.log" 2>&1
echo [OK] Outlook Forwarding Service started.
echo      Log file: %~dp0forward_log.log
echo      To stop:  taskkill /f /im python.exe
echo      To auto-start on boot: Place a shortcut in shell:startup
pause
