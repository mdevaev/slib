# -*- coding: utf-8 -*-


import os
import time
import helib.tools.fmt
import helib.tools.unix
import helib.validators.common
import helib.validators.fs

from slib import widgetlib
from slib import html


##### Public methods #####
@widgetlib.provides("server_status_table")
@widgetlib.required(css_list=("simple_table.css",))
def serverStatus() :
	server_status = html.statusTable([
			("Now", time.ctime()),
			("Uptime", helib.tools.fmt.formatTimeDelta(helib.tools.unix.uptime())),
			("Load average", ", ".join(map(str, helib.tools.unix.loadAverage())))
		])
	return (server_status,)

@widgetlib.provides("server_df_table")
@widgetlib.required(css_list=("simple_table.css", "progress_bar.css"))
def disksFree(dirs_list) :
	dirs_list = map(helib.validators.fs.validAccessiblePath, helib.validators.common.validStringList(dirs_list))
	rows_list = []
	for path in dirs_list :
		label = ( os.path.basename(path) or path )
		(full, used) = helib.tools.unix.diskFree(path)
		percent = 100 * used / full
		rows_list.append([
				{ "nowrap" : None, "body" : label },
				{ "style" : "width: 70%", "body" : html.progressBar(percent) },
				{ "nowrap" : None, "body" : helib.tools.fmt.formatSize(full) },
				{ "nowrap" : None, "body" : helib.tools.fmt.formatSize(used) },
				{ "nowrap" : None, "body" : helib.tools.fmt.formatSize(full - used) },
			])
	df_table = html.tableWithHeader(["Label", "", "Size", "Used", "Free"], rows_list)
	return (df_table,)

