#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#
# Example Query Processor to catalog pages
#
#####


from slib import engine


##### Main #####
if __name__ == "__main__" :
	engine.main(
		default_page="example",
		pages_dir_path="pages",
		css_dir_path="style",
		js_dir_path="js"
	)

