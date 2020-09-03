import sys
import re
import matplotlib.pyplot as plt
import numpy as np

max_sensor_num = 30
sensorName=['MANUAL_TRAY','MAIN_TRAY','SECOND_TRAY','THIRD_TRAY','FOURTH_TRAY','PAPER_DETECT_1','PAPER_DETECT_2',
'MAIN_FEED','DESKEW','REGISTRATION','REGISTRATION2','OPC_JAM','FUSER_OUT','EXIT','DUPLEX','FRONT_COVER',       
'REAR_COVER','DUPLEX_COVER','NEAR_EMPTY','TRAY1_COVER','TRAY1_CAPACITY','LIFTUP','PICKUP_CHECK','SECOND_TRAY_PAPER_OUT',
'THIRD_TRAY_PAPER_OUT','FOURTH_TRAY_PAPER_OUT','EXIT_CAPACITY','MANUAL_TRAY_PAPER_SIZE', 'MAIN_TRAY_PAPER_SIZE', 'S29']

_lineNum = 0
_curTime = 0
_curSensorId =0
_startM3pTime = 0.0
sCurM3Time = 0
sStartM3Time = 0

sensorTimeX = [[] for _ in range(max_sensor_num)]
sensorPosY = [[] for _ in range(max_sensor_num)]
sensorName2id = {}
id = 0

for name in sensorName:
	#print("%d=%s" % (id,name))	
	sensorName2id[name] = id
	id += 1
stateName2id = {'NO_PAPER':0, 'HAS_PAPER':1, 'COVER_OPEN':1, 'COVER_CLOSE':0}


def RestartM3(m):
	global _curTime
	global _startM3pTime
	global sCurM3Time
	global sStartM3Time
	#debugFp.write("RestartM3 _startM3pTime:%f _curM3pTime:%f \n" % (_startM3pTime, _curM3pTime))	
	_startM3pTime = _curTime
	sStartM3Time = sCurM3Time

def RecordSensorInfo(sensorId, sensorStatus, m3time):
	global sCurM3Time
	global sStartM3Time

	sCurM3Time = int(m3time) + sStartM3Time
	print("%40s %6d %8d %12s %12s" % (sensorName[sensorId], sensorId, sensorStatus,int(sCurM3Time)*1000,_lineNum))
	if len(sensorTimeX[sensorId]) > 0 and sensorTimeX[sensorId][-1] >= _curTime:
			return None	
	
	if len(sensorPosY[sensorId]) > 0 and sensorPosY[sensorId][-1] != sensorStatus:
		sensorTimeX[sensorId].append(_curTime)
		sensorPosY[sensorId].append(sensorPosY[sensorId][-1])
	sensorTimeX[sensorId].append(_curTime)
	sensorPosY[sensorId].append(sensorStatus)

def ShowM3PSensor(m):
	global _curTime	
	
	sensorId, sensorStatus, m3time = m.groups()
	if _curTime == 0:		
		print("%40s %6s %8s %12s %12s" % ("Name", "ID", "state","time(us)","line"))

	_curTime = float(m3time)/1000.0 + _startM3pTime
	sensorId = int(sensorId)
	sensorStatus = int(sensorStatus)
	RecordSensorInfo(sensorId, sensorStatus, m3time)

def CheckVm3Sensor(m):
	global _curTime	
	global _curSensorId

	m3time, sensorId, sensorStatus = m.groups()
	if _curTime == 0:		
		print("%40s %6s %8s %12s %12s" % ("Name", "ID", "state","time(us)","line"))
	_curTime = float(m3time)/1000.0 + _startM3pTime

	if sensorId not in sensorName2id:
		sensorName[_curSensorId] = sensorId
		sensorName2id[sensorId] = _curSensorId
		_curSensorId += 1

	if sensorId in sensorName2id:
		sensorId = sensorName2id[sensorId]
	else:
		#print("%40s %6s %8s %12s %12s" % (sensorId, "XXX", "XXX","XXX","XXX"))
		return None	
	if sensorStatus in stateName2id:
		sensorStatus = stateName2id[sensorStatus]
	else:
		#print("%40s %6s %8s %12s %12s" % ("XXX", "XX", sensorStatus,"XXX","XXX"))
		return None	
				
	RecordSensorInfo(sensorId, sensorStatus, m3time)

def CheckMiceSensor(m):
	global _curTime	
	global _curSensorId

	sensorId, sensorStatus, m3time = m.groups()
	if _curTime == 0:		
		print("%40s %6s %8s %12s %12s" % ("Name", "ID", "state","time(us)","line"))
	_curTime = float(m3time)/1000.0 + _startM3pTime

	if sensorId not in sensorName2id:
		sensorName[_curSensorId] = sensorId
		sensorName2id[sensorId] = _curSensorId
		_curSensorId += 1

	if sensorId in sensorName2id:
		sensorId = sensorName2id[sensorId]
	else:
		#print("%40s %6s %8s %12s %12s" % (sensorId, "XXX", "XXX","XXX","XXX"))
		return None	
	
	sensorStatus = int(sensorStatus)
	RecordSensorInfo(sensorId, sensorStatus, m3time)

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
			(re.compile(r'PrintParser_SensorTestInfoCallBackProc:\d+ : sensor_id=(\d+), sensorStatus=(\d+), timeMS=(\d+) Enter Time: \d+'), ShowM3PSensor),
			#(re.compile(r'UpdatePrinterSensorStatus:\d+\(Time:\d+\) : sensor_id=(\d+), sensorStatus=(\d+), timeMS=(\d+)'), ShowM3PSensor),			
			(re.compile(r'PRINTER_FUNC_CheckSensorStatus:\d+\((\d+)ms\) : \[Sensor\](\w+)=(\w+).*'), CheckVm3Sensor),
			(re.compile(r'Sensor_PrintStatas:\d+ : \[Sensor\] (\w+)\(Sensor Type, Status, RegisterSN\) = \(\d+, (\w+), \d+\). T\((\d+).*\)'), CheckMiceSensor),
			(re.compile(r'PRINTER_FUNC_InitDebugLog'), RestartM3),
			(re.compile(r'DSP_IP_Init'), RestartM3)
			]
	
	SearchLog(sys.stdin, patterns)
	my_dpi = 96
	plt.figure(figsize=(2048/my_dpi, 1024/my_dpi), dpi=my_dpi)
	lineNum = max_sensor_num
	for i in range(max_sensor_num):
		if len(sensorTimeX[i]) > 1:
			sensorPosY[i] = list(np.asarray(sensorPosY[i])*8+lineNum*10)			
			plt.plot(sensorTimeX[i], sensorPosY[i], label=sensorName[i])
			lineNum -= 1
	
	plt.legend(loc='upper left',bbox_to_anchor=(1,1))
	plt.tight_layout(pad=3)
	plt.title("Sensor Curve", fontsize=8)
	plt.xlabel("Time(Sec)", fontsize=14)
	plt.ylabel("sensor pos", fontsize=14)
	plt.tick_params(axis='both', labelsize=8, color='red')
	#plt.show()
	plt.savefig('curve.png', bbox_inches='tight')
