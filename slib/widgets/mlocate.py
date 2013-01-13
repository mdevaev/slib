# -*- coding: utf-8 -*-


import os
import re
import operator
import time

from slib import widgetlib
from slib import html

from slib import tools
import slib.tools.coding
import slib.tools.process

from slib import validators
import slib.validators.fs


#####
VALID_SYMBOLS = r"[^\w ]"
DELIMITERS = r"[\s\-\.,]"


##### Public methods #####
@widgetlib.provides("mlocate_search", "mlocate_stats", "mlocate_query")
def mlocateSearch(query, remove_prefix, locate_bin_path, db_file_path) :
	query = tools.coding.fromUtf8(query)
	query = re.sub(VALID_SYMBOLS, "", query, flags=re.UNICODE).lower()
	query_list = re.split(DELIMITERS, query)
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

	results_list = mapResults(query_list, proc_stdout.strip().split("\0"))

	if len(results_list) == 0 :
		return ("Nothing found", search_time(), query)

	rows_list = []
	for (count, (row, weight)) in enumerate(results_list) :
		row = re.sub("^%s" % (remove_prefix), "", row)
		row = "<a href=\"%s\">%s</a>" % (row, row)
		rows_list.append((str(count + 1), row, "%.2f" % (weight)))
	results = html.tableWithHeader(("N", "Path", "Weight"), rows_list)

	return (results, search_time(), query)


##### Private #####
def mapResults(query_list, rows_list) :
	results_dict = {}
	for path in rows_list :
		path_list = path.split(os.path.sep)
		found_dict = dict.fromkeys(query_list, False)

		for index in xrange(len(path_list)) :
			component = tools.coding.fromUtf8(path_list[index]).lower()
			for word in query_list :
				if word in component :
					found_dict[word] = True

			if all(found_dict.values()) :
				result_path = os.path.sep.join(path_list[:index + 1])
				weight = calculateWeight(query_list, path_list[index])
				results_dict[result_path] = max(weight, results_dict.get(result_path, 0))
				break

	return sorted(results_dict.items(), key=( lambda arg : -arg[1] ))

def calculateWeight(query_list, file_name) :
	file_name = tools.coding.fromUtf8(file_name).lower()
	without_spaces = re.sub(r"\s", "", file_name)
	weight = 0
	for query in query_list :
		if query in file_name :
			weight += float(len(query)) / float(len(without_spaces))
	return weight

