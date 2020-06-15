import sys
import re

_lineNum = 0
_curTime = 0
phyAddr2Size = {}
virAddr2Size = {}

def MemMgrMalloc(m):	
	phyAddr, size, free = m.groups()
	phyAddr2Size[phyAddr] = size
	

def MemMgrFree(m):	
	phyAddr, size, free = m.groups()
	
	if phyAddr in phyAddr2Size:
		if phyAddr2Size[phyAddr] != size:
			print("[ %6d ] MemMgrFree phyAddr:%s size:%s != original size:%s" % (_lineNum, phyAddr, size, phyAddr2Size[phyAddr]))
		del phyAddr2Size[phyAddr]    
	else:		
		print("[ %6d ] MemMgrFree can't find phyAddr:%s size:%s" % (_lineNum, phyAddr, size))

def PhyMemToVirMem(m):	
	phyAddr, size, virPtr = m.groups()
	virAddr2Size[virPtr] = size
	if phyAddr not in phyAddr2Size:
		print("[ %6d ] PhyMemToVirMem can't find MemMgrMalloc phyAddr:%s size:%s" % (_lineNum, phyAddr, size))

def ReleaseMapVirMem(m):	
	virPtr, size = m.groups()
	
	if virPtr in virAddr2Size:
		if virAddr2Size[virPtr] != size:
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

#MemMgrMalloc Ptr=0xa98e0000 size=4349952 gFreeMemSize=103784448
#MemMgrFree Free Ptr=0xa9d06000 size=4349952 gFreeMemSize=103784448
#__PhyMemToVirMem:0130(Time:7734) : gMiscellaneousThread: phyPtr = 0x80e00000 size=8192 vPtr=0xabb9d000
#ReleaseMapVirMem:0217(Time:47230) : AppCopy_JobTask: vPtr = 0xa92e2000 size=4349952

if __name__ == '__main__':	
	patterns = [						
			(re.compile(r'MemMgrMalloc Ptr=(\w+) size=(\d+) gFreeMemSize=(\d+)'), MemMgrMalloc),
            (re.compile(r'MemMgrFree Free Ptr=(\w+) size=(\d+) gFreeMemSize=(\d+)'), MemMgrFree),	
            (re.compile(r'__PhyMemToVirMem:\d+\(Time:\d+\) : .*phyPtr = (\w+) size=(\d+) vPtr=(\w+)'), PhyMemToVirMem),
            (re.compile(r'ReleaseMapVirMem:\d+\(Time:\d+\) : .*vPtr = (\w+) size=(\d+)'), ReleaseMapVirMem),			
			]
	
	SearchLog(sys.stdin, patterns)
	
	for key, value in phyAddr2Size.items():
		print("need MemMgrFree phyAddr:%s size:%s" % (key, value))

	for key, value in virAddr2Size.items():
		print("need ReleaseMapVirMem virAddr:%s size:%s" % (key, value))    