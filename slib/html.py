# -*- coding: utf-8 -*-


import re

import tools.types


##### Public methods #####
def maybeLink(url) :
	if not re.match(r"^[a-zA-Z0-9_\-]+://.*", url) is None :
		return "<a href=\"%s\">%s</a>" % (url, url)
	else :
		return url

def buttonLink(title, url, css_list=("button",)) :
	return ( """
			<form action="%s">
				<input class="%s" type="submit" value="%s">
			</form>
		""" % (url, css_list[0], title) )


###
def progressBar(percent, css_list=("progress_internal", "progress_external")) :
	return ( """
			<div class="%s">
				<div class="%s" style="width: %d%%;">
					&nbsp;
				</div>
			</div>
		""" % (css_list[0], css_list[1], percent) )


###
def spoilerTitle(title, css_list=("script",)) :
	div_id = tools.types.uniqueId(title)
	return (div_id, "<a class=\"%s\" href=\"javascript:toggleSpoiler('%s')\">%s</a>" % (css_list[0], div_id, title))

def spoilerBody(div_id, text) :
	return "<div style=\"display:none;\" id=\"%s\">%s</div>" % (div_id, text)

def spoiler(title, text) :
	(div_id, title) = spoilerTitle(title)
	return title + spoilerBody(div_id, text)


###
def simpleTable(rows_list, css_list=("simple",)) :
	trs = ""
	for items_list in rows_list :
		items_list = map(lambda arg : constructTag("td", arg), items_list)
		trs += "<tr>%s</tr>" % ("".join(items_list))
	return "<table class=\"%s\">%s</table>" % (css_list[0], trs)

def tableWithHeader(header_list, rows_list, css_list=("bold", "simple")) :
	header_list = map(lambda arg : { "class" : css_list[0], "body" : arg }, header_list)
	return simpleTable([header_list] + ( rows_list or [[""] * len(header_list)]), css_list[1:])

def statusTable(table_list, css_list=("bold", "simple")) :
	rows_list = []
	for (label, data) in table_list :
		rows_list.append([{ "class" : css_list[0], "body" : label }, data])
	return simpleTable(rows_list, css_list[1:])


###
def image(url, alt = None) :
	return "<img alt=\"%s\" src=\"%s\">" % ((alt or url), url)


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

