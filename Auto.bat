
pushd "%~dp0"

for %%F in (*.txt) do (    
    type "%%F" | python readlog.py > "%%F".log        
)

for %%F in (./log/*.txt) do (    
    type ".\log\%%F" | python readlog.py > ".\log\%%F.log"          
)

popd