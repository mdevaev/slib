# -*- coding: utf-8 -*-


import types
import decorator


##### Public methods #####
def provides(*macroses_list) :
	def make_method(method) :
		setattr(method, "is_widget", True)
		setattr(method, "widget_macroses_list", macroses_list)
		def wrap(method, *args_list, **kwargs_dict) :
			results_list = method(*args_list, **kwargs_dict)
			assert isinstance(results_list, (list, tuple)), "Invalid result type"
			assert len(macroses_list) == len(results_list), "Invalid results count"
			for result in results_list :
				assert isinstance(result, (str, unicode)), "Invalid macros result"
			return dict([(macroses_list[count], results_list[count]) for count in xrange(len(macroses_list))])
		return decorator.decorator(wrap, method)
	return make_method

def widgetProvides(method) :
	return list(getattr(method, "widget_macroses_list"))


###
def required(css_list=(), js_list=()) :
	assert isinstance(css_list, (list, tuple)), "Required CSS must be a list"
	assert isinstance(js_list, (list, tuple)), "Required JS must be a list"
	def make_method(method) :
		setattr(method, "is_widget", True)
		setattr(method, "widget_required_css", list(css_list))
		setattr(method, "widget_required_js", list(js_list))
		return method
	return make_method

def widgetRequired(method) :
	return {
		"css" : list(getattr(method, "widget_required_css", ())),
		"js" : list(getattr(method, "widget_required_js", ())),
	}


###
def buildWidgetsTree(module) :
	widgets_tree_dict = {}
	widgets_dict = {}

	for item_name in dir(module) :
		item = getattr(module, item_name)
		if isinstance(item, types.ModuleType) and (hasattr(item, "__file__") and "slib/widgets/" in item.__file__) :
			(child_widgets_tree_dict, child_widgets_dict) = buildWidgetsTree(item)
			widgets_tree_dict[item_name] = child_widgets_tree_dict
			widgets_dict.update(child_widgets_dict)
		elif isinstance(item, types.FunctionType) and getattr(item, "is_widget", False) :
			widgets_tree_dict[item_name] = item
			widgets_dict["%s.%s" % (item.__module__, item.__name__)] = item

	return (widgets_tree_dict, widgets_dict)

