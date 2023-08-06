# Setting setup file name

import os 
import sys

def setup(fname_settings):
	if os.path.isfile(fname_settings):
		sys.argv.append(fname_settings)
	else:
		sys.argv.append('settings.yaml')
		print("Warning. No settings file specified, using settings in: " + fname_settings)