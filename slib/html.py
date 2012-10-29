# -*- coding: utf-8 -*-


import re

import tools.types


##### Public methods #####
def maybeLink(url) :
	if not re.match(r"^[a-zA-Z0-9_\-]+://.*", url) is None :
		return "<a href=\"%s\">%s</a>" % (url, url)
	else :
		return url


###
def progressBar(percent) :
	return ( """
			<div class="progress_internal">
				<div class="progress_external" style="width: %d%%;">
					&nbsp;
				</div>
			</div>
		""" % (percent) )


###
def spoilerTitle(title) :
	div_id = tools.types.uniqueId(title)
	return (div_id, "<a class=\"script\" href=\"javascript:toggleSpoiler('%s')\">%s</a>" % (div_id, title))

def spoilerBody(div_id, text) :
	return "<div style=\"display:none;\" id=\"%s\">%s</div>" % (div_id, text)

def spoiler(title, text) :
	(div_id, title) = spoilerTitle(title)
	return title + spoilerBody(div_id, text)


###
def simpleTable(rows_list) :
	trs = ""
	for items_list in rows_list :
		items_list = map(lambda arg : constructTag("td", arg), items_list)
		trs += "<tr>%s</tr>" % ("".join(items_list))
	return "<table class=\"simple\">%s</table>" % (trs)

def tableWithHeader(header_list, rows_list) :
	header_list = map(lambda arg : "<b>%s</b>" % (arg), header_list)
	return simpleTable([header_list] + ( rows_list or [[""] * len(header_list)]))

def statusTable(table_list) :
	rows_list = []
	for (label, data) in table_list :
		rows_list.append(["<b>%s</b>" % (label), data])
	return simpleTable(rows_list)


##### Private methods #####
def constructTag(tag, body) :
	if isinstance(body, dict) :
		for (attr, value) in body.iteritems() :
			attrs = ""
			if attr == "body" :
				body = value
			elif not value is None :
				attrs += " %s=\"%s\"" % (attr, value)
			else :
				attrs += " " + attr
	elif isinstance(body, (str, unicode)) :
		attrs = ""
	else :
		raise TypeError("Invalid body type")
	return "<%s%s>%s</%s>" % (tag, attrs, body, tag)

