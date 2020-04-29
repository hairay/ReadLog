import sys
import re
import matplotlib.pyplot as plt

_lineNum = 0
_startTime = 0
_header13 = 'time,state,centerHw,centerSw,sideHw,sideSw,targetHw,targetSw,set1,set2,envHw,envSw,set3'
_header14 = 'time,state,centerHw,centerSw,sideHw,sideSw,targetHw,targetSw,set1,set2,set3,envHw,envSw,set4'

timeX = []
centerY = []
sideY = []
targetY = []
envY = []

def AssignVal(m):
	now = float(m.groups(0)[0])/1000.0

	if len(timeX) > 0 and timeX[-1] > now:		 
			return None

	timeX.append(now)
	centerY.append(float(m.groups(0)[3]))
	sideY.append(float(m.groups(0)[5]))
	targetY.append(float(m.groups(0)[7]))
	envY.append(float(m.groups(0)[-2]))	
	#print("%f,%f" % (timeX[-1] , centerY[-1]))	

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

def SearchLog(f, patterns):
	global _lineNum
	for line in f:   
		_lineNum +=1
		for mp in patterns:
			pat, proc = mp
			match_result = pat.search(line)
			if match_result:				
				proc(match_result)

if __name__ == '__main__':	
	patterns = [													
			(re.compile(r'FUSER_FUNC_ShowHeatingInfo:\d+\((\d+)ms\) : \[(\w+)\], \( (\d+), (\d+), (\d+), (\d+), (\d+), (\d+), (\d+), (\d+), (\d+), (\d+), (\d+) \)'), ShowHeatingInfo13),
			(re.compile(r'FUSER_FUNC_ShowHeatingInfo:\d+\((\d+)ms\) : \[(\w+)\], \( (\d+), (\d+), (\d+), (\d+), (\d+), (\d+), (\d+), (\d+), (\d+), (\d+), (\d+), (\d+) \)'), ShowHeatingInfo14),
			]
	SearchLog(sys.stdin, patterns)
	my_dpi = 96
	plt.figure(figsize=(2048/my_dpi, 1024/my_dpi), dpi=my_dpi)
	plt.plot(timeX, centerY, label='Center')
	plt.plot(timeX, sideY, label='Side')
	plt.plot(timeX, targetY, label='Target')
	plt.plot(timeX, envY, label='Env')
	plt.legend()
	plt.title("Temprature Curve", fontsize=24)
	plt.xlabel("Time", fontsize=14)
	plt.ylabel("Temprature", fontsize=14)
	plt.tick_params(axis='both', labelsize=12, color='red')
	#plt.show()
	plt.savefig('curve.png', bbox_inches='tight')     # 存檔
