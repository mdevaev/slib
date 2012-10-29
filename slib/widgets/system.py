# -*- coding: utf-8 -*-


import time

from slib import widgetlib
from slib import html

from slib import tools
import slib.tools.system
import slib.tools.fmt

from slib import validators
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
def disksFree(*args_list) :
	args_list = map(validators.fs.validAccessiblePath, args_list)
	rows_list = []
	for path in args_list :
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

