#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# imports.
from encrypti0n.v1.classes.config import *
from encrypti0n.v1.classes import utils

# new imports.
import zlib, base64, binascii, glob
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

# inc imports.
from fil3s import Files, Formats

# the encryption class.
class Encryption(object):
	def __init__(self, 
		key=None,
		passphrase=None,
	):
		self.key = key
		self.passphrase = passphrase
		self.public_key = None
		self.private_key = None
	# key management.
	def generate_keys(self):

		# default response.
		response = utils.__default_response__()

		# checks.
		if os.path.exists(self.key): 
			response["error"] = f"Key [{self.key}] already exists."
			return response
			
		# generate.
		key_pair = RSA.generate(4096, e=65537)
		public_key = key_pair.publickey()
		public_key_pem = public_key.exportKey()
		private_key_pem = None
		if self.passphrase == None: 
			private_key_pem = key_pair.exportKey()
		else:  
			private_key_pem = key_pair.exportKey(passphrase=self.passphrase)

		# save.
		os.mkdir(self.key)
		utils.__save_file__(self.key+"/private_key.pem", private_key_pem.decode())
		utils.__save_file__(self.key+"/public_key.pem", public_key_pem.decode())
		utils.__set_file_path_permission__(self.key, permission=700)
		utils.__set_file_path_permission__(self.key+"/private_key.pem", permission=600)
		utils.__set_file_path_permission__(self.key+"/public_key.pem", permission=644)
		
		# response.
		response["success"] = True
		response["message"] = "Successfully generated a key pair."
		return response

		#
	def load_keys(self):

		# load keys.
		response = utils.__default_response__()
		self.public_key = utils.__load_file__(self.key+"/public_key.pem")
		self.private_key = utils.__load_file__(self.key+"/private_key.pem")

		# initialize keys.
		if self.passphrase == None:
			try:
				self.public_key = RSA.importKey(self.public_key)
				self.private_key = RSA.importKey(self.private_key)
			except ValueError as e:
				if "Padding is incorrect" in str(e):
					response["error"] = "Provided an incorrect passphrase."
				else: response["error"] = f"ValueError: {e}"
				return response
		else:
			try:
				self.public_key = RSA.importKey(self.public_key, passphrase=self.passphrase)
				self.private_key = RSA.importKey(self.private_key, passphrase=self.passphrase)
			except ValueError as e:
				if "Padding is incorrect" in str(e):
					response["error"] = "Provided an incorrect passphrase."
				else: response["error"] = f"ValueError: {e}"
				return response
		
		# response.
		response["success"] = True
		response["message"] = "Successfully loaded the key pair."
		return response

		#
	def edit_passphrase(self, passphrase=None):

		if passphrase == None:
			passphrase = '""'
		output = utils.__execute__(["ssh-keygen", "-p", "-P", f"{self.passphrase}", "-N", f"{passphrase}", "-f", f"{self.key}/private_key.pem"])

		# response.
		response = utils.__default_response__()
		if "Your identification has been saved with the new passphrase." in output:
			self.passphrase = passphrase
			if self.passphrase == '""': self.passphrase = None
			response["success"] = True
			response["message"] = "Successfully loaded the key pair."
			return response
		else:
			response["error"] = f"Failed to edit the passphrase of key [{self.key}], error: {output}."
			return response

		#
	# encrypting.
	def encrypt_file(self, path, layers=1):

		# encrypt.
		response = utils.__default_response__()
		bytes = utils.__load_bytes__(path)
		encrypted = self.__encrypt_blob__(bytes, self.public_key)
		utils.__save_bytes__(path, encrypted)

		# layers.
		if layers-1 > 0:
			return self.encrypt_file(path, layers=layers-1)
		else:
			response["success"] = True
			response["message"] = f"Successfully encrypted file [{path}]."
			return response

		#
	def encrypt_directory(self, path, recursive=False, layers=1):
		response = utils.__default_response__()

		# recursively encrypt all files.
		if recursive:

			# recursive.
			for i in os.listdir(path):
				i = f'{path}/{i}'.replace("//",'/')
				if os.path.isdir(i):
					response = self.encrypt_directory(i, recursive=True)
					if response["error"] != None:
						return response
				else:
					response = self.encrypt_file(i)
					if response["error"] != None:
						return response

			# success.
			response = utils.__default_response__()
			if layers-1 > 0:
				return self.encrypt_directory(path, recursive=True, layers=layers-1)
			else:
				response["success"] = True
				response["message"] = f"Successfully encrypted directory [{path}] (recursively)."
				return response		


		# encrypt the directory and save to x.encrypted.zip file.
		else:

			# checks.
			file_path = Formats.FilePath(path)
			if not file_path.exists():
				response["error"] = f"Directory [{path}] does not exist."
				return response
			if not file_path.directory():
				response["error"] = f"Directory path [{path}] is not a directory."
				return response

			# create zip.
			if path[len(path)-1] == "/": zip_path = path[:-1]
			else: zip_path = str(path)
			zip_path = f'{zip_path}.encrypted.zip'
			zip = Files.Zip(path=zip_path)
			zip.create(source=path)

			# encrypt zip.
			response = utils.__default_response__()
			response = self.encrypt_file(zip.file_path.path, layers=layers)
			if response["success"]:
				response["success"] = True
				response["message"] = f"Successfully encrypted directory [{path}]."
				file_path.delete(forced=True)
				return response
			else:
				response["error"] = f"Failed to encrypted directory [{path}]."
				zip.file_path.delete(forced=True)
				return response

		#
	def encrypt_string(self, string, layers=1):

		# encrypt.
		response = utils.__default_response__()
		encrypted = self.__encrypt_blob__(string, self.public_key)

		# layers.
		if layers-1 > 0:
			return self.encrypt_string(encrypted, layers=layers-1)
		else:
			response["success"] = True
			response["message"] = f"Successfully encrypted the string."
			response["encrypted"] = encrypted.decode()
			return response

		#
	# decrypting.
	def decrypt_file(self, path, layers=1):

		# encrypt.
		response = utils.__default_response__()
		bytes = utils.__load_bytes__(path)
		decrypted = self.__decrypt_blob__(bytes, self.private_key)
		utils.__save_bytes__(path, decrypted)
		
		# layers.
		if layers-1 > 0:
			return self.decrypt_file(path, layers=layers-1)
		else:
			response["success"] = True
			response["message"] = f"Successfully decrypted file [{path}]."
			return response

		#
	def decrypt_string(self, string, layers=1):
		
		# decrypt.
		response = utils.__default_response__()
		if isinstance(string,str): string = string.encode()
		decrypted = self.__decrypt_blob__(string, self.private_key)
		
		# layers.
		if layers-1 > 0:
			return self.decrypt_string(decrypted, layers=layers-1)
		else:
			response["success"] = True
			response["message"] = f"Successfully encrypted the string."
			response["decrypted"] = decrypted.decode()
			return response

		#
	def decrypt_directory(self, path, recursive=False, layers=1):
		response = utils.__default_response__()

		# recursively decrypt all files.
		if recursive:
			
			# recursive.
			for i in os.listdir(path):
				i = f'{path}/{i}'.replace("//",'/')
				if os.path.isdir(i):
					response = self.decrypt_directory(i, recursive=True)
					if response["error"] != None:
						return response
				else:
					response = self.decrypt_file(i)
					if response["error"] != None:
						return response

			# success.
			response = utils.__default_response__()
			if layers-1 > 0:
				return self.decrypt_directory(path, recursive=True, layers=layers-1)
			else:
				response["success"] = True
				response["message"] = f"Successfully decrypted directory [{path}] (recursively)."
				return response		

		# decrypt the encrypted.zip file.
		else:
			path = path.replace('.encrypted.zip', '/')

			# checks.
			file_path = Formats.FilePath(path)

			# set zip path.
			if path[len(path)-1] == "/": zip_path = path[:-1]
			else: zip_path = str(path)
			zip_path = f'{zip_path}.encrypted.zip'
			if not os.path.exists(zip_path):
				response["error"] = f"System encrypted zip [{path}] does not exist."
				return response
			
			# decrypt zip.
			response = self.decrypt_file(zip_path, layers=layers)
			if response["error"] != None:
				response["error"] = f"Failed to decrypted directory [{path}]."
				return response

			# extract zip.
			response = utils.__default_response__()
			zip = Files.Zip(path=zip_path)
			zip.extract(base=None)
			if os.path.exists(path):
				response["success"] = True
				response["message"] = f"Successfully decrypted directory [{path}]."
				zip.file_path.delete(forced=True)
				return response
			else:
				response["error"] = f"Failed to decrypted directory [{path}]."
				return response

		#
	# system functions.
	def __encrypt_blob__(self, blob, public_key, silent=True):
		#Import the Public Key and use for encryption using PKCS1_OAEP
		rsa_key = public_key
		rsa_key = PKCS1_OAEP.new(rsa_key)

		#compress the data first
		try: 
			blob = zlib.compress(blob.encode())
		except: 
			blob = zlib.compress(blob)
		
		#In determining the chunk size, determine the private key length used in bytes
		#and subtract 42 bytes (when using PKCS1_OAEP). The data will be in encrypted
		#in chunks
		chunk_size = 470
		offset = 0
		end_loop = False
		encrypted = bytearray()
		max_offset, progress = len(blob), 0
		if silent == False: print(f'Encrypting {max_offset} bytes.')
		while not end_loop:
			#The chunk
			chunk = blob[offset:offset + chunk_size]

			#If the data chunk is less then the chunk size, then we need to add
			#padding with " ". This indicates the we reached the end of the file
			#so we end loop here
			if len(chunk) % chunk_size != 0:
				end_loop = True
				#chunk += b" " * (chunk_size - len(chunk))
				chunk += bytes(chunk_size - len(chunk))
			#Append the encrypted chunk to the overall encrypted file
			encrypted += rsa_key.encrypt(chunk)

			#Increase the offset by chunk size
			offset += chunk_size
			l_progress = round((offset/max_offset)*100,2)
			if l_progress != progress:
				progress = l_progress
				if silent == False: print('Progress: '+str(progress), end='\r')

		#Base 64 encode the encrypted file
		return base64.b64encode(encrypted)
	def __decrypt_blob__(self, encrypted_blob, private_key, silent=True):

		#Import the Private Key and use for decryption using PKCS1_OAEP
		rsakey = private_key
		rsakey = PKCS1_OAEP.new(rsakey)

		#Base 64 decode the data
		encrypted_blob = base64.b64decode(encrypted_blob)

		#In determining the chunk size, determine the private key length used in bytes.
		#The data will be in decrypted in chunks
		chunk_size = 512
		offset = 0
		decrypted = bytearray()
		max_offset = len(encrypted_blob)
		progress = 0
		if silent == False: print(f'Decrypting {max_offset} bytes.')
		#keep loop going as long as we have chunks to decrypt
		while offset < len(encrypted_blob):
			#The chunk
			chunk = encrypted_blob[offset: offset + chunk_size]

			#Append the decrypted chunk to the overall decrypted file
			decrypted += rsakey.decrypt(chunk)

			#Increase the offset by chunk size
			offset += chunk_size
			l_progress = round((offset/max_offset)*100,2)
			if l_progress != progress:
				progress = l_progress
				if silent == False: print('Progress: '+str(progress), end='\r')

		#return the decompressed decrypted data
		return zlib.decompress(decrypted)

# the encrypted dictionary class.
class EncryptedDictionary(Files.Dictionary):
	"""
		The saved dictionary remains encrypted while local memory contains the decrypted dict.
		Requires already generated keys.
	"""	
	def __init__(self,
		# the file path.
		path=None, 
		# the dictionary.
		dictionary=None, 
		# specify default to check & create the dict.
		default={}, 
		# load the dictionary.
		load=True,
		# the key's path.
		key=None,
		# the key's passphrase.
		passphrase=None,
		# the encryption layers.
		layers=1,
	):

		# the dictionary object.
		self.default = default
		self._load_ = load
		self.dictionary = dictionary
		self._dictionary_ = Files.Dictionary(
			path=False, 
			dictionary=self.dictionary, )

		# the file object.
		self._file_ = Files.File(path=path)

		# variables.
		self.file_path = self._file_.file_path

		# the encryption object.
		self.key = key
		self.passphrase = passphrase
		self.layers = layers

	def initialize(self):
		response = utils.__default_response__()

		# init encryption,
		self.encryption = Encryption(
			key=self.key,
			passphrase=self.passphrase,)
		response = self.encryption.load_keys()
		if response["error"] != None: return response

		# checks.
		response = utils.__default_response__()
		created = False
		if not self._file_.file_path.exists():
			self._file_.save(json.dumps(self.default, indent=4, ensure_ascii=False))
			response = self.encryption.encrypt_file(self.file_path.path, layers=self.layers)
		elif self._load_:
			response = self.load()
			if response["error"] != None: return response
		if not created and self.default != None:
			if self.dictionary == None: 
				response = self.load()
				if response["error"] != None: return response
			response = self.check(default=self.default)
			if response["error"] != None: return response

		# success.
		response = utils.__default_response__()
		response["success"] = True
		response["message"] = f"Successfully initialized encrypted dictionary [{self.file_path.path}]."
		return response
		#
	def load(self):

		# decrypt.
		encrypted = self._file_.load()
		response = self.encryption.decrypt_string(encrypted, layers=self.layers)
		if response["error"] != None: return response
		decrypted = response["decrypted"]

		# handle.
		response = utils.__default_response__()
		try:
			self.dictionary = json.loads(decrypted)
			response["success"] = True
			response["message"] = f"Successfully loaded encrypted dictionary [{self.file_path.path}]."
			return response
		except: 
			self.dictionary = None
			response["error"] = f"Failed to load encrypted dictionary [{self.file_path.path}]."
			return response

		#
	def save(self, dictionary=None):

		# encrypt.
		if dictionary == None: dictionary = self.dictionary
		response = self.encryption.encrypt_string(
			json.dumps(dictionary, indent=4, ensure_ascii=False), 
			layers=self.layers)
		if response["error"] != None: return response
		encrypted = response["encrypted"]

		# handle.
		response = utils.__default_response__()
		try:
			self._file_.save(encrypted)
			response["success"] = True
			response["message"] = f"Successfully saved encrypted dictionary [{self.file_path.path}]."
			return response
		except: 
			self.dictionary = None
			response["error"] = f"Failed to save encrypted dictionary [{self.file_path.path}]."
			return response

		#
	def check(self, default=None, save=True):

		# checks.
		response = utils.__default_response__()
		if not isinstance(default, dict): 
			response["error"] = "Parameter [default] must be a dictionary."
			return response
		if not isinstance(self.dictionary, dict): 
			response["error"] = "The dictionary must be initialized & loaded."
			return response

		# handle.
		response = utils.__default_response__()
		try:
			old = ast.literal_eval(str(self.dictionary))
			self._dictionary_.dictionary = self.dictionary
			self.dictionary = self._dictionary_.check(default=default)
		except:
			response["error"] = "Failed to check the loaded dictionary."
			return response

		# save.
		response = utils.__default_response__()
		if save and old != self.dictionary:
			response = self.save()
			if response["error"] != None: 
				response["error"] = "Failed to check the loaded dictionary, error: "+response['error']
				return response

		# success.
		response["success"] = True
		response["message"] = f"Successfully saved encrypted dictionary [{self.file_path.path}]."
		return response
		
