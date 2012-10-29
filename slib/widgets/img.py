# -*- coding: utf-8 -*-


import os

from slib import widgetlib

from slib import tools
import slib.tools.types

from slib import validators
import slib.validators.common
import slib.validators.fs


##### Public methods #####
@widgetlib.provides("random_image")
@widgetlib.required(js_list=("random_image.js",))
def randomImage(width, dir_path) :
	width = validators.common.validNumber(width, 0)
	dir_path = validators.fs.validAccessiblePath(dir_path)
	div_id = tools.types.uniqueId("random_image %d %s" % (width, dir_path))
	images_list = [ os.path.join(dir_path, item) for item in os.listdir(dir_path) ]
	text = ( """
			<div align="center" id="%(div_id)s">
				<script type="text/javascript">randomImage('%(div_id)s', %(width)d, %(images)s)</script>
			</div>
		""" % { "div_id" : div_id, "width" : width, "images" : repr(images_list) } )
	return (text,)
