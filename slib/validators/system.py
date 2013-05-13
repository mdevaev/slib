# -*- coding: utf-8 -*-


from slib import validatorlib


##### Public methods #####
def validVariableName(arg) :
	return validatorlib.checkRegexp(arg,
		r"^[a-zA-Z_][a-zA-Z0-9_]*$",
		"variable name",
	)

def validPageName(arg) :
	return validatorlib.checkRegexp(arg,
		r"^[a-zA-Z0-9_][a-zA-Z0-9_\-]*$",
		"page name",
	)

