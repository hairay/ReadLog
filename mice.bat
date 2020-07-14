
pushd "%~dp0"

for %%F in (*.txt) do (    
    micelog.exe "%%F"        
)

for %%F in (./log/*.txt) do (    
    micelog.exe ".\log\%%F"
)

ren *.log *.

popd