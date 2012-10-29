# -*- coding: utf-8 -*-


import sys
import os
import re
import cgi
import httplib
import traceback
import time

import page
import widgets
import widgetlib
import tools.types


##### Public constants #####
DEFAULT_PAGE = None
PAGES_DIR = "pages"
CSS_DIR = "style"
JS_DIR = "js"


##### Exceptions #####
class BadRequest(Exception) :
	def __init__(self, code, text) :
		super(BadRequest, self).__init__()
		self.__code = code
		self.__text = text

	def text(self) :
		return self.__text

	def __str__(self) :
		return "%d %s" % (self.__code, httplib.responses[self.__code])


##### Public classes #####
class SlibServer(object) :
	def __init__(self, default_page, pages_dir_path, css_dir_path, js_dir_path, widgets_list) :
		object.__init__(self)

		self.__default_page = default_page
		self.__pages_dir_path = pages_dir_path
		self.__css_dir_path = css_dir_path
		self.__js_dir_path = js_dir_path
		self.__widgets_list = widgets_list


	### Public ###

	def application(self, env_dict, start_response) :
		try :
			(response, content_type) = self.processRequest(env_dict)
			start_response("200 OK", [("Content-Type", content_type)])
			return tools.types.chunks(response, 1024)
		except BadRequest, err :
			self.logFail(env_dict)
			start_response(str(err), [("Content-Type", "text/plain")])
			return "ERROR: %s" % (err.text())
		except Exception, err :
			self.logFail(env_dict)
			start_response("500 Internal Error", [("Content-Type", "text/plain")])
			return "ERROR: %s" % (str(err))


	### Private ###

	def processRequest(self, env_dict) :
		args_dict = cgi.parse_qs(env_dict["QUERY_STRING"], keep_blank_values=True)
		for (key, value) in args_dict.iteritems() :
			args_dict[key] = value[0]

		page_name = args_dict.get("page", self.__default_page)
		if page_name is None :
			raise BadRequest(400, "Missing page name")
		elif re.match(r"^[a-zA-Z0-9_-]+$", page_name) is None :
			raise BadRequest(400, "Invalid page name")
		elif not os.access(os.path.join(self.__pages_dir_path, page_name), os.F_OK) :
			raise BadRequest(404, "Not found: %s" % (page_name))

		with open(os.path.join(self.__pages_dir_path, page_name)) as page_file :
			text = page_file.read()
			text = page.replaceWidgetPlaceholders(text, args_dict)
			text = page.replaceWidgets(text, self.__widgets_list, self.__css_dir_path, self.__js_dir_path)
			return (text, "text/html")

	def logFail(self, env_dict) :
		request = ( "Protocol: %(SERVER_PROTOCOL)s\n"
			"Method: %(REQUEST_METHOD)s\n"
			"Path: %(PATH_INFO)s\n"
			"Query: %(QUERY_STRING)s\n" % (env_dict) )
		request += "User-Agent: %s" % (env_dict.get("HTTP_USER_AGENT", ""))
		message = "----- Error: %s -----\n%s\n-----\n%s" % (time.ctime(), request, traceback.format_exc())
		print >> sys.stderr, message


##### Public methods #####
def main(default_page = DEFAULT_PAGE, pages_dir_path = PAGES_DIR, css_dir_path = CSS_DIR, js_dir_path = JS_DIR, widgets_list = ()) :
	from flup.server.fcgi import WSGIServer

	path = os.path.dirname(sys.argv[0])
	if len(path) != 0 :
		os.chdir(path)

	widgets_list = ( widgets_list or widgetlib.buildWidgetsTree(widgets)[1].values() )
	WSGIServer(SlibServer(default_page, pages_dir_path, css_dir_path, js_dir_path, widgets_list).application).run()

