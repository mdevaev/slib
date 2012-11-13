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


RANKS_LIST = (
	(0, "Private"),
	(5, "Junior Lieutenant"),
	(10, "Lieutenant"),
	(20, "Senior Lieutenant"),
	(30, "Captain"),
	(40, "Major"),
	(50, "Lieutenant Colonel"),
	(60, "Colonel"),
	(70, "Major General"),
	(80, "Lieutenant General"),
	(90, "Colonel General"),
	(100, "General of the Army"),
	(200, "Marshal"),
)

##### Public methods #####
@widgetlib.provides("kf_leaderboard_table", "kf_perks_table")
@widgetlib.required(css_list=("simple_table.css", "progress_bar.css"))
def kfStatistics(config_file_path, profile_url) :
	config_file_path = validators.fs.validAccessiblePath(config_file_path)
	# FIXME: No validation for profile url!

	stat_dict = serverPerksStat(config_file_path)

	return (
		serverLeaderboardTable(stat_dict),
		serverPerksTable(stat_dict, profile_url),
	)


@widgetlib.provides("kf_player_stat_table", "kf_player_perks_table", "kf_player_rating_table")
@widgetlib.required(css_list=("simple_table.css", "progress_bar.css", "font.css"))
def kfPlayerStatistics(user_id, config_file_path) :
	user_id = validators.common.validNumber(user_id, 1)
	config_file_path = validators.fs.validAccessiblePath(config_file_path)

	stat_dict = serverPerksStat(config_file_path)
	if not user_id in stat_dict :
		raise RuntimeError("Invalid Steam ID")

	return (
		playerStatisticsTable(stat_dict, user_id),
		playerPerksTable(stat_dict, user_id),
		playerRatingTable(stat_dict, user_id),
	)

@widgetlib.provides("kf_player_rank")
def kfPlayerAchievement(user_id, config_file_path, rank_img_url) :
	user_id = validators.common.validNumber(user_id, 1)
	config_file_path = validators.fs.validAccessiblePath(config_file_path)
	# FIXME: No validation for rank img url!

	stat_dict = serverPerksStat(config_file_path)
	if not user_id in stat_dict :
		raise RuntimeError("Invalid Steam ID")

	return (
		 playerRank(stat_dict, user_id, rank_img_url),
	)


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

def sortedPlayers(stat_dict, key, user_id = None) :
	sorted_players_list = sorted(stat_dict.items(), key=key)
	index = -1
	for count in xrange(len(sorted_players_list)) :
		if sorted_players_list[count][0] == user_id :
			index = count
		sorted_players_list[count] = [count] + list(sorted_players_list[count])
	return (sorted_players_list, index)


###
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


#####
def serverLeaderboardTable(stat_dict, limit = 5) :
	count = 1
	leaderboard_list = []
	for (user_id, player_stat_dict) in sorted(stat_dict.items(), key=( lambda arg : -arg[1]["KillsStat"] )) :
		leaderboard_list.append([
				str(count),
				{ "nowrap" : None, "body" : player_stat_dict["PlayerName"] },
				str(player_stat_dict["KillsStat"]),
				tools.fmt.formatTimeDelta(player_stat_dict["TotalPlayTime"])
			])
		if count == limit :
			break
		count += 1
	return html.tableWithHeader(["N", "Name", "Kills", "Time"], leaderboard_list)

def serverPerksTable(stat_dict, profile_url) :
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
	return html.tableWithHeader(players_header_list, players_list)


###
def playerStatisticsTable(stat_dict, user_id) :
	player_stat_dict = stat_dict[user_id]

	wins = player_stat_dict["WinsCount"]
	losts = player_stat_dict["LostsCount"]
	battles = wins + losts
	kills = player_stat_dict["KillsStat"]
	efficiency = float(kills) / float(battles)
	skill_factor = float(wins) / float(battles)

	skill_factor_text = ( """
			<div style="float:left; text-align:left;">%.2f&nbsp;</div>
			<div style="float:right; text-align:right; width:70px;">%s</div>
		""" % (skill_factor, html.progressBar(skill_factor * 100)) )

	return html.statusTable([
			("Battles", str(battles)),
			("Wins", str(wins)),
			("Losts", str(losts)),
			("Skill factor", skill_factor_text),
			("Efficiency", "%2.f" % (efficiency)),
			("Last hope", str(player_stat_dict["SoleSurvivorWavesStat"])),
			("Kills", str(kills)),
			("Time played", tools.fmt.formatTimeDelta(player_stat_dict["TotalPlayTime"])),
		])

def playerPerksTable(stat_dict, user_id) :
	perks_list = []
	for (perk, levels_map) in (
			("Berserk", BERSERK_LEVELS_MAP),
			("Sharpshooter", SHARPSHOOTER_LEVELS_MAP),
			("Firebug", FIREBUG_LEVELS_MAP),
			("Field medic", FIELD_MEDIC_LEVELS_MAP),
			("Demolitions", DEMOLITIONS_LEVELS_MAP),
			("Support spec", SUPPORT_SPEC_LEVELS_MAP),
			("Commando", COMMANDO_LEVELS_MAP) ) :
		(level, percent) = calculateLevelProgress(levels_map, stat_dict[user_id])
		max_percent = calculateProgress(levels_map, stat_dict[user_id])
		perks_list.append([
				perk,
				str(level),
				{ "width" : "150px", "body" : html.progressBar(percent) },
				{ "width" : "150px", "body" : html.progressBar(max_percent) },
			])
	return html.tableWithHeader(["Perk", "Level", "Until the next", "Until the max"], perks_list)

def playerRatingTable(stat_dict, user_id) :
	(sorted_list, index) = sortedPlayers(stat_dict, ( lambda arg : -arg[1]["KillsStat"] ), user_id)
	assert index != -1
	players_list = []
	wrap_special = ( lambda text, count : "<font class=\"special\">%s</font>" % (str(text)) if count == index else str(text) )
	for (count, stat_user_id, player_stat_dict) in sorted_list[max(index-2, 0):index+3] :
		players_list.append([
				wrap_special(count + 1, count),
				{ "nowrap" : None, "body" : wrap_special(player_stat_dict["PlayerName"], count) },
				wrap_special(player_stat_dict["KillsStat"], count),
			])
		count += 1
	return html.tableWithHeader(["N", "Name", "Kills"], players_list)

def playerRank(stat_dict, user_id, img_url) :
	wins = stat_dict[user_id]["WinsCount"]

	rank_index = 0
	player_rank = RANKS_LIST[0][1]
	prev = 0
	need_next = wins

	for (index, (need, title)) in enumerate(RANKS_LIST[1:]) :
		if wins >= need :
			player_rank = title
			rank_index = index
			prev = need
		else :
			need_next = need
			break

	rank_img = html.image(img_url % { "rank_index" : rank_index })
	rank_progress = html.progressBar(100 * (wins - prev) / (need_next - prev))

	return """
			%s<br><br>
			<div style="float:left; text-align:left;">%s</div>
			<div style="float:right; text-align:right; width:80px;">%s</div>
		""" % (player_rank, rank_img, rank_progress)

