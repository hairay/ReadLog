
pushd "%~dp0"

for %%F in (*.txt) do (    
    type "%%F" | python read_key_word.py > "%%F"-keyword.log
)

for %%F in (./log/*.txt) do (    
    type ".\log\%%F" | python read_key_word.py > .\log\"%%F"-keyword.log
)

popd