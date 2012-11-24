# -*- coding: utf-8 -*-


import os
import bencode
import operator

from slib import widgetlib
from slib import html

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
	for (torrent_file_name, meta_dict) in sorted(torrents(torrents_dir_path).items(), key=operator.itemgetter(0)) :
		torrent_file_path = os.path.join(link_prefix, torrent_file_name)
		torrent_size = torrentSize(meta_dict)
		size += torrent_size
		rows_list.append([
				str(len(rows_list) + 1),
				"<a href=\"%s\">%s</a>" % (os.path.join(link_prefix, torrent_file_name), torrent_file_name),
				tools.fmt.formatSize(torrent_size),
				html.maybeLink(meta_dict.get("comment", ""))
			])
	torrents_table = html.tableWithHeader(["N", "Torrent", "Size", "Comment"], rows_list)
	return (torrents_table, str(len(rows_list)), tools.fmt.formatSize(size))


##### Private methods #####
def torrents(torrents_dir_path) :
	torrents_dict = {}
	for torrent_file_name in filter(lambda name : name.endswith(".torrent"), os.listdir(torrents_dir_path)) :
		with open(os.path.join(torrents_dir_path, torrent_file_name)) as torrent_file :
			torrents_dict[torrent_file_name] = bencode.bdecode(torrent_file.read())
	return torrents_dict

def torrentSize(meta_dict) :
	if meta_dict["info"].has_key("length") :
		return meta_dict["info"]["length"]
	elif meta_dict["info"].has_key("files") :
		size = 0
		for part_dict in meta_dict["info"]["files"] :
			size += part_dict["length"]
		return size
	else :
		return -1

