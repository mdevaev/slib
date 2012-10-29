# -*- coding: utf-8 -*-


import time
import hashlib
import threading


##### Public methods #####
def uniqueId(salt = "") :
	return hashlib.sha1("%f %d %s" % (time.time(), id(threading.current_thread()), salt)).hexdigest()

def chunks(items_list, chunk_size) :
	return [ items_list[offset:offset+chunk_size] for offset in xrange(0, len(items_list), chunk_size) ]

