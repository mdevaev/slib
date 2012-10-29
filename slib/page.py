# -*- coding: utf-8 -*-


import os
import re

import widgetlib


##### Private constants #####
JS_PATTERN = "<script type=\"text/javascript\" src=\"%s\"></script>"
CSS_PATTERN = "<style type=\"text/css\" media=\"all\">@import \"%s\";</style>"


##### Public methods #####
def replaceWidgetPlaceholders(text, placeholders_dict) :
	return text # TODO: implement this feature

def replaceWidgets(text, widgets_list, css_dir_path, js_dir_path) :
	cache_dict = {}
	for widget in widgets_list :
		for name in widgetlib.widgetProvides(widget) :
			cache_dict[name] = { None : widget }

	css_list = []
	js_list = []

	for match in re.finditer(r"{([a-zA-Z]+[^}\n]+)}", text) :
		macros_tuple = tuple(match.group(1).split())
		name = macros_tuple[0]
		args_tuple = macros_tuple[1:]
		widget = cache_dict.get(name, {}).get(None, None)
		if widget is None :
			continue

		if cache_dict[name].get(args_tuple, None) is None :
			try :
				result_dict = widget(*args_tuple)
				required_dict = widgetlib.widgetRequired(widget)
				css_list += required_dict["css"]
				js_list += required_dict["js"]
			except Exception, err :
				message = "{%s :: %s: %s}" % (name, type(err).__name__, str(err))
				result_dict = dict.fromkeys(widgetlib.widgetProvides(widget), message)
			for (key, value) in result_dict.iteritems() :
				cache_dict[key][args_tuple] = value

		text = text.replace("{%s}" % (match.group(1)), cache_dict[name][args_tuple])

	css = "\n".join(map(lambda arg : makeResourceLink(arg, css_dir_path, CSS_PATTERN), list(set(css_list))))
	js = "\n".join(map(lambda arg : makeResourceLink(arg, js_dir_path, JS_PATTERN), list(set(js_list))))
	text = text.replace("{__css__}", css)
	text = text.replace("{__js__}", js)

	return text


##### Private methods #####
def makeResourceLink(url, dir_path, pattern) :
	if re.match(r"^[a-zA-Z0-9_\-]+://.*", url) is None :
		url = os.path.join(dir_path, url)
	return pattern % (url)

