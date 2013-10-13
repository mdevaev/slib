# -*- coding: utf-8 -*-


import ulib.validatorlib


##### Public methods #####
def validVariableName(arg) :
	return ulib.validatorlib.checkRegexp(arg,
		r"^[a-zA-Z_][a-zA-Z0-9_]*$",
		"variable name",
	)

def validPageName(arg) :
	return ulib.validatorlib.checkRegexp(arg,
		r"^[a-zA-Z0-9_][a-zA-Z0-9_\-]*$",
		"page name",
	)

