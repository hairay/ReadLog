
pushd "%~dp0"

for %%F in (*.txt) do (    
    type "%%F" | python vm3_sensor.py > "MCU_%%F.log"
    rename curve.png "%%F".png	
)

for %%F in (./log/*.txt) do (    
    type ".\log\%%F" | python vm3_sensor.py > ".\log\MCU_%%F.log"      
    move .\curve.png ".\log\%%F.png"	
)

popd