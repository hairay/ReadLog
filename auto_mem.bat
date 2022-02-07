
pushd "%~dp0"

for %%F in (*.txt) do (    
    type "%%F" | python memory.py > "%%F"-mem.log        
)

for %%F in (./log/*.txt) do (    
    type ".\log\%%F" | python memory.py > ".\log\%%F-mem.log"          
)

popd