# -*- coding: utf-8 -*-


import ConfigParser

from slib import widgetlib
from slib import html

from slib import tools
import slib.tools.fmt

from slib import validators
import slib.validators.fs


##### Public methods #####
@widgetlib.provides("kf_leaderboard_table", "kf_perks_table")
@widgetlib.required(css_list=("simple_table.css", "progress_bar.css", "script.css"), js_list=("spoiler.js",))
def kfStatistics(config_file_path) :
	config_file_path = validators.fs.validAccessiblePath(config_file_path)

	config = ConfigParser.ConfigParser()
	config.optionxform = str
	config.read(config_file_path)
	stat_dict = {}
	for section in config.sections() :
		player_name = config.get(section, "PlayerName")
		stat_dict[player_name] = {}
		for option in config.options(section) :
			value = config.get(section, option)
			try :
				value = int(value)
			except ValueError : pass
			stat_dict[player_name][option] = value

	count = 1
	leaderboard_list = []
	for (player_name, player_stat_dict) in sorted(stat_dict.items(), key=( lambda arg : -arg[1]["KillsStat"])) :
		leaderboard_list.append([
				str(count),
				{ "nowrap" : None, "body" : player_name },
				str(player_stat_dict["KillsStat"]),
				tools.fmt.formatTimeDelta(player_stat_dict["TotalPlayTime"])
			])
		if count == 5 :
			break
		count += 1
	leaderboard_table = html.tableWithHeader(["N", "Name", "Kills", "Time"], leaderboard_list)

	count = 1
	players_list = []
	for (player_name, player_stat_dict) in sorted(stat_dict.items(), key=( lambda arg : arg[0].lower() )) :
		perk_percent = ( lambda option, limit : min(100 * player_stat_dict[option] / limit, 100) )
		perk_progress = ( lambda percent : { "width" : "13%", "body" : html.progressBar(percent) } )

		stat_table = html.statusTable([
				("Kills", str(player_stat_dict["KillsStat"])),
				("Time", tools.fmt.formatTimeDelta(player_stat_dict["TotalPlayTime"]))
			])
		(stat_spoiler_div_id, spoiler_title) = html.spoilerTitle("&raquo;")
		stat_spoiler = html.spoilerBody(stat_spoiler_div_id, "<br>"+stat_table)

		berserk = perk_percent("MeleeDamageStat", 5500000)
		sharpshooter = perk_percent("HeadshotKillsStat", 8500)
		firebug = perk_percent("FlameThrowerDamageStat", 5500000)
		field_medic = perk_percent("DamageHealedStat", 100000)
		demolitions = perk_percent("ExplosivesDamageStat", 5500000)
		support_spec = (perk_percent("WeldingPointsStat", 370000) + perk_percent("ShotgunDamageStat", 5500000)) / 2
		commando = (perk_percent("StalkerKillsStat", 3600) + perk_percent("BullpupDamageStat", 5500000)) / 2

		players_list.append([
				str(count),
				{ "nowrap" : None, "body" : "%s %s%s" % (spoiler_title, player_name, stat_spoiler) },
				perk_progress(berserk),
				perk_progress(sharpshooter),
				perk_progress(firebug),
				perk_progress(field_medic),
				perk_progress(demolitions),
				perk_progress(support_spec),
				perk_progress(commando)
			])
		count += 1

	players_header_list = ["N", "Name", "Berserk", "Sharpshooter", "Firebug", "FieldMedic", "Demolitions", "SupportSpec", "Commando"]
	players_table = html.tableWithHeader(players_header_list, players_list)

	return (leaderboard_table, players_table)

