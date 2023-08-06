# ssht00ls
Author(s):  Daan van den Bergh.<br>
Copyright:  © 2020 Daan van den Bergh All Rights Reserved.<br>
Supported Operating Systems: osx & linux.<br>
(linux required to convert smart card modes.)
<br>
<br>
<p align="center">
  <img src="https://github.com/vandenberghinc/storage/blob/master/images/logo.png?raw=true" alt="Bergh-Encryption" width="50"/>
</p>

## WARNING!
THIS REPO IS UNSTABLE AND UNDER DEVELOPMENT.


## Installation
Install the package.

	pip3 install ssht00ls --upgrade
Activate the ssht00ls alias.

	python3 -c 'import ssht00ls'

## Notes.
The executing user must be added to the "/etc/sudoers" to execute all functions without input interference, example:
<br>(Mostly for installation functions.)

	# The administrator client.
	administrator ALL = (ALL:ALL) NOPASSWD:ALL

## CLI Usage:
	Usage: ssht00ls <mode> <options> 
	Modes:
	    --create-alias : Create a ssh alias.
	        --server myserver : Specify the server's name.
	        --username myuser : Specify the username.
	        --ip 0.0.0.0 : Specify the server's ip.
	        --port 22 : Specify the server's port.
	        for ssh keys: : 
	        --key /path/to/key/private_key : Specify the path to the private key.
	        for smart cards: : 
	        --smart-cards : Enable the smart cards boolean.
	    -h / --help : Show the documentation.
	Author: Daan van den Bergh. 
	Copyright: © Daan van den Bergh 2020. All rights reserved.


## Python Examples.

### The Installation() object class.
The Installation() object class.  
```python

# import the package.
import ssht00ls

# check if ssh is correctly installed for the specified user.
# (leave the username None to use the current user.)
response = installation.check_installed(username=None)

# install the ssh correctly for the specified user.
if response["error"] != None:
	response = installation.install(username=None)

```

### The SmartCards() object class.
The SmartCards() object class.
(Supports the yubikey 5 series.)
```python

# import the package.
import ssht00ls

# scan for connected smart cards.
response = ssht00ls.smart_cards.scan()


```

### The SmartCard() object class.
The SmartCard() object class.
(Supports the yubikey 5 series.)
```python

# import the package.
import ssht00ls

# scan for connected smart cards.
response = ssht00ls.smart_cards.scan()

# select an initialized smart card object.
smart_card = response["smart_cards"]["10968447"]

# get information.
response = smart_card.get_info()

# install a new smart card.
# (warning: resets the smart card!)
response = smart_card.install()

# export the public keys.
response = smart_card.export_keys(
	# optionally save the keys to a file.
	path="/tmp/public_keys",)

# reset the smart card.
response = smart_card.reset_piv()

# change the pin code.
response = smart_card.change_pin(
	# the smart cards new puk code.
	new=123456, 
	# the smart cards old puk code.
	old=123456,)

# change the puk code.
response = smart_card.change_puk(
	# the smart cards new puk code.
	new=12345678, 
	# the smart cards old puk code.
	old=12345678,)

# unblock the pin code.
response = smart_card.unblock_pin(
	# the new pin code.
	pin=123456, 
	# the smart cards puk code
	puk=12345678,)

# generate a new key inside the smart card.
response = smart_card.generate_key(
	# the smart cards pin code.
	pin=123456, )

# generate a new management key inside the smart card.
response = smart_card.generate_management_key(
	# the smart cards pin code.
	pin=123456, )

# check if the yubikey is in the correct mode.
response = smart_card.check_smart_card()

# convert a yubikey into a piv smart card.
# (experimental)
response = smart_card.convert_to_smart_card()


```

### The SSHD() object class.
The SSHD() object class.  
```python

# import the package.
import ssht00ls

# create and optionally save a sshd configuration.
response = ssht00ls.sshd.create(
	# save the configuration & banner.
	save=False,
	# the ssh port.
	port=22,
	# the listen addresses.
	listen_addresses=[],
	# the server's banner.
	banner="Hello World!",
	# the allowed users & options.
	users={
		# define per user (all keys are optional).
		"administrator": {
			# the user's root permissions.
			"root_permissions":False,
			# authentication by password.
			"password_authentication":False,
			# authentication by keys.
			"key_authentication":True,
			# ip filter.
			"ip_filter":True,
			"allowed_ips":["192.168.1.201"],
			# sftp server only.
			"sftp_only":False,
			# the chroot directory (leave null to disable).
			"chroot_directory":None,
			# allowed connection options.
			"x11_forwarding":False,
			"tcp_forwarding":False,
		},
	},)

```

### The Key() object class.
The Key() object class.  
```python

# import the package.
import ssht00ls

# generate a key.
response = ssht00ls.key.generate(directory="/path/to/mykey/", passphrase="passphrase123!", comment="my key")

# edit the passphrase of a key.
response = ssht00ls.key.edit_passphrase(path="/path/to/mykey/private_key", new="Passphrase123!", old="passphrase123!")

```

### The Config() object class.
The Config() object class.  
```python

# import the package.
import ssht00ls

# create an ssh alias for the key.
response = ssht00ls.config.create_alias( 
	# the servers name.
	server="myserver", 
	# the username.
	username="administrator", 
	# the ip of the server.
	ip="0.0.0.0",
	# the port of the server.
	port=22,
	# the path to the private key.
	key="/path/to/mykey/private_key",
	# smart card.
	smart_card=False,
)
# if successfull you can use the ssh alias <username>.<server>
# $ ssh <username>.<server>

# create an ssh alias for a smart card.
response = ssht00ls.config.create_alias(
	# the servers name.
	server="myserver", 
	# the username.
	username="administrator", 
	# the ip of the server.
	ip="0.0.0.0",
	# the port of the server.
	port=22,
	# the path to the private key.
	key=smart_card.path,
	# smart card.
	smart_card=True,)

```

### The Agent() object class.
The Agent() object class. 
```python

# import the package.
import ssht00ls

# initialize the ssh agent.
response = ssht00ls.agent.initialize()

# delete all keys from the agent.
response = ssht00ls.agent.delete()

# add a key to the agent.
response = ssht00ls.agent.add(
	path="/path/to/mykey/private_key", 
	passphrase="TestPass!",)

# add a smart cards key to the agent.
response = ssht00ls.agent.add(
	path=smart_card.path, 
	smart_card=True,
	pin=123456,)

# check if a key is added to the agent.
response = ssht00ls.agent.check("/path/to/mykey/private_key")

# list all agent keys.
response = ssht00ls.agent.list()

```

### The SSH() object class.
The SSH() object class. 
<br>Make sure the key you are using is added to the ssh agent.
```python

# import the package.
import ssht00ls

# start a ssh session in the terminal console.
ssht00ls.ssh.session(alias="username.server")

# execute a command on the server over ssh.
response = ssht00ls.ssh.command(command=["echo", "$HOME"], alias="username.server")
# or without a created alias.
response = ssht00ls.ssh.command(
	# the command.
	command=["echo", "$HOME"], 
	# the ssh params.
	username="administrator", 
	ip="0.0.0.0", 
	port=22,
	key_path="/path/to/mykey/private_key",)

```

### The SSHFS() object class.
The SSHFS() object class. 
<br>Make sure the key you are using is added to the ssh agent.
```python

# import the package.
import ssht00ls

# mount a remote server directory.
response = ssht00ls.sshfs.mount(
	# the directory paths.
	server_path="/path/to/directory/", 
	client_path="/path/to/directory/", 
	# the ssh params.
	alias="administrator.myserver",)
	
# or without a created alias.
response = ssht00ls.sshfs.mount(
	# the directory paths.
	server_path="/path/to/directory/", 
	client_path="/path/to/directory/", 
	# the ssh params.
	username="administrator", 
	ip="0.0.0.0", 
	port=22,
	key_path="/path/to/mykey/private_key",)

# unmount a mounted directory.
response = ssht00ls.sshfs.unmount(
	client_path="/path/to/directory/", 
	forced=False,
	sudo=False,)

```

### The SCP() object class.
The SCP() object class. 
<br>Make sure the key you are using is added to the ssh agent.
```python

# import the package.
import ssht00ls

# download a server file or directory from a server.
response = ssht00ls.scp.download(
	# the file paths.
	server_path="/path/to/directory/", 
	client_path="/path/to/directory/",
	directory=True, 
	# the ssh params.
	username="administrator", 
	ip="0.0.0.0", 
	port=22,
	key_path="/path/to/mykey/private_key",)

# upload a file or directory to a server.
response = ssht00ls.scp.upload(
	# the file paths.
	server_path="/path/to/directory/", 
	client_path="/path/to/directory/",
	directory=True, 
	# the ssh params.
	username="administrator", 
	ip="0.0.0.0", 
	port=22,
	key_path="/path/to/mykey/private_key",)

```

### Response Object.
When a function completed successfully, the "success" variable will be "True". When an error has occured the "error" variable will not be "None". The function returnables will also be included in the response.

	{
		"success":False,
		"message":None,
		"error":None,
		"...":"...",
	}