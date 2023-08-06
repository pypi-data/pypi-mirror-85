#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# insert the package for universal imports.
import os, sys, pathlib

# functions.
def __get_file_path_base__(path, back=1):
	path = path.replace('//','/')
	if path[len(path)-1] == "/": path = path[:-1]
	string, items, c = "", path.split("/"), 0
	for item in items:
		if c == len(items)-(1+back):
			string += "/"+item
			break
		else:
			string += "/"+item
		c += 1
	return string+"/"

# settings.
SOURCE_NAME = "ssht00ls"
VERSION = "v1"
SOURCE_PATH = __get_file_path_base__(__file__, back=2)
BASE = __get_file_path_base__(SOURCE_PATH)
sys.path.insert(1, BASE)

# imports.
from ssht00ls.v1.classes.config import *
from ssht00ls.v1.classes import *

# the cli object class.
class CLI(cl1.CLI):
	def __init__(self):
		
		# defaults.
		cl1.CLI.__init__(self,
			modes={
				"--create-alias":"Create a ssh alias.",
				"    --server myserver":"Specify the server's name.",
				"    --username myuser":"Specify the username.",
				"    --ip 0.0.0.0":"Specify the server's ip.",
				"    --port 22":"Specify the server's port.",
				"    for ssh keys:":"",
				"    --key /path/to/key/private_key":"Specify the path to the private key.",
				"    for smart cards:":"",
				"    --smart-cards":"Enable the smart cards boolean.",
				"-h / --help":"Show the documentation.",
			},
			options={},
			alias=ALIAS,
			executable=__file__,
		)

		#
	def start(self):
		
		# help.
		if self.arguments_present(['-h', '--help']):
			print(self.documentation)

		# check create ssh config.
		elif self.argument_present('--create-alias'):
			
			# create an ssh alias for the key.
			if not self.argument_present('--smart-card'):
				response = config.create_alias( 
					# the servers name.
					server=self.get_argument('--server'), 
					# the username.
					username=self.get_argument('--username'), 
					# the ip of the server.
					ip=self.get_argument('--ip'),
					# the port of the server.
					port=self.get_argument('--port'),
					# the path to the private key.
					key=self.get_argument('--key'),
					# smart card.
					smart_card=False,)

			# create an ssh alias for a smart card.
			else:
				response = config.create_alias( 
					# the servers name.
					server=self.get_argument('--server'), 
					# the username.
					username=self.get_argument('--username'), 
					# the ip of the server.
					ip=self.get_argument('--ip'),
					# the port of the server.
					port=self.get_argument('--port'),
					# the path to the private key.
					key=smart_card.path,
					# smart card.
					smart_card=True,)

			# log to console.
			if response["error"] != None: print(response["error"])
			else: print(response["message"])

		# invalid.
		else: 
			print(self.documentation)
			print("Selected an invalid mode.")

		#
	
# main.
if __name__ == "__main__":
	cli = CLI()
	cli.start()
