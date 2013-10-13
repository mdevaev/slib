# -*- coding: utf-8 -*-


import os
import ulib.validators.common
import ulib.validators.fs

from slib import widgetlib
from slib import html


##### Public methods #####
@widgetlib.provides("random_image")
@widgetlib.required(js_list=("random_image.js",))
def randomImage(width, dir_path) :
	width = ulib.validators.common.validNumber(width, 0)
	dir_path = ulib.validators.fs.validAccessiblePath(dir_path)
	div_id = html.uniqueId("random_image %d %s" % (width, dir_path))
	images_list = [ os.path.join(dir_path, item) for item in os.listdir(dir_path) if not item.startswith(".") ]
	text = ( """
			<div align="center" id="%(div_id)s">
				<script type="text/javascript">randomImage('%(div_id)s', %(width)d, %(images)s)</script>
			</div>
		""" % { "div_id" : div_id, "width" : width, "images" : repr(images_list) } )
	return (text,)


@widgetlib.provides("images_list")
@widgetlib.required(css_list=("gallery.css",))
def imagesList(dir_path) :
	images_list = [ os.path.join(dir_path, item) for item in sorted(os.listdir(dir_path)) if not item.startswith(".") ]
	text = ""
	for image_path in images_list :
		text += ( """
				<img class="preview" src="%s">
			""" % (image_path))
	return (text,)

