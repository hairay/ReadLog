
pushd "%~dp0"

for %%F in (*.txt) do (    
    type "%%F" | python mcu_in_out.py > "MCU_IO_%%F.log"
    rename curve.png "%%F"-inout.png	
)

for %%F in (./log/*.txt) do (    
    type ".\log\%%F" | python mcu_in_out.py > ".\log\MCU_IO_%%F.log"      
    move .\curve.png .\log\"%%F"-inout.png
)

popd