# -*- coding: utf-8 -*-


import re

from . import ValidatorError


##### Public methods #####
def validVariableName(arg) :
	if arg is None :
		raise ValidatorError("Empty argument is not valid variable name")
	arg = str(arg).strip()
	if re.match(r"^[a-zA-Z_][a-zA-Z0-9_]*$", arg) is None :
		raise ValidatorError("Argument \"%s\" is not valid variable name" % (arg))
	return arg

def validPageName(arg) :
	if arg is None :
		raise ValidatorError("Empty argument is not valid page name")
	arg = str(arg).strip()
	if re.match(r"^[a-zA-Z0-9_][a-zA-Z0-9_\-]*$", arg) is None :
		raise ValidatorError("Argument \"%s\" is not valid page name" % (arg))
	return arg

