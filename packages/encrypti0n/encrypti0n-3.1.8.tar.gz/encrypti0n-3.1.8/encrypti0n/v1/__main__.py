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
from encrypti0n.v1.classes.config import *
from encrypti0n.v1.classes import utils
from encrypti0n.v1.classes.encryption import Encryption,EncryptedDictionary


# the cli object class.
class CLI(object):
	def __init__(self, alias=None):
		
		# variables.
		self.modes={
			"--generate-keys":"Generate a key pair.",
			"--encrypt /path/to/file":"Encrypt the provided file path.",
			"--decrypt /path/to/file":"Decrypt the provided file path.",
			"-h / --help":"Show the documentation.",
		},
		self.options={
			"-k / --key /path/to/directory/":"Specify the path to the key's directory.",
			"-p / --passphrase 'Passphrase123!'":"Specify the key's passphrase.",
			"-l / --layers 1":"Specify the encryption layers.",
		}
		self.alias = ALIAS
		self.documentation = self.__create_docs__()

		#
	def start(self):
		
		# help.
		if self.__argument_present__('-h') or self.__argument_present__('--help'):
			print(self.documentation)

		# encrypt.
		elif self.__argument_present__('--encrypt'):
			file = self.__get_argument__('--encrypt')
			key, passphrase = self.get_key_passphrase()
			layers = self.get_layers()
			encryption = Encryption(key=key, passphrase=passphrase)
			encryption.load_keys()
			if os.path.isdir(file): 
				encryption.encrypt_directory(file, layers=layers, recursive=True)
			else: encryption.encrypt_file(file, layers=layers)

		# decrypt.
		elif self.__argument_present__('--decrypt'):
			file = self.__get_argument__('--decrypt')
			key, passphrase = self.get_key_passphrase()
			layers = self.get_layers()
			encryption = Encryption(key=key, passphrase=passphrase)
			encryption.load_keys()
			if os.path.isdir(file): 
				encryption.decrypt_directory(file, layers=layers, recursive=True)
			else: encryption.decrypt_file(file, layers=layers)

		# generate-keys.
		elif self.__argument_present__('--generate-keys'):
			file = self.__get_argument__('--generate-keys')
			key, passphrase = self.get_key_passphrase()
			encryption = Encryption(key=key, passphrase=passphrase)
			encryption.generate_keys()

		# invalid.
		else: 
			print(self.documentation)
			print("Selected an invalid mode.")

		#
	def get_layers(self):
		layers = self.__get_argument__('--layers', required=False)
		if layers != None: return int(layers)
		layers = self.__get_argument__('-l', required=False)
		if layers != None: return int(layers)
		else: return 1
	def get_key_passphrase(self):
		key = self.__get_argument__('-k', required=False)
		if key == None:
			key = self.__get_argument__('--key', required=True)
		passphrase = self.__get_argument__('-p', required=False)
		if passphrase == None:
			passphrase = self.__get_argument__('--passphrase', required=False)
		if passphrase == None:
			passprase = utils.__prompt_password__("Enter the key's passphrase:")
		return key, passphrase
	# system functions.
	def __create_docs__(self):
		m = str(json.dumps(self.modes, indent=4)).replace('    }','').replace('    {','').replace('    "','')[:-1][1:].replace('    "', "    ").replace('",',"").replace('": "'," : ")[2:][:-3]
		#o = str(json.dumps(self.options, indent=4)).replace('    }','').replace('    {','').replace('    "','')[:-1][1:].replace('    "', "    ").replace('",',"").replace('": "'," : ")[2:][:-3]
		o = str(json.dumps(self.options, indent=4)).replace('{\n','').replace('}\n','').replace('    "','    ').replace('": "',' : ').replace('",\n','\n').replace('"\n','\n')[:-2]
		c = "\nAuthor: Daan van den Bergh \nCopyright: © Daan van den Bergh 2020. All rights reserved."
		doc = "Usage: "+self.alias+" <mode> <options> \nModes:\n"+m
		if o != "": doc += "\nOptions:\n"+o
		doc += c
		return doc
	def __argument_present__(self, argument):
		if argument in sys.argv: return True
		else: return False
	def __get_argument__(self, argument, required=True, index=1, empty=None):

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
	
# main.
if __name__ == "__main__":
	cli = CLI()
	cli.start()
