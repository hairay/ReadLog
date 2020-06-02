import sys
import re
import matplotlib.pyplot as plt

debugFp = open("debug.log", "a")
_lineNum = 0
_startTime = 0
_header13 = 'time,state,centerHw,centerSw,sideHw,sideSw,targetHw,targetSw,set1,set2,envHw,envSw,set3'
_header14 = 'time,state,centerHw,centerSw,sideHw,sideSw,targetHw,targetSw,set1,set2,set3,envHw,envSw,set4'
_headerTwinColor = 'state,centerHw,centerSw,sideHw,sideSw,envSw,type,targetSw,LampOn,LampOn_Side,time'
_headerTwinColor12 = 'state,centerHw,centerSw,sideHw,sideSw,envSw,type,targetSw,LampOn,LampOn_Side,set,time'
_headerTwinColor7 = 'state,centerHw,centerSw,sideHw,sideSw,targetSw,time'
_headerMice14 = 'state,centerHw,centerSw,sideHw,sideSw,envHw,envSw,EnvFuserError,EnvType,mode1,mode2,SideTherCheck,targetSw,time'
_headerMice15 = 'state,centerHw,centerSw,sideHw,sideSw,envHw,envSw,EnvFuserError,EnvType,mode1,mode2,SideTherCheck,targetSw,PaperNip,time'

timeX = []
centerY = []
sideY = []
targetY = []
envY = []

def AssignVal(m):
	global debugFp
	now = float(m.groups(0)[0])/1000.0

	if len(timeX) > 0 and timeX[-1] > now:		 
			return None

	timeX.append(now)
	centerY.append(float(m.groups(0)[3]))
	sideY.append(float(m.groups(0)[5]))
	targetY.append(float(m.groups(0)[7]))
	envY.append(float(m.groups(0)[-2]))	
	if float(m.groups(0)[-2]) > 50:
		debugFp.write("error env temp %s line:%d \n" % (m.groups(0)[-2], _lineNum))
	

def ShowHeatingInfo13(m):	
	global _startTime
	if _startTime == 0:
		print(_header13)
		_startTime = float(m.groups(0)[0])/1000.0			
	print("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s" % (m.groups()))	
	AssignVal(m)

def ShowHeatingInfo14(m):	
	global _startTime		
	if _startTime == 0:
		print(_header14)	
		_startTime = float(m.groups(0)[0])/1000.0			
	print("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s" % (m.groups()))	
	AssignVal(m)

def ShowHeatingInfoTwinColor(m):
	global _startTime		
	if _startTime == 0:
		if len(m.groups(0)) == 7:
			print(_headerTwinColor7)
		elif len(m.groups(0)) == 12:
			print(_headerTwinColor12)
		else:
			print(_headerTwinColor)
	_startTime = float(m.groups(0)[-1])/1000.0
	if len(m.groups(0)) == 7:	
		print("%s,%s,%s,%s,%s,%s,%s" % (m.groups()))
	elif len(m.groups(0)) == 12:	
		print("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s" % (m.groups()))
	else:	
		print("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s" % (m.groups()))
	now = float(m.groups(0)[-1])/1000.0

	if len(timeX) > 0 and timeX[-1] > now:		 
			return None

	timeX.append(now)
	centerY.append(float(m.groups(0)[2]))
	sideY.append(float(m.groups(0)[4]))
	
	if len(m.groups(0)) > 7:
		envY.append(float(m.groups(0)[5]))	
		targetY.append(float(m.groups(0)[7]))
	else:
		targetY.append(float(m.groups(0)[5]))	
def ShowHeatingInfoMice(m):
	global _startTime		
	if _startTime == 0:
		if len(m.groups(0)) == 15:
			print(_headerMice15)
		else:	
			print(_headerMice14)
		_startTime = float(m.groups(0)[-1])/1000.0
	if len(m.groups(0)) == 15:		
		print("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s" % (m.groups()))
	else:	
		print("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s" % (m.groups()))
	now = float(m.groups(0)[-1])/1000.0

	if len(timeX) > 0 and timeX[-1] > now:		 
			return None
	timeX.append(now)
	centerY.append(float(m.groups(0)[2]))
	sideY.append(float(m.groups(0)[4]))
	targetY.append(float(m.groups(0)[12]))
	envY.append(float(m.groups(0)[6]))

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
			(re.compile(r'FUSER_FUNC_ShowHeatingInfo:\d+\((\d+)ms\) : \[(\w+)\], \( (\d+), (\d+), (\d+), (\d+), (\d+), (\d+), (\d+), (\d+), (\d+), (\d+), (\d+) \)'), ShowHeatingInfo13),
			(re.compile(r'FUSER_FUNC_ShowHeatingInfo:\d+\((\d+)ms\) : \[(\w+)\], \( (\d+), (\d+), (\d+), (\d+), (\d+), (\d+), (\d+), (\d+), (\d+), (\d+), (\d+), (\d+) \)'), ShowHeatingInfo14),
			(re.compile(r'O_TwinColor_Fuser_Action_ISR_ADC_Temp:\d+ : \[(\w+)\], (\d+), (\d+), (\d+), (\d+), (\d+), (\d+), (\d+), (\d+), (\d+). (\d+) ms'), ShowHeatingInfoTwinColor),
			(re.compile(r'O_TwinColor_Fuser_Action_ISR_ADC_Temp:\d+ : \[(\w+)\], (\d+), (\d+), (\d+), (\d+), (\d+), (\d+), (\d+), (\d+), (\d+), (\d+). (\d+) ms'), ShowHeatingInfoTwinColor),
			(re.compile(r'O_TwinColor_Fuser_Action_ISR_ADC_Temp:\d+ : \[(\w+)\], (\d+), (\d+), (\d+), (\d+), (\d+), (\d+) ms'), ShowHeatingInfoTwinColor),
			(re.compile(r'O_MICE_Fuser_Action_ISR_ADC_Temp:\d+ : \[(\w+)\], \((\d+), (\d+), (\d+), (\d+), (\d+), (\d+), (\d+), (\d+), (\d+), (\d+), (\d+)\) gFuserTargetTemp=(\d+), (\d+) ms'), ShowHeatingInfoMice),
			(re.compile(r'O_MICE_Fuser_Action_ISR_ADC_Temp:\d+ : \[(\w+)\], \((\d+), (\d+), (\d+), (\d+), (\d+), (\d+), (\d+), (\d+), (\d+), (\d+), (\d+)\) gFuserTargetTemp=(\d+),Nip=(\d+), (\d+) ms'), ShowHeatingInfoMice),
			]
	SearchLog(sys.stdin, patterns)
	my_dpi = 96
	plt.figure(figsize=(2048/my_dpi, 1024/my_dpi), dpi=my_dpi)
	plt.plot(timeX, centerY, label='Center')
	plt.plot(timeX, sideY, label='Side')
	plt.plot(timeX, targetY, label='Target')
	if len(envY) > 1:
		plt.plot(timeX, envY, label='Env')
	plt.legend()
	plt.title("Temprature Curve", fontsize=24)
	plt.xlabel("Time(Sec)", fontsize=14)
	plt.ylabel("Temprature", fontsize=14)
	plt.tick_params(axis='both', labelsize=12, color='red')
	#plt.show()
	plt.savefig('curve.png', bbox_inches='tight')     # 存檔

debugFp.close()