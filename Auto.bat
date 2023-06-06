
pushd "%~dp0"

for %%F in (*.txt) do (    
    cat2 "%%F" | python readlog.py > "%%F"-time.log
)

for %%F in (./log/*.txt) do (    
    cat2 ".\log\%%F" | python readlog.py > .\log\"%%F"-time.log
)

popd