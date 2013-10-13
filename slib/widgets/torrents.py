# -*- coding: utf-8 -*-


import os
import operator
import rtlib.tfile
import ulib.tools.fmt
import ulib.validators.fs

from slib import widgetlib
from slib import html


##### Public methods #####
@widgetlib.provides("torrents_table", "torrents_count", "torrents_size")
@widgetlib.required(css_list=("simple_table.css",))
def torrentsList(torrents_dir_path, link_prefix) :
	torrents_dir_path = ulib.validators.fs.validAccessiblePath(torrents_dir_path)
	link_prefix = os.path.normpath(link_prefix)

	size = 0
	rows_list = []
	for (torrent_file_name, torrent) in sorted(rtlib.tfile.torrents(torrents_dir_path).items(), key=operator.itemgetter(0)) :
		torrent_size = torrent.size()
		size += torrent_size
		rows_list.append([
				str(len(rows_list) + 1),
				"<a href=\"%s\">%s</a>" % (os.path.join(link_prefix, torrent_file_name), torrent_file_name),
				ulib.tools.fmt.formatSize(torrent_size),
				html.maybeLink(torrent.comment() or ""),
			])
	torrents_table = html.tableWithHeader(["N", "Name", "Size", "Comment"], rows_list)

	return (torrents_table, str(len(rows_list)), ulib.tools.fmt.formatSize(size))

