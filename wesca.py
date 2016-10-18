#!/usr/bin/env python
# -*- coding: utf-8 -*-


import app.core

import sys  


reload(sys)  
sys.setdefaultencoding('utf8')


#-----------------------------------------------------------------------

def getInputs():
	
	inputs = {"commands":[], "args":{}}
	
	for arg in sys.argv:
		
		if arg[:2] == "--":
			inputs["commands"].append(arg[2:])

		if arg[:1] == "-" and inputs["commands"].count(arg[2:])==0:
			values = arg[1:].split("=")
			inputs["args"][values[0]] = values[1]
			
	return inputs


########################################################################

if __name__ == "__main__":

	inputs = getInputs()
	
	wesca = app.core.Core()
	wesca.start(inputs)
			
	

########################################################################


