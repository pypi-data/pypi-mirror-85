# Encrypti0n
Author(s):  Daan van den Bergh.<br>
Copyright:  © 2020 Daan van den Bergh All Rights Reserved.<br>
Supported Operating Systems: osx & linux.<br>
<br>
<br>
<p align="center">
  <img src="https://github.com/vandenberghinc/storage/blob/master/images/logo.png?raw=true" alt="Bergh-Encryption" width="50"/>
</p>


## Installation:

	pip3 install encrypti0n  --upgrade

## CLI:
	Usage: encryption <mode> <options> 
	Modes:
	    --generate-keys : Generate a key pair.
	    --encrypt /path/to/file : Encrypt the provided file path.
	    --decrypt /path/to/file : Decrypt the provided file path.
	    --create-alias : Create an alias.
	    -h / --help : Show the documentation.
	Options:
	    -k / --key /path/to/directory/ : Specify the path to the key's directory.
	    -p / --passphrase 'Passphrase123!Passphrase123!' : Specify the key's passphrase.
	    -l / --layers 1 : Specify encryption layers.
	Author: Daan van den Bergh 
	Copyright: © Daan van den Bergh 2020. All rights reserved.
	Usage at own risk.

## Python Examples.
Import the encryption package.
```python
# import the encryption object.
from encrypti0n import Encryption, EncryptedDictionary
```

### The Encryption class.
Initialize the encryption class (Leave the passphrase None if you require no passphrase).
```python
# initialize the encryption class.
encryption = Encryption(
	key='mykey/',
	passphrase='MyPassphrase123!')
```

Generating the keys.
```python
# generate the key pair.
response = encryption.generate_keys()
```

Load the generated keys before encrypting / decrypting.
```python
# load the key pair.
response = encryption.load_keys()
```

Edit the key's passphrase.
```python
# edit the key's passphrase.
response = encryption.edit_passphrase(passphrase="NewPassphrase123!")

```

Encrypting & decrypting files and strings.
```python

# encrypting & decrypting a file.
response = encryption.encrypt_file('file.txt', layers=1)
response = encryption.decrypt_file('file.txt', layers=1)

# encrypting & decrypting a string.
response = encryption.encrypt_string('hello world!', layers=1)
response = encryption.decrypt_string(response['encrypted'], layers=1)

```

Encrypting & decrypting directories.
```python

# encrypting & decrypting a directory.

# option 1: 
# (recursively encrypt each file in the directory).
response = encryption.encrypt_directory('directory/', recursive=True, layers=1)
response = encryption.decrypt_directory('directory/', recursive=True, layers=1)

# option 2:
# (create an encrypted zip of the directory and remove the directory).
response = encryption.encrypt_directory('directory/', layers=1)
response = encryption.decrypt_directory('directory/', layers=1)
```

### The EncryptedDictionary class.
The dictionary remains encrypted on file system while being decrypted in the local memory.
```python
# initialize the encrypted dictionary.
dictionary = EncryptedDictionary(
	# the file path.
	path="encrypted-dict.json", 
	# the dictionary.
	dictionary=None, 
	# specify default to check & create the dict.
	default={
		"hello":"world!"
	}, 
	# the key's path.
	key="mykey/",
	# the key's passphrase.
	passphrase='MyPassphrase123!',
	# the encryption layers.
	layers=1,)

# initialize the encryption.
response = dictionary.initialize()

# load the dict.
response = dictionary.load()
print(dictionary.dictionary)

# save the dict.
response = dictionary.save({"hello":"world!"})
# equal to.
dictionary.dictionary = {"hello":"world!"}
response = dictionary.save()

# check the dict.
response = dictionary.check(
	save=True,
	dictionary={
		"hello":"world!"
		"foo":"bar",
	})
```

### Response Object.
When a function completed successfully, the "success" variable will be "True". When an error has occured the "error" variable will not be "None". The function returnables will also be included in the response.

	{
		"success":False,
		"message":None,
		"error":None,
		"...":"...",
	}