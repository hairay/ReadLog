import sys
import re
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.pyplot import MultipleLocator
from matplotlib.backend_bases import MouseButton

debugFp = None
_lineNum = 0
_startTime = 0
_curM3pTime = 0.0
_startM3pTime = 0.0
_tmpDiff = 0.0
_tmpDiffLine = 0
_header13 = 'time,state,centerHw,centerSw,sideHw,sideSw,targetHw,targetSw,set1,set2,envHw,envSw,set3'
_header14 = 'time,state,centerHw,centerSw,sideHw,sideSw,targetHw,targetSw,set1,set2,envHw,envSw,set3,set4'
_header15 = 'time,state,centerHw,centerSw,sideHw,sideSw,targetHw,targetSw,set1,set2,set3,envHw,envSw,set4, set5'
_headerTwinColor = 'state,centerHw,centerSw,sideHw,sideSw,envSw,type,targetSw,LampOn,LampOn_Side,time'
_headerTwinColor12 = 'state,centerHw,centerSw,sideHw,sideSw,envSw,type,targetSw,LampOn,LampOn_Side,set,time'
_headerTwinColor7 = 'state,centerHw,centerSw,sideHw,sideSw,targetSw,time'
_headerMice14 = 'state,centerHw,centerSw,sideHw,sideSw,envHw,envSw,EnvFuserError,EnvType,mode1,mode2,SideTherCheck,targetSw,time'
_headerMice15 = 'state,centerHw,centerSw,sideHw,sideSw,envHw,envSw,EnvFuserError,EnvType,mode1,mode2,SideTherCheck,targetSw,PaperNip,time'
_headerPanther = 'sideSw,centerSw,targetSw1,targetSw2,time1,time2'
_headerRiscv = 'time,state,center,side,env,target,duty,nip'

timeX = []
centerY = []
sideY = []
targetY = []
NipY = []
DutyY = []
envY = []

def RestartM3(m):
	global _curM3pTime
	global _startM3pTime
	
	#debugFp.write("RestartM3 _startM3pTime:%f _curM3pTime:%f \n" % (_startM3pTime, _curM3pTime))	
	_startM3pTime = _curM3pTime
	
def AssignVal(m, envPos):
	global debugFp
	global _curM3pTime
	global _startM3pTime
	global _tmpDiff, _tmpDiffLine
	now = float(m.groups(0)[0])/1000.0 + _startM3pTime

	if len(timeX) > 0 and timeX[-1] > now:					
			debugFp.write("wrong procedure now:%f  previous:%f line:%d \n" % (now, timeX[-1], _lineNum)) 
			return None
	
	_curM3pTime = now
	timeX.append(now)	
	centerY.append(float(m.groups(0)[3]))
	sideY.append(float(m.groups(0)[5]))
	targetY.append(float(m.groups(0)[7]))
	DutyY.append(float(m.groups(0)[-6]))	
	NipY.append(float(m.groups(0)[-1])*2.25+2.5)
	#debugFp.write("Duty:%f  NipY:%f line:%d \n" % (float(m.groups(0)[-4]), float(m.groups(0)[-1]), _lineNum)) 
	envY.append(float(m.groups(0)[envPos]))
	
	if(abs(float(m.groups(0)[3])- float(m.groups(0)[5])) > _tmpDiff):
		_tmpDiff = abs(float(m.groups(0)[3])- float(m.groups(0)[5]))
		_tmpDiffLine = _lineNum
	
	if float(m.groups(0)[envPos]) > 50:
		debugFp.write("error env temp %s line:%d \n" % (m.groups(0)[envPos], _lineNum))
	

def ShowHeatingInfo13(m):	
	global _startTime
	if _startTime == 0:
		print(_header13)
		_startTime = float(m.groups(0)[0])/1000.0			
	print("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s" % (m.groups()))	
	AssignVal(m, -2)

def ShowHeatingInfo14(m):	
	global _startTime		
	if _startTime == 0:
		print(_header14)	
		_startTime = float(m.groups(0)[0])/1000.0			
	print("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s" % (m.groups()))	
	AssignVal(m, -3)

def ShowHeatingInfo15(m):	
	global _startTime		
	if _startTime == 0:
		print(_header15)	
		_startTime = float(m.groups(0)[0])/1000.0			
	print("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s" % (m.groups()))	
	AssignVal(m, -3)

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
		envY.append(np.nan)

	DutyY.append(np.nan)
	NipY.append(np.nan)

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
	DutyY.append(float(m.groups(0)[11]))
	targetY.append(float(m.groups(0)[12]))
	if len(m.groups(0)) == 15:
		NipY.append(float(m.groups(0)[13])*2.25+2.5)
	else:
		NipY.append(np.nan)
	envY.append(float(m.groups(0)[6]))


def ShowHeatingInfoPanther(m):
	global _startTime		
	if _startTime == 0:		
			print(_headerPanther)
			_startTime = float(m.groups(0)[-2])/1000.0
	
	print("%s,%s,%s,%s,%s,%s" % (m.groups()))
	
	now = float(m.groups(0)[-2])/1000.0

	if len(timeX) > 0 and timeX[-1] > now:		 
			return None

	timeX.append(now)
	centerY.append(float(m.groups(0)[1]))
	sideY.append(float(m.groups(0)[0]))
	
	targetY.append(float(m.groups(0)[2]))
	envY.append(np.nan)
	DutyY.append(np.nan)
	NipY.append(np.nan)

def ShowHeatingInfoRiscv(m):
	global _startTime		
	if _startTime == 0:		
			print(_headerRiscv)
			_startTime = float(m.group(1))/1000.0
	
	print("%s,%s,%s,%s,%s,%s,%s,%s" % (m.group(1), m.group(2), m.group(3), m.group(4), m.group(5), m.group(6), m.group(7), m.group(8)))
	
	now = float(m.group(1))/1000.0

	if len(timeX) > 0 and timeX[-1] > now:		 
			return None

	timeX.append(now)
	centerY.append(float(m.group(3)))
	sideY.append(float(m.group(4)))
	envY.append(float(m.group(5)))
	targetY.append(float(m.group(6)))
	DutyY.append(float(m.group(7)))
	NipY.append(float(m.group(8))*2.25+2.5)
	
def ShowHeatingInfoRiscvV2(m):
	global _startTime		
	if _startTime == 0:		
			print(_headerRiscv)
			_startTime = float(m.group(1))/1000.0
	
	print("%s,%s,%s,%s,%s,%s,%s,%s" % (m.group(1), m.group(2), m.group(3), m.group(4), m.group(5), m.group(8), m.group(6), m.group(11)))
	
	now = float(m.group(1))/1000.0

	if len(timeX) > 0 and timeX[-1] > now:		 
			return None

	timeX.append(now)
	centerY.append(float(m.group(3)))
	sideY.append(float(m.group(4)))
	envY.append(float(m.group(5)))
	targetY.append(float(m.group(8)))
	DutyY.append(float(m.group(6)))
	NipY.append(float(m.group(11))*2.25+2.5)

def on_move(event):
    if event.inaxes:
        print(f'data coords {event.xdata} {event.ydata},',
              f'pixel coords {event.x} {event.y}')


def on_click(event):
    if event.button is MouseButton.LEFT:
        if event.xdata is not None and event.ydata is not None:
            label = "Time(Sec) {:.3f} {:.3f}".format(event.xdata, event.ydata)        
            plt.xlabel(label , fontsize=14)
            event.canvas.draw()

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

#2901: [Fuser] State = 0(Initial), (TempA3, TempA4, gCtrlTempA3, gCtrlTempA4) = /185/192/0/0/ T(1936, 2194)

if __name__ == '__main__':	
	debugFp = open("debug.log", "w")
	patterns = [													
			(re.compile(r'FUSER_FUNC_ShowHeatingInfo:\d+\((\d+)ms\) : \[(\w+)\], \( (-?\d+), (-?\d+), (-?\d+), (-?\d+), (-?\d+), (-?\d+), (-?\d+), (-?\d+), (-?\d+), (-?\d+), (-?\d+) \)'), ShowHeatingInfo13),
			(re.compile(r'FUSER_FUNC_ShowHeatingInfo:\d+\((\d+)ms\) : \[(\w+)\], \( (-?\d+), (-?\d+), (-?\d+), (-?\d+), (-?\d+), (-?\d+), (-?\d+), (-?\d+), (-?\d+), (-?\d+), (-?\d+), (-?\d+) \)'), ShowHeatingInfo14),
			(re.compile(r'FUSER_FUNC_ShowHeatingInfo:\d+\((\d+)ms\) : \[(\w+)\], \( (-?\d+), (-?\d+), (-?\d+), (-?\d+), (-?\d+), (-?\d+), (-?\d+), (-?\d+), (-?\d+), (-?\d+), (-?\d+), (-?\d+), (-?\d+) \)'), ShowHeatingInfo15),
			(re.compile(r'O_TwinColor_Fuser_Action_ISR_ADC_Temp:\d+ : \[(\w+)\], (-?\d+), (-?\d+), (-?\d+), (-?\d+), (-?\d+), (-?\d+), (-?\d+), (-?\d+), (-?\d+), (-?\d+). (\d+) ms'), ShowHeatingInfoTwinColor),
			(re.compile(r'O_TwinColor_Fuser_Action_ISR_ADC_Temp:\d+ : \[(\w+)\], (-?\d+), (-?\d+), (-?\d+), (-?\d+), (-?\d+), (-?\d+), (-?\d+), (-?\d+), (-?\d+). (\d+) ms'), ShowHeatingInfoTwinColor),
			(re.compile(r'O_TwinColor_Fuser_Action_ISR_ADC_Temp:\d+ : \[(\w+)\], (-?\d+), (-?\d+), (-?\d+), (-?\d+), (-?\d+), (-?\d+) ms'), ShowHeatingInfoTwinColor),
			(re.compile(r'.*Fuser_Action_ISR_ADC_Temp:\d+ : \[(\w+)\], \((-?\d+), (-?\d+), (-?\d+), (-?\d+), (-?\d+), (-?\d+), (-?\d+), (-?\d+), (-?\d+), (-?\d+), (-?\d+)\) gFuserTargetTemp=(-?\d+), (\d+) ms'), ShowHeatingInfoMice),
			(re.compile(r'.*Fuser_Action_ISR_ADC_Temp:\d+ : \[(\w+)\], \((-?\d+), (-?\d+), (-?\d+), (-?\d+), (-?\d+), (-?\d+), (-?\d+), (-?\d+), (-?\d+), (-?\d+), (-?\d+)\) gFuserTargetTemp=(-?\d+),Nip=(-?\d+), (\d+) ms'), ShowHeatingInfoMice),
			(re.compile(r'.*Fuser_Action_ISR_ADC_Temp:\d+ : \[(\w+)\], \((-?\d+), (-?\d+), (-?\d+), (-?\d+), (-?\d+), (-?\d+), (-?\d+), (-?\d+), (-?\d+), (-?\d+), (-?\d+)\) gFuserTargetTemp=(-?\d+),gA4FlickerMode=\d+,Nip=(-?\d+), (\d+)'), ShowHeatingInfoMice),			
			(re.compile(r'\(TempA3, TempA4, gCtrlTempA3, gCtrlTempA4\) = /(-?\d+)/(-?\d+)/(-?\d+)/(-?\d+)/ T\((\d+), (\d+)\)'), ShowHeatingInfoPanther),
			(re.compile(r'FUSER_FUNC_ShowHeatingInfo:\d+\((\d+)ms\) : \[(\w+)\]\[\w+\]\(C:(-?\d+),S:(-?\d+),E:(-?\d+),T:(-?\d+),D:(-?\d+),N:(-?\d+)\),T\((\d+)\)'), ShowHeatingInfoRiscv),
			(re.compile(r'FUSER_FUNC_ShowHeatingInfo:\d+\((\d+)ms\) : \[(\w+)\]\[\w+\]\(C:(-?\d+),S:(-?\d+),E:(-?\d+),D:(-?\d+),EF:(-?\d+),T:(-?\d+),CP:(-?\d+),SP:(-?\d+),N:(-?\d+)\),T\((\d+)\)'), ShowHeatingInfoRiscvV2),
			(re.compile(r'PRINTER_FUNC_InitDebugLog'), RestartM3),
			(re.compile(r'M31:PRT Clock:'), RestartM3),
			]
	SearchLog(sys.stdin, patterns)
	my_dpi = 96
	plt.figure(figsize=(2048/my_dpi, 1024/my_dpi), dpi=my_dpi)
	plt.plot(timeX, centerY, label='Center')
	plt.plot(timeX, sideY, label='Side')
	plt.plot(timeX, targetY, label='Target')
	if len(envY) > 1 and not np.isnan(envY).all():
		plt.plot(timeX, envY, label='Env')
	if len(DutyY) > 1 and not np.isnan(DutyY).all():
		plt.plot(timeX, DutyY, label='Duty')	
	if len(NipY) > 1 and not np.isnan(NipY).all():
		plt.plot(timeX, NipY, label='Nip')	
		
	plt.legend()
	y_major_locator=MultipleLocator(10)
	ax=plt.gca()	
	#Set y-axis major ticks to multiples of 10
	ax.yaxis.set_major_locator(y_major_locator)
	plt.title("Temperature Curve", fontsize=24)
	plt.xlabel("Time(Sec)", fontsize=14)
	plt.ylabel("Temperature", fontsize=14)
	plt.tick_params(axis='both', labelsize=12, color='red')
	#binding_id = plt.connect('motion_notify_event', on_move)
	plt.connect('button_press_event', on_click)
	plt.savefig('curve.png', bbox_inches='tight')
	if '--show' in sys.argv:
		plt.show()
	else:
		plt.close()
	debugFp.write("max temprature diff:%f line=%d\n" % (_tmpDiff, _tmpDiffLine))
	debugFp.close()