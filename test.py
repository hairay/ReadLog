import re

def RealProcPageResult(m):    
	print(m.groups())	

def SearchLog(line, patterns):    			
		for mp in patterns:
			pat, proc = mp
			match_result = pat.search(line)
			if match_result:				
				proc(match_result)

input = {'[80000000][M3P_CMD]JOB_FUNC_ParserPrintFlow:0546(23912ms) : CmdGet : CmdId=0x4000000, CMD_ID_PRE_FUSING',
'[80000000][M3P_CMD]JOB_FUNC_ParserPrintFlow:0546(23912ms) : CmdGet : CmdId=0x4000000, CMD_ID_PRE_FUSING',			
}

if __name__ == '__main__':	
	patterns = [														
            (re.compile(r'JOB_FUNC_ParserPrintFlow:\d+\((\d+)ms\) : CmdGet : CmdId=\w+, (\w+)'), RealProcPageResult),	
			]
	for str in 	input:		
		SearchLog(str, patterns)
    
