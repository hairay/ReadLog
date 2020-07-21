import sys
import re

_lineNum = 0
_curTime = 0
phyAddr2Size = {}
virAddr2Size = {}

def MemMgrMalloc(m):	
	phyAddr, size = m.groups()
	phyAddr2Size[phyAddr] = [size, _lineNum]
	

def MemMgrFree(m):	
	phyAddr, size = m.groups()
	
	if phyAddr in phyAddr2Size:
		if phyAddr2Size[phyAddr][0] != size:
			print("[ %6d ] MemMgrFree phyAddr:%s size:%s != original size:%s" % (_lineNum, phyAddr, size, phyAddr2Size[phyAddr]))
		del phyAddr2Size[phyAddr]    
	else:		
		print("[ %6d ] MemMgrFree can't find phyAddr:%s size:%s" % (_lineNum, phyAddr, size))

def PhyMemToVirMem(m):	
	phyAddr, size, virPtr = m.groups()
	virAddr2Size[virPtr] = [size, _lineNum]
	if phyAddr not in phyAddr2Size:
		print("[ %6d ] PhyMemToVirMem can't find MemMgrMalloc phyAddr:%s size:%s virPtr:%s" % (_lineNum, phyAddr, size, virPtr))
	elif phyAddr2Size[phyAddr][0] != size:
		print("[ %6d ] PhyMemToVirMem phyAddr:%s size:%s != original size:%s" % (_lineNum, phyAddr, size, phyAddr2Size[phyAddr]))

def InvadateCache(m):	
	phyAddr, size = m.groups()	
	if phyAddr not in phyAddr2Size:
		print("[ %6d ] InvadateCache can't find MemMgrMalloc phyAddr:%s size:%s" % (_lineNum, phyAddr, size))
	elif phyAddr2Size[phyAddr][0] != size:
		print("[ %6d ] InvadateCache phyAddr:%s size:%s != original size:%s" % (_lineNum, phyAddr, size, phyAddr2Size[phyAddr]))

def FlushCache(m):	
	phyAddr, size = m.groups()	
	if phyAddr not in phyAddr2Size:
		print("[ %6d ] FlushCache can't find MemMgrMalloc phyAddr:%s size:%s" % (_lineNum, phyAddr, size))
	elif phyAddr2Size[phyAddr][0] != size:
		print("[ %6d ] FlushCache phyAddr:%s size:%s != original size:%s" % (_lineNum, phyAddr, size, phyAddr2Size[phyAddr]))

def ReleaseMapVirMem(m):	
	virPtr, size = m.groups()
	
	if virPtr in virAddr2Size:
		if virAddr2Size[virPtr][0] != size:
			print("[ %6d ] ReleaseMapVirMem virAddr:%s size:%s != original size:%s" % (_lineNum, virPtr, size, virAddr2Size[virPtr]))
		del virAddr2Size[virPtr]    
	else:		
		print("[ %6d ] ReleaseMapVirMem can't find virPtr:%s size:%s" % (_lineNum, virPtr, size))

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
			(re.compile(r'MemMgrMalloc Ptr=(\w+) size=(\d+) gFreeMemSize=\d+'), MemMgrMalloc),
            (re.compile(r'MemMgrFree Free Ptr=(\w+) size=(\d+) gFreeMemSize=\d+'), MemMgrFree),	
            (re.compile(r'__PhyMemToVirMem:\d+\(Time:\d+\) : .*phyPtr = (\w+) size=(\d+) vPtr=(\w+)'), PhyMemToVirMem),
			(re.compile(r'InvadateCache:\d+\(Time:\d+\) : .*phyPtr = (\w+) size=(\d+)'), InvadateCache),
			(re.compile(r'FlushCache:\d+\(Time:\d+\) : .*phyPtr = (\w+) size=(\d+)'), FlushCache),
            (re.compile(r'ReleaseMapVirMem:\d+\(Time:\d+\) : .*vPtr = (\w+) size=(\d+)'), ReleaseMapVirMem),			
			]
	
	SearchLog(sys.stdin, patterns)
	
	for key, value in phyAddr2Size.items():
		print("need MemMgrFree phyAddr:%s size:%s" % (key, value))

	for key, value in virAddr2Size.items():
		print("need ReleaseMapVirMem virAddr:%s size:%s" % (key, value))    