# -*- coding: utf-8 -*-


import sys
import traceback
import time


##### Public methods #####
def log(message) :
	print >> sys.stderr, message

def attachException(message) :
	message = "----- Error: %s -----\n%s\n-----\n%s" % (time.ctime(), message, traceback.format_exc())
	log(message)

