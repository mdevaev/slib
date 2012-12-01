# -*- coding: utf-8 -*-


import os
import re
import time

from slib import widgetlib

from slib import tools
import slib.tools.coding
import slib.tools.process

from slib import validators
import slib.validators.fs


##### Public methods #####
@widgetlib.provides("mlocate_search", "mlocate_stats", "mlocate_query")
def mlocateSearch(query, remove_prefix, locate_bin_path, db_file_path) :
	query = tools.coding.fromUtf8(query)
	query = re.sub(r"[^\w ]", "", query, flags=re.UNICODE).lower()
	query_list = query.split()
	query = tools.coding.utf8(query)

	remove_prefix = os.path.normpath(remove_prefix) # XXX: Not validate!
	locate_bin_path = validators.fs.validAccessiblePath(locate_bin_path)
	db_file_path = validators.fs.validAccessiblePath(db_file_path)

	if len(query_list) == 0 :
		return ("Empty query string", "", query)

	before_run = time.time()
	search_time = ( lambda : "Search time: %.2f seconds" % (time.time() - before_run) )

	(proc_stdout, proc_stderr, proc_retcode) = tools.process.execProcess([
			locate_bin_path,
			"--database", db_file_path,
			"--all", "--ignore-case",
			"--null", "--quiet",
		] + query_list, fatal_flag=False)

	if proc_retcode != 0 :
		return ("Nothing found", search_time(), query)

	results_list = []
	for path in proc_stdout.strip().split("\0") :
		path_list = path.split(os.path.sep)
		found_dict = dict.fromkeys(query_list, False)
		for index in xrange(len(path_list)) :
			component = tools.coding.fromUtf8(path_list[index]).lower()
			for word in query_list :
				if word in component :
					found_dict[word] = True
			if all(found_dict.values()) :
				result_path = os.path.sep.join(path_list[:index + 1])
				if not result_path in results_list :
					results_list.append(result_path)
				break

	if len(results_list) == 0 :
		return ("Nothing found", search_time(), query)

	for index in xrange(len(results_list)) :
		row = results_list[index]
		row = re.sub("^%s" % (remove_prefix), "", row)
		row = "--- <a href=\"%s\">%s</a>" % (row, row)
		results_list[index] = row
	results = "<br>".join(results_list)

	return (results, search_time(), query)

