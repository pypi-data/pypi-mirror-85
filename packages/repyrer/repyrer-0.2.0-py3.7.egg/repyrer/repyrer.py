import sys
import os
import re
from importlib import import_module

def repyre(path):

	# rip off a `./` from the beginning to indicate relative-to-file imports
	local_file, _path = re.match("([.][/])?(.*)",path).groups()

	# rip off any residule pathing information
	_path, module_name = os.path.split(_path)

	# prepend file directory, if indicated by a `./`
	if not local_file is None:
		_path = os.path.join(sys.path[0],_path)

	# Make sure python checks the provided directory first
	sys.path.insert(0,_path)
	try:
		return import_module(module_name)
	finally:
		# always remove the inserted path object so as not to clutter sys.path
		sys.path.pop(0)
