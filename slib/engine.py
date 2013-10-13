# -*- coding: utf-8 -*-


import sys
import os
import cgi
import httplib
import ulib.tools.types

import page
import widgets
import widgetlib
import logger
import validators.system

from ulib.validatorlib import ValidatorError


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
			return ulib.tools.types.chunks(response, 1024)
		except BadRequest, err :
			self.logException(env_dict)
			start_response(str(err), [("Content-Type", "text/plain")])
			return "ERROR: %s" % (err.text())
		except Exception, err :
			self.logException(env_dict)
			start_response("500 Internal Error", [("Content-Type", "text/plain")])
			return "ERROR: %s" % (str(err))


	### Private ###

	def processRequest(self, env_dict) :
		args_dict = cgi.parse_qs(env_dict["QUERY_STRING"], keep_blank_values=True)
		for (key, value) in args_dict.iteritems() :
			args_dict[validators.system.validVariableName(key)] = value[0]

		page_name = args_dict.get("page", self.__default_page)
		if page_name is None :
			raise BadRequest(400, "Missing page name")

		try :
			page_name = validators.system.validPageName(page_name)
		except ValidatorError, err :
			raise BadRequest(400, str(err))

		if not os.access(os.path.join(self.__pages_dir_path, page_name), os.F_OK) :
			raise BadRequest(404, "Not found: %s" % (page_name))

		with open(os.path.join(self.__pages_dir_path, page_name)) as page_file :
			text = page_file.read()
			return page.replaceWidgets(text, self.__widgets_list, args_dict, self.__css_dir_path, self.__js_dir_path) # (text, content_type)

	def logException(self, env_dict) :
		request = ( "Protocol: %(SERVER_PROTOCOL)s\n"
			"Method: %(REQUEST_METHOD)s\n"
			"Path: %(PATH_INFO)s\n"
			"Query: %(QUERY_STRING)s\n" % (env_dict) )
		request += "User-Agent: %s" % (env_dict.get("HTTP_USER_AGENT", ""))
		logger.attachException(request)


##### Public methods #####
def runLocalServer(server, port = 8080) :
	import paste.httpserver
	paste.httpserver.serve(server.application, port=port)

def runFcgiServer(server) :
	from flup.server.fcgi import WSGIServer
	WSGIServer(server.application).run()

def main(default_page = DEFAULT_PAGE, pages_dir_path = PAGES_DIR, css_dir_path = CSS_DIR, js_dir_path = JS_DIR, widgets_list = ()) :
	path = os.path.dirname(sys.argv[0])
	if len(path) != 0 :
		os.chdir(path)
	widgets_list = ( widgets_list or widgetlib.buildWidgetsTree(widgets)[1].values() )
	server = SlibServer(default_page, pages_dir_path, css_dir_path, js_dir_path, widgets_list)

	if "local" in sys.argv[1:] :
		runLocalServer(server)
	else :
		runFcgiServer(server)

