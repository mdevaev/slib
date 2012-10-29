# -*- coding: utf-8 -*-


import SourceLib

from slib import widgetlib
from slib import html

from slib import tools
import slib.tools.fmt

from slib import validators
import slib.validators.network


##### Public methods #####
@widgetlib.provides("source_players_table", "source_status_table")
@widgetlib.required(css_list=("simple_table.css",))
def sourceServerStatus(host_name, port) :
	host_name = validators.network.validHostName(host_name)
	port = validators.network.validPort(port)

	server = SourceLib.SourceQuery.SourceQuery(host_name, port)

	count = 1
	players_list = []
	for player_dict in server.player() :
		players_list.append([
				str(count),
				{ "nowrap" : None, "body" : player_dict["name"] },
				tools.fmt.formatTimeDelta(player_dict["time"]),
				str(player_dict["kills"])
			])
		count += 1
	players_table = html.tableWithHeader(["N", "Name", "Time", "Score"], players_list)

	info_dict = server.info()
	status_table = html.statusTable([
			("Server", info_dict["hostname"]),
			("Description", info_dict["gamedesc"]),
			("Game", info_dict["gamedir"]),
			("Map", info_dict["map"]),
			("Players", "%d / %d" % (info_dict["numplayers"], info_dict["maxplayers"])),
			("Password", ( "Yes" if info_dict["passworded"] else "No" )),
			("Secure", ( "Yes" if info_dict["secure"] else "No" )),
			("Version", info_dict["version"])
		])
	return (players_table, status_table)

@widgetlib.provides("source_players_number")
def sourcePlayersNumber(host_name, port) :
	host_name = validators.network.validHostName(host_name)
	port = validators.network.validPort(port)
	server = SourceLib.SourceQuery.SourceQuery(host_name, port)
	info_dict = server.info()
	return ("%d / %d" % (info_dict["numplayers"], info_dict["maxplayers"]),)

