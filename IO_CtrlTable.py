import sys
import re
import matplotlib.pyplot as plt
import numpy as np

max_sensor_num = 35
sensorName=['MANUAL_TRAY','MAIN_TRAY','SECOND_TRAY','THIRD_TRAY','FOURTH_TRAY','PAPER_DETECT_1','PAPER_DETECT_2',
'MAIN_FEED','DESKEW','REGISTRATION','REGISTRATION2','OPC_JAM','FUSER_OUT','EXIT','DUPLEX','FRONT_COVER',       
'REAR_COVER','DUPLEX_COVER','NEAR_EMPTY','TRAY1_COVER','TRAY1_CAPACITY','LIFTUP','PICKUP_CHECK','SECOND_TRAY_PAPER_OUT',
'THIRD_TRAY_PAPER_OUT','FOURTH_TRAY_PAPER_OUT','EXIT_CAPACITY','MANUAL_TRAY_PAPER_SIZE', 'MAIN_TRAY_PAPER_SIZE', 'MAIN_FRAME_PAPER_SIZE_LEFT', 'MAIN_FRAME_PAPER_SIZE_RIGHT', 
'S31', 'S32', 'S33', 'S34']

_lineNum = 0
_curTime = 0
_curSensorId =0
oldM3Time = 0
oldM3UsTime = 0
sensorName2id = {}
id = 0

for name in sensorName:
	sensorName2id[name] = id
	id += 1

def GetMsTimeFromStart(curTime, startTime):
	if curTime >= startTime:
		return curTime - startTime
	else:	
		return ( 0xFFFFFFFF - startTime + curTime+1)
		
def CheckMiceOutput(m):
	global _curTime	
	global _curSensorId
	global oldM3Time	
	global oldM3UsTime

	sensorId, sensorStatus, m3time, m3UsTime = m.groups()
	
	if sensorId not in sensorName2id:
		sensorName[_curSensorId] = sensorId
		sensorName2id[sensorId] = _curSensorId
		_curSensorId += 1

	if sensorId in sensorName2id:
		sensorId = sensorName2id[sensorId]
	else:		
		return None	
	
	sensorStatus = int(sensorStatus)
	m3time = int(m3time)
	m3UsTime = int(m3UsTime)			

	if _curTime == 0:		
		print("%s,%s,%s,%s,%s,%s,%s,%s,%s"%("Name", "ID", "state","time(ms)","time(us)","line","osDiff","hwDiff", "Note"))		

	if m3time <= 1:
		print("%s,%d,%d,%d,%d,%s"%(sensorName[sensorId], sensorId, sensorStatus,m3time,m3UsTime,_lineNum))		
	else:
		msDiff = GetMsTimeFromStart(m3time, oldM3Time)
		usDiff = GetMsTimeFromStart(m3UsTime, oldM3UsTime)/1000
		diff = abs(msDiff-usDiff)
		if diff > 1:
			note = "error"
		else:
			note = ""
		print("%s,%d,%d,%d,%d,%s,%d,%d,%s"%(sensorName[sensorId], sensorId, sensorStatus,m3time,m3UsTime,_lineNum,msDiff,usDiff,note))

	oldM3Time = int(m3time)
	oldM3UsTime = int(m3UsTime)			
	_curTime = 1
	

def SearchLog(f, patterns):
	global _lineNum
	for line in f:   
		_lineNum +=1
		for mp in patterns:
			pat, proc = mp
			match_result = pat.search(line)
			if match_result:				
				proc(match_result)
				break

if __name__ == '__main__':	
	patterns = [									
			(re.compile(r'IO_CtrlTable_SetValue:\d+ : (\w+) id=\d+ state=(\d+) T\((\d+)\) GetuS\((\d+)\)'), CheckMiceOutput)
			]
	
	SearchLog(sys.stdin, patterns)
	
