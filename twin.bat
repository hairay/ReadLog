
pushd "%~dp0"

for %%F in (*.txt) do (    
    twincolor.exe "%%F"
    if exist "MCU_%%F.log" ren "MCU_%%F.log" "MCU_%%~nF.txt"
)

for %%F in (./log/*.txt) do (    
    twincolor.exe ".\log\%%F"
    if exist ".\log\MCU_%%F.log" ren ".\log\MCU_%%F.log" "MCU_%%~nF.txt"
)

popd
