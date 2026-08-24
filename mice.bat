
pushd "%~dp0"

for %%F in (*.txt) do (    
    micelog.exe "%%F"
    if exist "MCU_%%F.log" ren "MCU_%%F.log" "MCU_%%~nF.txt"
)

for %%F in (./log/*.txt) do (    
    micelog.exe ".\log\%%F"
    if exist ".\log\MCU_%%F.log" ren ".\log\MCU_%%F.log" "MCU_%%~nF.txt"
)

popd
