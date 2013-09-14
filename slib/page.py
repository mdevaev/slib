# -*- coding: utf-8 -*-


import os
import re
import helib.tools.coding
import helib.validators.common

import widgetlib
import logger

import validators.system


##### Private constants #####
JS_PATTERN = "<script type=\"text/javascript\" src=\"%s\"></script>"
CSS_PATTERN = "<style type=\"text/css\" media=\"all\">@import \"%s\";</style>"


##### Public methods #####
def replaceWidgets(text, widgets_list, args_dict, css_dir_path, js_dir_path) :
	cache_dict = {}
	for widget in widgets_list :
		for name in widgetlib.widgetProvides(widget) :
			cache_dict[name] = { None : widget }

	css_list = []
	js_list = []

	define_args_dict = {}

	for match in re.finditer(r"{([a-zA-Z_]+[^}\n]+)}", text) :
		macros_tuple = tuple(match.group(1).split())
		name = macros_tuple[0]
		args_tuple = macros_tuple[1:]

		if name.startswith("__") :
			if name == "__include_css__" :
				css_list += includeResources(args_tuple)
			elif name == "__include_js__" :
				js_list += includeResources(args_tuple)
			elif name == "__set_css_dir__" :
				css_dir_path = resourceDir(args_tuple, css_dir_path)
			elif name == "__set_js_dir__" :
				js_dir_path = resourceDir(args_tuple, js_dir_path)
			elif name == "__define_args__" :
				updateDefineArgs(define_args_dict, args_tuple)
			else :
				continue
			text = text.replace("{%s}" % (match.group(1)), "")
		else :
			widget = cache_dict.get(name, {}).get(None, None)
			if widget is None :
				continue

			args_tuple = define_args_dict.get(name, args_tuple)
			if cache_dict[name].get(args_tuple, None) is None :
				try :
					args_list = list(args_tuple)
					for (index, item) in enumerate(args_list) :
						if item.startswith("$") :
							variable = validators.system.validVariableName(item[1:])
							if variable in args_dict :
								args_list[index] = args_dict[variable]
							else :
								raise RuntimeError("Missing required argument \"%s\"" % (variable))

					result_dict = widget(*args_list)
					required_dict = widgetlib.widgetRequired(widget)
					css_list += required_dict["css"]
					js_list += required_dict["js"]
				except Exception, err :
					message = "{%s :: %s: %s}" % (name, type(err).__name__, str(err))
					result_dict = dict.fromkeys(widgetlib.widgetProvides(widget), message)
					logger.attachException("Error while processing widget %s(%s)" % (name, str(args_tuple)))
				for (key, value) in result_dict.iteritems() :
					cache_dict[key][args_tuple] = helib.tools.coding.utf8(value)

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

def includeResources(args_tuple) :
	return filter(None, map(str.strip, args_tuple))

def resourceDir(args_tuple, old_path) :
	if len(args_tuple) == 0 :
		return old_path
	new_path = args_tuple[0].strip()
	if len(new_path) == 0 :
		return old_path
	return new_path

def updateDefineArgs(define_args_dict, args_tuple) :
	args_list = filter(None, map(str.strip, args_tuple))
	if len(args_list) == 0 :
		return
	keys_list = helib.validators.common.validStringList(args_list[0])
	define_args_dict.update(dict.fromkeys(keys_list, tuple(args_list[1:])))

