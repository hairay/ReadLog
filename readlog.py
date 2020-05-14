import sys
import re
import numpy as np

_lineNum = 0
_pageIdTime = np.zeros((256,), dtype=int)
_jobIdTime = np.zeros((256,), dtype=int)
_curJobTime = 0
_curJobId = 0

def GetMsTimeFromStart(curTime, startTime):
	if curTime >= startTime:
		return curTime - startTime
	else:	
		return ( 0xFFFFFFFF - startTime + curTime+1)

def RestartMachine(m):
	global _curJobTime
	global _curJobId

	_curJobTime = 0
	_curJobId = 0	
	print("[%8d][%8d][ %6d ] Machine Start" % (0, 0, _lineNum))

def SysMgrUCO_JobStart(m):	
	global _curJobTime	
	global _curJobId	
	appType, job, time = m.groups()
	time = int(time)
	job = int(job)		
	_curJobTime = time
	diff = 0
	if job:
		_curJobId = job
		diff = GetMsTimeFromStart(time , _jobIdTime[job])
		#_jobIdTime[job] = time	
	print("[%8d][%8d][ %6d ] JobStart for [job:%3d appType:%s]" % (time, diff, _lineNum, job, appType))	
	
def JobMgr_JobStart(m):
	job , appType= m.groups()

	job = int(job)
	if job:
		_jobIdTime[job] = _curJobTime
	print("[%8d][%8d][ %6d ] JobStart OK [job:%3d appType:%s]" % (_curJobTime, 0, _lineNum, job, appType))

def SysMgrUCO_JobAbort(m):		
	appType, job, time = m.groups()
	time = int(time)
	job = int(job)		
	if job:		
		diff = GetMsTimeFromStart(time , _jobIdTime[job])
		print("[%8d][%8d][ %6d ] JobAbort for [job:%3d appType:%s]" % (time, diff, _lineNum, job, appType))	

def SysMgrUCO_JobEnd(m):		
	appType, job, time = m.groups()
	time = int(time)
	job = int(job)		
	if job:		
		diff = GetMsTimeFromStart(time , _jobIdTime[job])
		print("[%8d][%8d][ %6d ] JobEnd for [job:%3d appType:%s]" % (time, diff, _lineNum, job, appType))	

def PrintPaperIn(m):		
	job, id, time = m.groups()
	time = int(time)
	job = int(job)
	id = int(id)
	diff = GetMsTimeFromStart(time , _jobIdTime[job])
	_pageIdTime[id] = _jobIdTime[job]
	print("[%8d][%8d][ %6d ] PaperIn for [job:%3d][id:%3d]" % (time, diff, _lineNum, job, id))	

def PrintPage(m):		
	id, page, time = m.groups()
	time = int(time)	
	id = int(id)
	diff = GetMsTimeFromStart(time , _pageIdTime[id])	
	print("[%8d][%8d][ %6d ] PrintPage for [sizeCode:%s id:%3d]" % (time, diff, _lineNum, page, id))	

def RealProcPageResult(m):
	global _lineNum

	id, result, reason, time = m.groups()
	time = int(time)
	id = int(id)	
	diff = GetMsTimeFromStart(time , _pageIdTime[id])
	print("[%8d][%8d][ %6d ] Finish page [id:%3d result:%s reason:%s]" % (time, diff, _lineNum, id, result, reason))	

def ReportTrayInfo(m):	
	id, exist, time = m.groups()
	time = int(time)
	
	diff = GetMsTimeFromStart(time , _curJobTime)
	print("[%8d][%8d][ %6d ] ReportTrayInfo [tray%s:%s job:%3d]" % (time, diff, _lineNum, id, exist, _curJobId))

def PostActiveTrayErr(m):	
	param2, param3, time = m.groups()
	time = int(time)
	autoSel = (int(param2,16) >> 15) & 0x1
	id = (int(param2,16) >> 16) & 0xFF
	param3 = int(param3,16)
	job = (param3 >> 24) & 0xFF
	paper = (param3 >> 16) & 0xFF
	media = (param3 >> 8) & 0xFF
	diff = GetMsTimeFromStart(time , _jobIdTime[job])
	print("[%8d][%8d][ %6d ] PostActiveTrayErr [tray%1d autoSel:%d paper:%2d media:%2d job:%3d]" % (time, diff, _lineNum, id, autoSel, paper, media, job))

def PostPaperJamErr(m):	
	loc, param3, param4, time = m.groups()
	time = int(time)		
	param3 = int(param3,16)
	job = (param3 >> 16) & 0xFF
	param4 = int(param4,16)
	autoSel = (param4 >> 8) & 0xFF
	paper = (param4) & 0xFF
	id = (param4 >> 16) & 0xFF
	diff = GetMsTimeFromStart(time , _jobIdTime[job])
	print("[%8d][%8d][ %6d ] PostPaperJamErr [tray%1d autoSel:%d paper:%2d loc:%s job:%3d]" % (time, diff, _lineNum, id, autoSel, paper, loc, job))

def PostNoMatchPaper(m):	
	param2, param3, param4, time = m.groups()
	time = int(time)		
	param2 = int(param2,16)
	job = (param2 >> 16) & 0xFF
	id = (param2 >> 8) & 0xFF
	autoSel = (param2) & 0xFF

	param3 = int(param3,16)
	
	paper = (param3 >> 16) & 0xFF
	
	diff = GetMsTimeFromStart(time , _jobIdTime[job])
	print("[%8d][%8d][ %6d ] PostNoMatchPaper [tray%1d autoSel:%d paper:%2d job:%3d]" % (time, diff, _lineNum, id, autoSel, paper, job))

def SysReqPrint(m):	
	reqMsg, param2, param3, param4, time = m.groups()
	time = int(time)	
	
	diff = GetMsTimeFromStart(time , _curJobTime)
	print("[%8d][%8d][ %6d ] SYS_MGR ---> ENG_PRINT %s %s %s %s" % (time, diff, _lineNum, reqMsg, param2, param3, param4))

def PrintErrToSys(m):	
	errMsg, param2, param3, param4, time = m.groups()
	time = int(time)	
	
	diff = GetMsTimeFromStart(time , _curJobTime)
	print("[%8d][%8d][ %6d ] ENG_PRINT ---> SYS_MGR %s %s %s %s" % (time, diff, _lineNum, errMsg, param2, param3, param4))

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
			(re.compile(r'SysMgrUCO_JobStart.*ppType: (\w+),.*ID: (\d+).*Enter Time: (\d+)'), SysMgrUCO_JobStart),
			(re.compile(r'JobMgr_JobStart: add new job: .*ID = (\d+), appType = (\w+)'), JobMgr_JobStart),			
            (re.compile(r'_PrintPaperIn:\d+ : Report ENG_FD jobNum: (\d+), PID: (\d+).*T\((\d+)\)'), PrintPaperIn),
			(re.compile(r'_PrintPage:\d+ :PID: (\d+).*Code: (\d+), T\((\d+)\)'), PrintPage),
			(re.compile(r'_RealProcPageResult:\d+ : .*ID: (\d+),result: (\w+) reason=([-+]?\d+).*T\((\d+)\)'), RealProcPageResult),
			(re.compile(r'SysMgrUCO_JobAbortImpl:\d+ : .*ppType: (\w+).*ID: (\d+).*Enter Time: (\d+)'), SysMgrUCO_JobAbort),
			(re.compile(r'SysMgrUCO_JobEnd:\d+ : .*ppType: (\w+).*ID: (\d+).*Enter Time: (\d+)'), SysMgrUCO_JobEnd),						
			(re.compile(r'ENG_PRINT ---> SYS_MGR.*ERR (\w+)} {(\w+) (\w+) (\w+)} (\d+)'), PrintErrToSys),	
			(re.compile(r'SYS_MGR ---> ENG_PRINT.*REQ (\w+)} {(\w+) (\w+) (\w+)} (\d+)'), SysReqPrint),	
			(re.compile(r'_ReportTrayInfo_:\d+ : tray (\d+).*paper exist: (\d+).*T\((\d+)\)'), ReportTrayInfo),
			(re.compile(r'_PostActiveTrayEr: Post EVENT:    ENG_PRINT ---> SYS_MGR     , {ERR E_ACTIVE_TRAY} {(\w+) (\w+) \w+} (\d+)'), PostActiveTrayErr),
			(re.compile(r'PostJamWithPageS: .*_JAM} {(\w+) (\w+) (\w+)} (\d+)'), PostPaperJamErr),
			(re.compile(r'PostNoMatchPaper: .*_NO_MATCH_PAPER} {(\w+) (\w+) (\w+)} (\d+)'), PostNoMatchPaper),
			(re.compile(r'Main Program Start'), RestartMachine),
			(re.compile(r'DSP_IP_Init'), RestartMachine),
			]
	SearchLog(sys.stdin, patterns)

    