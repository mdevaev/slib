# -*- coding: utf-8 -*-


import os
import bencode


##### Public constsnts #####
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

