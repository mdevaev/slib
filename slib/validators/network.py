# -*- coding: utf-8 -*-


import re

from . import ValidatorError


##### Public methods #####
def validHostName(arg) : # XXX: Not RFC! Include "_" character and allow "-" in the beggining of chunk.
	if arg is None :
		raise ValidatorError("Empty argument is not valid hostname")
	arg = str(arg).strip()
	if re.match(r"^(([a-zA-Z0-9]|[-a-zA-Z0-9][\w\-]*[a-zA-Z0-9])\.)*([a-zA-Z0-9]|[-a-zA-Z0-9][\w\-]*[a-zA-Z0-9])$", arg) is None :
		raise ValidatorError("Argument \"%s\" is not valid hostname" % (arg))
	return arg

def validPort(arg) :
	if arg is None :
		raise ValidatorError("Empty is not valid TCP/UDP portnumber")
	try :
		arg = int(arg)
	except Exception :
		raise ValidatorError("Argument \"%s\" is not valid TCP/UDP portnumber" % (str(arg)))
	if not (0 <= arg < 65536) :
		raise ValidatorError("Argument \"%d\" is not valid TCP/UDP portnumber" % (arg))
	return arg

