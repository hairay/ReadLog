import sys
import re

_lineNum = 0
submit_band_num = 0
received_band_num = 0
phyAddr2Size = {}

def submit_band(m):
	global submit_band_num, received_band_num

	time, count,  phyAddr= m.groups()
	if int(count) == 1:
		phyAddr2Size.clear()
		print("start new band dict( clear %d %d)" % (submit_band_num, received_band_num))
		submit_band_num = received_band_num = 0
	phyAddr2Size[phyAddr] = [phyAddr, count, _lineNum]		
	submit_band_num += 1

def received_band(m):
	global received_band_num
	time, count,  phyAddr= m.groups()
	
	if phyAddr not in phyAddr2Size:
		print("[ %6d ] wrong %s %s %s" % (_lineNum, phyAddr, count, time))
	else:
		del phyAddr2Size[phyAddr]
	received_band_num += 1

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
			(re.compile(r'scan_submit_band.*\(Time:(\d+)\)Submit \((\d+)/\d+\), address=(\w+)'), submit_band),
			(re.compile(r'scan_buf_wait.*\(Time:(\d+)\)Received band (\d+) of \d+, address=(\w+)'), received_band),
			]
		
	SearchLog(sys.stdin, patterns)		
	print("end log dict(%d %d)" % (submit_band_num, received_band_num))