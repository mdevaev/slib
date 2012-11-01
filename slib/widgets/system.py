# -*- coding: utf-8 -*-


import os
import time

from slib import widgetlib
from slib import html

from slib import tools
import slib.tools.system
import slib.tools.fmt

from slib import validators
import slib.validators.common
import slib.validators.fs


##### Public methods #####
@widgetlib.provides("server_status_table")
@widgetlib.required(css_list=("simple_table.css",))
def serverStatus() :
	server_status = html.statusTable([
			("Now", time.ctime()),
			("Uptime", tools.fmt.formatTimeDelta(tools.system.uptime())),
			("Load average", ", ".join(map(str, tools.system.loadAverage())))
		])
	return (server_status,)

@widgetlib.provides("server_df_table")
@widgetlib.required(css_list=("simple_table.css", "progress_bar.css"))
def disksFree(dirs_list) :
	dirs_list = map(validators.fs.validAccessiblePath, validators.common.validStringList(dirs_list))
	rows_list = []
	for path in dirs_list :
		label = ( os.path.basename(path) or path )
		(full, used) = tools.system.diskFree(path)
		percent = 100 * used / full
		rows_list.append([
				label,
				{ "style" : "width: 70%", "body" : html.progressBar(percent) },
				tools.fmt.formatSize(used),
				tools.fmt.formatSize(full),
				tools.fmt.formatSize(full - used)
			])
	df_table = html.tableWithHeader(["Label", "", "Size", "Used", "Free"], rows_list)
	return (df_table,)

