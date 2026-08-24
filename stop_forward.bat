@echo off
rem Stop only the outlook_forward_service.py process (does NOT kill other python.exe)
powershell -NoProfile -Command "Get-CimInstance Win32_Process | Where-Object { ($_.Name -eq 'python.exe' -or $_.Name -eq 'pythonw.exe') -and $_.CommandLine -like '*outlook_forward_service*' } | ForEach-Object { Write-Host ('Stopping PID ' + $_.ProcessId); Stop-Process -Id $_.ProcessId -Force }"
echo [OK] Outlook Forwarding Service stopped (if it was running).
pause
