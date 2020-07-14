
pushd "%~dp0"

for %%F in (*.txt) do (    
    twincolor.exe "%%F"        
)

for %%F in (./log/*.txt) do (    
    twincolor.exe ".\log\%%F"
)

ren *.log *.

popd