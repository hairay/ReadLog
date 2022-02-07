
pushd "%~dp0"

for %%F in (*.txt) do (    
    type "%%F" | python vm3_temprature.py > "%%F".csv      
    rename curve.png "%%F"-temp.png	
)

for %%F in (./log/*.txt) do (    
    type ".\log\%%F" | python vm3_temprature.py > ".\log\%%F.csv"      
    move .\curve.png ".\log\%%F-temp.png"	
)

popd