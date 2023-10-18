
pushd "%~dp0"

for %%F in (*.txt) do (    
    type "%%F" | python qbitScanBand.py > "%%F"-band.log        
)

for %%F in (./log/*.txt) do (    
    type ".\log\%%F" | python qbitScanBand.py > ".\log\%%F-band.log"
)

popd