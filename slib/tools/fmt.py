# -*- coding: utf-8 -*-


import datetime


##### Public methods #####
def formatSize(size) :
	if size >= 1073741824 :
		return "%.1f Gb" % (size / 1073741824.0)
	elif size > 1048576 :
		return "%.1f Mb" % (size / 1048576.0)
	elif size > 1024 :
		return "%.1f Kb" % (size / 1024.0)
	else :
		return "%d bytes" % (size)

def formatTimeDelta(time_delta) :
	return str(datetime.timedelta(seconds=time_delta))

