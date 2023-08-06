#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# imports.
from r3sponse.v1.classes.config import * 

# argument functions.
def argument_present(arguments):
	if isinstance(arguments, str):
		if arguments in sys.argv: return True
		else: return False
	elif isinstance(arguments, list):
		for argument in arguments:
			if argument in sys.argv: return True
		return False
	else: raise ValueError("Invalid usage, arguments must either be a list or string.")
def get_argument(argument, required=True, index=1, empty=None):

	# check presence.
	if argument not in sys.argv:
		if required:
			raise ValueError(f"Define parameter [{argument}].")
		else: return empty

	# retrieve.
	y = 0
	for x in sys.argv:
		try:
			if x == argument: return sys.argv[y+index]
		except IndexError:
			if required:
				raise ValueError(f"Define parameter [{argument}].")
			else: return empty
		y += 1

	# should not happen.
	return empty