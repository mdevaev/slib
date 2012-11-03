# -*- coding: utf-8 -*-


import ConfigParser

from slib import widgetlib
from slib import html

from slib import tools
import slib.tools.fmt

from slib import validators
import slib.validators.fs


##### Public constants #####
BERSERK_LEVELS_MAP = {
	"MeleeDamageStat" : (0, 25000, 100000, 500000, 1500000, 3500000, 5500000),
}
SHARPSHOOTER_LEVELS_MAP = {
	"HeadshotKillsStat" : (0, 30, 100, 700, 2500, 5500, 8500),
}
FIREBUG_LEVELS_MAP = {
	"FlameThrowerDamageStat" : (0, 25000, 100000, 500000, 1500000, 3500000, 5500000),
}
FIELD_MEDIC_LEVELS_MAP = {
	"DamageHealedStat" : (0, 200, 750, 4000, 12000, 25000, 100000),
}
DEMOLITIONS_LEVELS_MAP = {
	"ExplosivesDamageStat" : (0, 25000, 100000, 500000, 1500000, 3500000, 5500000),
}
SUPPORT_SPEC_LEVELS_MAP = {
	"WeldingPointsStat" : (0, 2000, 7000, 35000, 120000, 250000, 370000),
	"ShotgunDamageStat" : (0, 25000, 100000, 500000, 1500000, 3500000, 5500000),
}
COMMANDO_LEVELS_MAP = {
	"StalkerKillsStat" : (0, 30, 100, 350, 1200, 2400, 3600),
	"BullpupDamageStat" : (0, 25000, 100000, 500000, 1500000, 3500000, 5500000),
}


##### Public methods #####
@widgetlib.provides("kf_leaderboard_table", "kf_perks_table")
@widgetlib.required(css_list=("simple_table.css", "progress_bar.css"))
def kfStatistics(config_file_path, profile_url) :
	config_file_path = validators.fs.validAccessiblePath(config_file_path)
	# FIXME: No validation for profile url!

	stat_dict = serverPerksStat(config_file_path)

	count = 1
	leaderboard_list = []
	for (user_id, player_stat_dict) in sorted(stat_dict.items(), key=( lambda arg : -arg[1]["KillsStat"])) :
		leaderboard_list.append([
				str(count),
				{ "nowrap" : None, "body" : player_stat_dict["PlayerName"] },
				str(player_stat_dict["KillsStat"]),
				tools.fmt.formatTimeDelta(player_stat_dict["TotalPlayTime"])
			])
		if count == 5 :
			break
		count += 1
	leaderboard_table = html.tableWithHeader(["N", "Name", "Kills", "Time"], leaderboard_list)

	count = 1
	players_list = []
	for (user_id, player_stat_dict) in sorted(stat_dict.items(), key=( lambda arg : arg[1]["PlayerName"].lower() )) :
		perk_progress = ( lambda levels_map : { "width" : "13%", "body" : html.progressBar(calculateProgress(levels_map, player_stat_dict)) } )
		player_name = "<a href=\"%s\">&raquo;</a>&nbsp;%s" % (profile_url % { "user_id" : user_id }, player_stat_dict["PlayerName"])
		players_list.append([
				str(count),
				{ "nowrap" : None, "body" : player_name },
				perk_progress(BERSERK_LEVELS_MAP),
				perk_progress(SHARPSHOOTER_LEVELS_MAP),
				perk_progress(FIREBUG_LEVELS_MAP),
				perk_progress(FIELD_MEDIC_LEVELS_MAP),
				perk_progress(DEMOLITIONS_LEVELS_MAP),
				perk_progress(SUPPORT_SPEC_LEVELS_MAP),
				perk_progress(COMMANDO_LEVELS_MAP),
			])
		count += 1

	players_header_list = ["N", "Name", "Berserk", "Sharpshooter", "Firebug", "FieldMedic", "Demolitions", "SupportSpec", "Commando"]
	players_table = html.tableWithHeader(players_header_list, players_list)

	return (leaderboard_table, players_table)


@widgetlib.provides("kf_player_stat_table")
@widgetlib.required(css_list=("simple_table.css", "progress_bar.css"))
def kfPlayerStatistics(user_id, config_file_path) :
	user_id = validators.common.validNumber(user_id, 1)
	config_file_path = validators.fs.validAccessiblePath(config_file_path)

	stat_dict = serverPerksStat(config_file_path)
	if not user_id in stat_dict :
		raise RuntimeError("Invalid Steam ID")
	stat_dict = stat_dict[user_id]

	wins = stat_dict["WinsCount"]
	losts = stat_dict["LostsCount"]
	battles = wins + losts
	kills = stat_dict["KillsStat"]
	efficiency = float(kills) / float(battles)
	skill_factor = float(wins) / float(battles)

	skill_factor_text = ( """
			<div style="float:left; text-align:left;">%.2f&nbsp;</div>
			<div style="float:right; text-align:right; width:100px">%s</div>
		""" % (skill_factor, html.progressBar(skill_factor * 100)) )

	player_stat_table = html.statusTable([
			("Battles", str(battles)),
			("Wins", str(wins)),
			("Losts", str(losts)),
			("Skill factor", skill_factor_text),
			("Efficiency", "%2.f" % (efficiency)),
			("Last hope", str(stat_dict["SoleSurvivorWavesStat"])),
			("Kills", str(kills)),
			("Time played", tools.fmt.formatTimeDelta(stat_dict["TotalPlayTime"])),
			#map(str, calculateLevelProgress(BERSERK_LEVELS_MAP, stat_dict)),
			#map(str, calculateLevelProgress(SHARPSHOOTER_LEVELS_MAP, stat_dict)),
			#map(str, calculateLevelProgress(FIREBUG_LEVELS_MAP, stat_dict)),
			#map(str, calculateLevelProgress(FIELD_MEDIC_LEVELS_MAP, stat_dict)),
			#map(str, calculateLevelProgress(DEMOLITIONS_LEVELS_MAP, stat_dict)),
			#map(str, calculateLevelProgress(SUPPORT_SPEC_LEVELS_MAP, stat_dict)),
			#map(str, calculateLevelProgress(COMMANDO_LEVELS_MAP, stat_dict)),
		])

	return (player_stat_table,)


##### Private methods #####
def serverPerksStat(config_file_path) :
	config = ConfigParser.ConfigParser()
	config.optionxform = str
	config.read(config_file_path)

	stat_dict = {}
	for section in config.sections() :
		user_id = int(section.split()[0]) + 76561197960265728 # XXX: Fucking linux magic
		stat_dict[user_id] = {}
		for option in config.options(section) :
			value = config.get(section, option)
			try :
				value = int(value)
			except ValueError : pass
			stat_dict[user_id][option] = value

	return stat_dict

def calculateProgress(levels_map, stat_dict) :
	percent = 0
	for (key, levels_list) in levels_map.iteritems() :
		percent += min(100 * stat_dict[key] / levels_list[-1], 100)
	return percent / len(levels_map)

def calculateLevelProgress(levels_map, stat_dict) :
	percent = 0
	result_level = max_level = len(levels_map.values()[0]) -1
	for (key, levels_list) in levels_map.iteritems() :
		for level in range(len(levels_list) - 1, -1, -1) :
			if stat_dict[key] >= levels_list[level] :
				result_level = min(level, result_level)
				for_next_level = levels_list[( level + 1 if level < max_level else max_level )]
				percent += min(100 * stat_dict[key] / for_next_level, 100)
				break
	return (result_level, percent / len(levels_map))

