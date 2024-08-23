import sys
import re

_lineNum = 0
_curTime = 0
phyAddr2Size = {}
virAddr2Size = {}
pipePhyAddr2Size = {}
imageAddr = {}

def ImageOpen(m):
	iAddr= m.groups()		
	if iAddr in imageAddr:
		print("[ %6d ] ImageOpen use same Addr:%s %s" % (_lineNum, iAddr))
	else:	
		imageAddr[iAddr] = [_lineNum]
	
def ImageClose(m):
	iAddr= m.groups()	
	if iAddr in imageAddr:
		del imageAddr[iAddr]
	else:	
		print("[ %6d ] ImageClose can't fine Addr:%s" % (_lineNum, iAddr))

def SearchPipePhyMem(addr, size):
	for key, value in pipePhyAddr2Size.items():
		start = int(key, 16)
		end = start + int(value[0])
		if addr >= start and (addr+size) <= end:
			return 1
	return 0

def IPMallocPhy(m):
	virPtr, size,  phyAddr= m.groups()
	pipePhyAddr2Size[phyAddr] = [size, _lineNum]
	virAddr2Size[virPtr] = [size, _lineNum]

def MemMgrMalloc(m):
	phyAddr, size = m.groups()
	phyAddr2Size[phyAddr] = [size, _lineNum]

def PipeMemMgrMalloc(m):
	phyAddr, size = m.groups()
	pipePhyAddr2Size[phyAddr] = [size, _lineNum]

def MemMgrFree(m):	
	phyAddr, size = m.groups()
	
	if phyAddr in pipePhyAddr2Size:
		if pipePhyAddr2Size[phyAddr][0] != size:
			print("[ %6d ] MemMgrFree phyAddr:%s size:%s != original size:%s" % (_lineNum, phyAddr, size, pipePhyAddr2Size[phyAddr]))
		del pipePhyAddr2Size[phyAddr]
		return

	if phyAddr in phyAddr2Size:
		if phyAddr2Size[phyAddr][0] != size:
			print("[ %6d ] MemMgrFree phyAddr:%s size:%s != original size:%s" % (_lineNum, phyAddr, size, phyAddr2Size[phyAddr]))
		del phyAddr2Size[phyAddr]    
	else:		
		print("[ %6d ] MemMgrFree can't find phyAddr:%s size:%s" % (_lineNum, phyAddr, size))

def PhyMemToVirMem(m):	
	phyAddr, size, virPtr = m.groups()
	virAddr2Size[virPtr] = [size, _lineNum]

	if SearchPipePhyMem(int(phyAddr,16), int(size)) == 1:
		return
	if phyAddr not in phyAddr2Size:
		if int(phyAddr,16) >= 0x80000000:
			print("[ %6d ] PhyMemToVirMem can't find MemMgrMalloc phyAddr:%s size:%s virPtr:%s" % (_lineNum, phyAddr, size, virPtr))
	elif int(phyAddr2Size[phyAddr][0]) < int(size):
		print("[ %6d ] PhyMemToVirMem phyAddr:%s size:%s > original size:%s" % (_lineNum, phyAddr, size, phyAddr2Size[phyAddr]))

def FileToVirMem(m):	
	virPtr, size = m.groups()
	virAddr2Size[virPtr] = [size, _lineNum]
	
def QuasarPhyMemToVirMem(m):	
	virPtr, size, phyAddr = m.groups()
	virAddr2Size[virPtr] = [size, _lineNum]

	if SearchPipePhyMem(int(phyAddr,16), int(size)) == 1:
		return
	if phyAddr not in phyAddr2Size:
		if int(phyAddr, 16) >= 0x80000000:
			print("[ %6d ] PhyMemToVirMem can't find MemMgrMalloc phyAddr:%s size:%s virPtr:%s" % (_lineNum, phyAddr, size, virPtr))
	elif int(phyAddr2Size[phyAddr][0]) < int(size):
		print("[ %6d ] PhyMemToVirMem phyAddr:%s size:%s > original size:%s" % (_lineNum, phyAddr, size, phyAddr2Size[phyAddr]))

def InvadateCache(m):	
	phyAddr, size = m.groups()	

	if SearchPipePhyMem(int(phyAddr,16), int(size)) == 1:
		return
	if phyAddr not in phyAddr2Size:
		print("[ %6d ] InvadateCache can't find MemMgrMalloc phyAddr:%s size:%s" % (_lineNum, phyAddr, size))
	elif int(phyAddr2Size[phyAddr][0]) < int(size):
		print("[ %6d ] InvadateCache phyAddr:%s size:%s != original size:%s" % (_lineNum, phyAddr, size, phyAddr2Size[phyAddr]))

def FlushCache(m):	
	phyAddr, size = m.groups()

	if SearchPipePhyMem(int(phyAddr,16), int(size)) == 1:
		return	
	if phyAddr not in phyAddr2Size:
		print("[ %6d ] FlushCache can't find MemMgrMalloc phyAddr:%s size:%s" % (_lineNum, phyAddr, size))
	elif int(phyAddr2Size[phyAddr][0]) < int(size):
		print("[ %6d ] FlushCache phyAddr:%s size:%s != original size:%s" % (_lineNum, phyAddr, size, phyAddr2Size[phyAddr]))

def ReleaseMapVirMem(m):	
	virPtr, size = m.groups()
		
	if virPtr in virAddr2Size:
		if virAddr2Size[virPtr][0] != size and virAddr2Size[virPtr][0] != 0:
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
			(re.compile(r'IPMallocPhys.* mmap addr=(\w+) size=(\d+) phyAddr=(\w+)'), IPMallocPhy),
			(re.compile(r'IImemAllocateSPMEM.* mmap addr=(\w+) size=(\d+) phyAddr=(\w+)'), IPMallocPhy),
			(re.compile(r'IImemAddPool Ptr=(\w+) size=(\d+)'), PipeMemMgrMalloc),
            (re.compile(r'MemMgrFree Free Ptr=(\w+) size=(\d+) gFreeMemSize=\d+'), MemMgrFree),
			(re.compile(r'IImemFreePool Free Ptr=(\w+) size=(\d+)'), MemMgrFree),
            (re.compile(r'__PhyMemToVirMem:\d+\(Time:\d+\) : .*phyPtr = (\w+) size=(\d+) vPtr=(\w+)'), PhyMemToVirMem),
            (re.compile(r'NotifyFileToHost:\d+ : mmap addr=(\w+) size=(\d+)'), FileToVirMem),
			(re.compile(r'mmap addr=(\w+) size=(\d+) phyAddr=(\w+)'), QuasarPhyMemToVirMem),
			(re.compile(r'InvadateCache:\d+\(Time:\d+\) : .*phyPtr = (\w+) size=(\d+)'), InvadateCache),
			(re.compile(r'MemMgrInvadateCache:\d+\(Time:\d+\) : .*phyPtr = (\w+) size=(\d+)'), InvadateCache),
			(re.compile(r'FlushCache:\d+\(Time:\d+\) : .*phyPtr = (\w+) size=(\d+)'), FlushCache),
			(re.compile(r'MemMgrFlushCache:\d+\(Time:\d+\) : .*phyPtr = (\w+) size=(\d+)'), FlushCache),
            (re.compile(r'ReleaseMapVirMem:\d+\(Time:\d+\) : .*vPtr = (\w+) size=(\d+)'), ReleaseMapVirMem),
			(re.compile(r'munmap addr=(\w+) size=(\d+)'), ReleaseMapVirMem),
			(re.compile(r'IMAGEopenD.*: (\w+)'), ImageOpen),
			(re.compile(r'IMAGEcloseD.*: (\w+)'), ImageClose),
			]
	
	pipePhyAddr2Size["0x88000000"] = ["6291456", 0]
	pipePhyAddr2Size["0x88600000"] = ["6291456", 0]

	SearchLog(sys.stdin, patterns)
	del pipePhyAddr2Size["0x88000000"]
	del pipePhyAddr2Size["0x88600000"]

	for key, value in phyAddr2Size.items():
		print("need MemMgrFree phyAddr:%s size:%s" % (key, value))

	for key, value in virAddr2Size.items():
		print("need ReleaseMapVirMem virAddr:%s size:%s" % (key, value))

	for key, value in pipePhyAddr2Size.items():
		print("need IImemFreePool phyAddr:%s size:%s" % (key, value))
