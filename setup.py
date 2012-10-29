#!/usr/bin/env python2
# -*- coding: utf-8 -*-


from setuptools import setup


setup(
	name="slib",
	version="0.1",
	url="https://github.com/mdevaev/slib",
	license="GPLv3",
	author="Devaev Maxim",
	author_email="mdevaev@gmail.com",
	description="Silverna library - a set of macros and fcgi-application to generate HTML pages",
	platforms="any",
	packages=[
		"slib",
		"slib/tools",
		"slib/validators",
		"slib/widgets",
	],
	classifiers=[
		"Topic :: Software Development :: Libraries :: Python Modules",
		"Development Status :: 3 - Alpha",
		"Programming Language :: Python",
		"Operating System :: OS Independent",
		"Topic :: Internet :: WWW/HTTP :: Dynamic Content",
		"Topic :: Internet :: WWW/HTTP :: Dynamic Content :: CGI Tools/Libraries",
	],
)

