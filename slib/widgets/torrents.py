# -*- coding: utf-8 -*-


import os

from slib import widgetlib
from slib import html
from slib import torrents

from slib import tools
import slib.tools.fmt

from slib import validators
import slib.validators.fs


##### Public methods #####
@widgetlib.provides("torrents_table", "torrents_count", "torrents_size")
@widgetlib.required(css_list=("simple_table.css",))
def torrentsList(torrents_dir_path, link_prefix) :
	torrents_dir_path = validators.fs.validAccessiblePath(torrents_dir_path)
	link_prefix = os.path.normpath(link_prefix)
	size = 0
	rows_list = []
	for (torrent_file_name, meta_dict) in sorted(torrents.torrents(torrents_dir_path).items(), key=( lambda arg : arg[0] )) :
		torrent_file_path = os.path.join(link_prefix, torrent_file_name)
		torrent_size = torrents.torrentSize(meta_dict)
		size += torrent_size
		rows_list.append([
				str(len(rows_list) + 1),
				"<a href=\"%s\">%s</a>" % (os.path.join(link_prefix, torrent_file_name), torrent_file_name),
				tools.fmt.formatSize(torrent_size),
				html.maybeLink(meta_dict.get("comment", ""))
			])
	torrents_table = html.tableWithHeader(["N", "Torrent", "Size", "Comment"], rows_list)
	return (torrents_table, str(len(rows_list)), tools.fmt.formatSize(size))

