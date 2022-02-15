import sys
import re

_lineNum = 0

def PrintKeyWord(allLine):
	print("[ %6d ] %s" % (_lineNum, allLine),end='')

def SearchLog(f, patterns):
	global _lineNum
	for line in f:   
		_lineNum +=1
		for mp in patterns:
			pat, proc = mp
			match_result = pat.search(line)
			if match_result:				
				proc(line)

if __name__ == '__main__':	
	patterns = [												
			(re.compile(r'error code|ALERT:'), PrintKeyWord),
			(re.compile(r'osAssertCalled|ASSERT'), PrintKeyWord),
			(re.compile(r'DATA ABORT|HardFault|SIGTERM|SIGINT'), PrintKeyWord),
			(re.compile(r'ServiceCall|service call|wServiceCallError'), PrintKeyWord),
			(re.compile(r'time out .*error'), PrintKeyWord),
			(re.compile(r'SysErrInfo_GetErrNum'), PrintKeyWord),
			(re.compile(r'Report engine Error state'), PrintKeyWord),
			(re.compile(r'fail_ap.log'), PrintKeyWord),						
			]
	SearchLog(sys.stdin, patterns)

    