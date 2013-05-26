# -*- coding: utf-8 -*-


import helib.validatorlib


##### Public methods #####
def validVariableName(arg) :
	return helib.validatorlib.checkRegexp(arg,
		r"^[a-zA-Z_][a-zA-Z0-9_]*$",
		"variable name",
	)

def validPageName(arg) :
	return helib.validatorlib.checkRegexp(arg,
		r"^[a-zA-Z0-9_][a-zA-Z0-9_\-]*$",
		"page name",
	)

