
pushd "%~dp0"

for %%F in (*.txt) do (    
    type "%%F" | python IO_CtrlTable.py > "MCU_Output_%%F.csv"
)

for %%F in (./log/*.txt) do (    
    type ".\log\%%F" | python IO_CtrlTable.py > ".\log\MCU_Output_%%F.csv"          
)

popd