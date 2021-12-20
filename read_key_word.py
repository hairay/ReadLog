import sys
import re
import numpy as np

_lineNum = 0

def PrintKeyWord(m):
	print("[ %6d ] %s" % (_lineNum, m),end='')

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
			(re.compile(r'error code|ASSERT|DATA ABORT|ServiceCall|time out'), PrintKeyWord),
			]
	SearchLog(sys.stdin, patterns)

    