#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# imports.
from ssht00ls.v1.classes.config import *
from ssht00ls.v1.classes import utils
from ssht00ls.v1.classes.smart_cards import smart_cards

# the installation object class.
class Installation(object):
	def __init__(self):
		a=1
	def install(self, 
		# optional define the user (leave None for current user).
		username=None,
	):
		# initialize.
		response = utils.__default_response__()
		if username == None: username = OWNER
		home = f"{HOME_BASE}/{username}/"	
		sudo = True
		
		# users ssh directory.
		fp = Formats.FilePath(f"{home}.ssh/")
		if not fp.exists(sudo=sudo):
			fp.create(
				directory=True,
				permission=700,
				owner=username,
				group=None,
				sudo=sudo,)
		else:
			fp.permission.set(permission=700, sudo=sudo)
			fp.ownership.set(owner=username, group=None, sudo=sudo)

		# the ssh config.
		fp = Formats.FilePath(f"{home}.ssh/config")
		if not fp.exists(sudo=sudo):
			fp.create(
				directory=False,
				data="",
				permission=644,
				owner=username,
				group=None,
				sudo=sudo,)
		else:
			fp.permission.set(permission=644, sudo=sudo)
			fp.ownership.set(owner=username, group=None, sudo=sudo)

		# the ssh known hosts.
		fp = Formats.FilePath(f"{home}.ssh/known_hosts")
		if not fp.exists(sudo=sudo):
			fp.create(
				directory=False,
				data="",
				permission=644,
				owner=username,
				group=None,
				sudo=sudo,)
		else:
			fp.permission.set(permission=644, sudo=sudo)
			fp.ownership.set(owner=username, group=None, sudo=sudo)

		# authorized keys.
		fp = Formats.FilePath(f"{home}.ssh/authorized_keys")
		if not fp.exists(sudo=sudo):
			fp.create(
				directory=False,
				data="",
				permission=600,
				owner=username,
				group=None,
				sudo=sudo,)
		else:
			fp.permission.set(permission=600, sudo=sudo)
			fp.ownership.set(owner=username, group=None, sudo=sudo)

		# success.
		response["success"] = True
		response["message"] = f"Successfully installed ssh for user [{username}]."
		return response

		#
	def check_installed(self, 
		# optional define the user (leave None for current user).
		username=None,
	):	

		# initialize.
		response = utils.__default_response__()
		if username == None: username = OWNER
		home = f"{HOME_BASE}/{username}/"	
		sudo = True
		
		# users ssh directory.
		fp = Formats.FilePath(f"{home}.ssh/")
		if not fp.exists():
			response["error"] = f"Required ssh configuration file [{fp.path}] for user [{username}] is not installed."
			return response
		else:
			fp.permission.set(permission=700, sudo=sudo)
			fp.ownership.set(owner=username, group=None, sudo=sudo)

		# the ssh config.
		fp = Formats.FilePath(f"{home}.ssh/config")
		if not fp.exists():
			response["error"] = f"Required ssh configuration file [{fp.path}] for user [{username}] is not installed."
			return response
		else:
			fp.permission.set(permission=644, sudo=sudo)
			fp.ownership.set(owner=username, group=None, sudo=sudo)

		# the ssh known hosts.
		fp = Formats.FilePath(f"{home}.ssh/known_hosts")
		if not fp.exists():
			response["error"] = f"Required ssh configuration file [{fp.path}] for user [{username}] is not installed."
			return response
		else:
			fp.permission.set(permission=644, sudo=sudo)
			fp.ownership.set(owner=username, group=None, sudo=sudo)
			
		# authorized keys.
		fp = Formats.FilePath(f"{home}.ssh/authorized_keys")
		if not fp.exists():
			response["error"] = f"Required ssh configuration file [{fp.path}] for user [{username}] is not installed."
			return response
		else:
			fp.permission.set(permission=600, sudo=sudo)
			fp.ownership.set(owner=username, group=None, sudo=sudo)

		# success.
		response["success"] = True
		response["message"] = f"SSH is successfully installed for user [{username}]."
		return response
			
# the config object class.
class Config(object):
	def __init__(self):
		a=1
	def create_alias(self, 
		# the servers name.
		server=None, 
		# the users.
		username=None, 
		# the ip of the server.
		ip=None,
		# the port of the server.
		port=None,
		# the path to the private key.
		key=None,
		# smart card.
		smart_card=False,
	):
		
		# checks.
		success, response = utils.__check_parameters__({
			"server":server,
			"username":username,
			"ip":ip,
			"port":port,
			"key":key,
		}, empty_value=None)
		if not success: return response
		
		# disable key.
		path = f'{HOME}/.ssh/config'
		utils.__set_file_path_permission__(path, permission=755)
		try:
			data = utils.__load_file__(path)
		except:
			data = ""
			if not os.path.exists(f'{HOME}/.ssh'):
				os.mkdir(f'{HOME}/.ssh')
				os.system("chmod 700 "+f'{HOME}/.ssh')
		
		# create config.
		tag = f'# ID: {username}@{server} '+'{'
		config = f"\n{tag}"
		config += f"\nHost {username}.{server}"
		config += "\n    HostName {}".format(ip)
		config += "\n    Port {}".format(port)
		config += "\n    User {}".format(username)
		config += "\n    ForwardAgent yes"
		config += "\n    PubKeyAuthentication yes"
		#config += "\n    IdentitiesOnly yes"
		if not smart_card:
			config += "\n    IdentityFile {}".format(key)
		else:
			config += "\n    PKCS11Provider {}".format(key)
		config += "\n# }\n"
		if tag not in data:
			data += config
			utils.__save_file__(path, data)
		else:
			c, d, set = 0, "", False
			for line in data.split('\n'):
				if line not in ['']:
					if tag in line:set = True
					elif set:
						if "# }" in line: set = False
					else: d += line+"\n"
			data = str(d)
			data += config
			utils.__save_file__(path, data)
		utils.__set_file_path_permission__(path, permission=644)

		# response.
		response["success"] = True
		response["message"] = f"Successfully created a ssh config for client [{username}@{server}] (host alias: {username}.{server})."
		return response
	def check_keys(self, username=None, public_keys=[], reversed=False):

		# check if already present.
		if username == None: username = OWNER
		ssh_dir = Formats.FilePath(f"{HOME_BASE}/{username}/.ssh/", check_existance=False)
		auth_keys = Formats.FilePath(f"{HOME_BASE}/{username}/.ssh/authorized_keys", check_existance=False)
		output = self.__load_keys__(username)
		for key in public_keys:
			key = key.replace("\n", "")
			if key not in [""]:
				if not reversed and key not in output:
					ssh_dir.permission.set(permission=700, sudo=True, silent=True) # silent for when non existant.
					auth_keys.permission.set(permission=600, sudo=True, silent=True) # silent for when non existant.
					auth_keys.ownership.set(owner=username, sudo=True)
					ssh_dir.ownership.set(owner=username, sudo=True)
					return r3sponse.error_response(f'Public key [{key}] is not activated.')
				if reversed and key in output:
					ssh_dir.permission.set(permission=700, sudo=True, silent=True) # silent for when non existant.
					auth_keys.permission.set(permission=600, sudo=True, silent=True) # silent for when non existant.
					auth_keys.ownership.set(owner=username, sudo=True)
					ssh_dir.ownership.set(owner=username, sudo=True)
					return r3sponse.error_response(f'Public key [{key}] is activated.')

		# set correct permission.
		ssh_dir.permission.set(permission=700, sudo=True, silent=True) # silent for when non existant.
		auth_keys.permission.set(permission=600, sudo=True, silent=True) # silent for when non existant.
		auth_keys.ownership.set(owner=username, sudo=True)
		ssh_dir.ownership.set(owner=username, sudo=True)

		# success.
		if not reversed:
			return r3sponse.success_response(f'Successfully confirmed that the specfied {len(public_keys)} public key(s) are activated.')
		else:
			return r3sponse.success_response(f'Successfully confirmed that the specfied {len(public_keys)} public key(s) are not activated.')
	def enable_keys(self, username=None, public_keys=[]):

		# check if already present.
		if username == None: username = OWNER
		output = self.__load_keys__(username)
		new_keys = []
		for key in public_keys:
			key = key.replace("\n", "")
			if key not in [""]:
				if key not in output:
					output.append(key)
		self.__save_keys__(username, output)

		# check if added.
		response = self.check_keys(username, public_keys)
		if response["error"] != None: return response
	
		# success.
		return r3sponse.success_response(f'Successfully enabled {len(public_keys)} public key(s).')

		#
	def disable_keys(self, username=None, public_keys=[]):

		# check if already present.
		if username == None: username = OWNER
		output = self.__load_keys__(username)
		new_keys = []
		for key in output:
			key = key.replace("\n", "")
			if key not in [""]:
				if key not in public_keys: new_keys.append(key)
		self.__save_keys__(username, new_keys)

		# check if added.
		response = self.check_keys(username, public_keys, reversed=True)
		if response["error"] != None: return response
	
		# success.
		return r3sponse.success_response(f'Successfully disabled {len(public_keys)} public key(s).')

		#
	def __load_keys__(self, username):

		# make readable.
		if username == None: username = OWNER
		sudo = OWNER != username or True
		ssh_dir = Formats.FilePath(f"{HOME_BASE}/{username}/.ssh/", check_existance=False)
		auth_keys = Formats.FilePath(f"{HOME_BASE}/{username}/.ssh/authorized_keys", check_existance=False)

		# checks.
		if not ssh_dir.exists(sudo=sudo):
			ssh_dir.create(
				directory=True,
				permission=770,
				owner=username,
				group=None,
				sudo=sudo,)
		if not auth_keys.exists(sudo=sudo):
			auth_keys.create(
				directory=False,
				data="",
				permission=770,
				owner=username,
				group=None,
				sudo=sudo,)

		ssh_dir.permission.set(permission=770, sudo=sudo, silent=True) # silent for when non existant.
		auth_keys.permission.set(permission=770, sudo=sudo, silent=True) # silent for when non existant.
		auth_keys.ownership.set(owner=OWNER, sudo=sudo)
		ssh_dir.ownership.set(owner=OWNER, sudo=sudo)

		if sudo: command = ["sudo"]
		else: command = []
		output = utils.__execute__(command + ["cat", f"{HOME_BASE}/{username}/.ssh/authorized_keys"], return_format="array")
		return output

		#
	def __save_keys__(self, username, public_keys):

		# make readable.
		if username == None: username = OWNER
		sudo = OWNER != username or True
		ssh_dir = Formats.FilePath(f"{HOME_BASE}/{username}/.ssh/", check_existance=False)
		auth_keys = Formats.FilePath(f"{HOME_BASE}/{username}/.ssh/authorized_keys", check_existance=False)

		# checks.
		if not ssh_dir.exists(sudo=sudo):
			ssh_dir.create(
				directory=True,
				permission=770,
				owner=username,
				group=None,
				sudo=sudo,)
		if not auth_keys.exists(sudo=sudo):
			auth_keys.create(
				directory=False,
				data="",
				permission=770,
				owner=username,
				group=None,
				sudo=sudo,)

		f = Files.File(path="/tmp/file")
		new = []
		for public_key in public_keys:
			new.append(public_key.replace("\n",''))
		f.save(Files.Array(path=False, array=new).string(joiner="\n"))
		os.system(f"sudo mv {f.file_path.path} {auth_keys.path}")

		ssh_dir.permission.set(permission=700, sudo=sudo, silent=True) # silent for when non existant.
		auth_keys.permission.set(permission=600, sudo=sudo, silent=True) # silent for when non existant.
		auth_keys.ownership.set(owner=OWNER, sudo=sudo)
		ssh_dir.ownership.set(owner=OWNER, sudo=sudo)

		#

# the ssh key object class.
class Key(object):
	def __init__(self):

		# variables.
		a = 1

		#
	def edit_passphrase(self, path=None, old=None, new=None):

		# checks.
		success, response = utils.__check_parameter__(old, "old", None)
		if not success: return response
		success, response = utils.__check_parameter__(new, "new", None)
		if not success: return response
		success, response = utils.__check_parameter__(path, "path", None)
		if not success: return response
		
		# do.
		output = utils.__execute__(["ssh-keygen", "-p", "-P", old, "-N", new, "-f", path])

		# check fails.
		if "incorrect passphrase supplied" in output:
			response["error"] = f"Provided an incorrect passphrase for key [{path}]."
			return response
		elif "No such file or directory" in output:
			response["error"] = f"Key [{path}] does not exist."
			return response
		
		# check success.	
		elif "Your identification has been saved with the new passphrase" in output:
			response["success"] = True
			response["message"] = f"Successfully edited the passphrase of key [{path}]."
			return response

		# unknown.
		else:
			l = f"Failed to edit the passphrase of key [{path}]"
			response["error"] = (f"{l}, error: "+output.replace("\n", ". ").replace(". .", ".")+".)").replace(". .",".").replace("\r","").replace("..",".")
			return response

			
		
		#
	def generate(self, directory=None, passphrase=None, comment=""):

		# checks.
		success, response = utils.__check_parameter__(directory, "directory", None)
		if not success: return response

		# check arguments.
		if passphrase in [None, False]:
			passphrase = '""'

		# create dir.
		if os.path.exists(directory): 
			response["error"] = f"Key directory [{directory}] already exists."
			return response
		else:
			os.mkdir(directory)
			utils.__set_file_path_permission__(directory, permission=700, sudo=True)
			utils.__set_file_path_ownership__(directory, owner=os.environ.get("USER"), group=None, sudo=True)

		# options.
		private_key = f'{directory}/private_key'
		public_key = f'{directory}/public_key'
		identity_file = f'-f {private_key}'
		if comment == None: comment = ""
		if "[#id:" not in comment: comment += f" [#id:{utils.__generate_shell_string__(characters=48, numerical_characters=True, special_characters=True)}]"
		comment = '-C "{}"'.format(comment)
		passphrase = '-N '+utils.__string_to_bash__(passphrase)

		# execute.
		os.system(f'ssh-keygen -q -v -o -a 100 -t ed25519 {passphrase} {identity_file} {comment}')
		if not os.path.exists(private_key): 
			utils.__delete_file_path__(directory, forced=True, sudo=True)
			response["error"] = f"Failed to generate key [{directory}]."
			return response

		# permissions.
		utils.__set_file_path_permission__(private_key, permission=600, sudo=True)
		utils.__set_file_path_ownership__(private_key, owner=os.environ.get("USER"), group=None, sudo=True)
		os.system(f"mv {private_key}.pub {public_key}")
		if not os.path.exists(public_key): 
			utils.__delete_file_path__(directory, forced=True, sudo=True)
			response["error"] = f"Failed to move private key [{private_key}]."
			return response
		utils.__set_file_path_permission__(public_key, permission=640, sudo=True)
		utils.__set_file_path_ownership__(public_key, owner=os.environ.get("USER"), group=None, sudo=True)

		# response.
		response["success"] = True
		response["message"] = f"Successfully generated key [{directory}]."
		return response

		#

# the sshfs object class.
class SSH(object):
	def __init__(self):

		# variables.
		a = 1

		#
	def session(self, 
		# the ssh parameters.
		#    option 1:
		alias=None,
		#    option 2:
		username=None, 
		ip=None, 
		port=22,
		key_path=None,
	):

		# build base.
		base = self.__build__(
			alias=alias,
			username=username, 
			ip=ip, 
			port=port,
			key_path=key_path,)

		# execute.
		command = base

		# do.
		os.system(utils.__array_to_string__(command, joiner=" "))

		#
	def command(self, 
		# the function parameters.
		command=["ls"], 
		# the return format: string / array
		return_format="string",
		# the ssh parameters.
		#    option 1:
		alias=None,
		#    option 2:
		username=None, 
		ip=None, 
		port=22,
		key_path=None,
	):

		# build base.
		base = self.__build__(
			alias=alias,
			username=username, 
			ip=ip, 
			port=port,
			key_path=key_path,)
		
		# execute.
		command = base

		# do.
		output = utils.__execute__(command, shell=False, return_format=return_format)
		#output = utils.__execute_script__(utils.__array_to_string__(command, joiner="\n"), shell=False, return_format=return_format)
		

		response = utils.__default_response__()
		
		# uncaptured error.
		s = ""
		if len(output) >= 1 and len(output[0]) >= len('ssh: '):
			for i in range(len('ssh: ')):
				s += output[0][i]
		if s == "ssh: ":
			error = output.split('ssh: ')[1]
			response["error"] = f"Error: {error}."
			return response

		# unkown host.
		elif "Could not resolve hostname " in output:
			hostname = output.split('Could not resolve hostname ')[1].split(":")[0]
			response["error"] = f"Invalid hostname [{hostname}]."
			return response
	
		else:
			response["success"] = True
			response["message"] = f"Successfully executed command [$ {utils.__array_to_string__(command ,joiner=' ')}]."
			response["output"] = output
			return response
		
		#		
	# system functions.
	def __build__(self,
		# option 1:
		alias=None,
		# option 2:
		username=None, 
		ip=None, 
		port=22,
		key_path=None,
	):
		base = []
		if alias != None:
			return base + ['ssh', alias]
		else:
			base += ['ssh']
			if key_path != None: base += ['-i', key_path,]
			if port != None: base += ['-p', port,]
			base += [f"{username}@{ip}"]
			return base

# the sshfs object class.
class SSHFS(object):
	def __init__(self):

		# variables.
		a = 1

		#
	def mount(self, 
		# the directory paths.
		server_path=None, 
		client_path=None, 
		# the ssh params.
		# option 1:
		alias=None,
		# option 2:
		username=None, 
		ip=None, 
		port=22,
		key_path=None,
	):

		# checks.
		base = []
		if alias == None:
			success, response = utils.__check_parameters__(empty_value=None, parameters={
				"username":username,
				"ip":ip,
				"server_path":server_path,
				"client_path":client_path,
				"key_path":key_path,
				"port":port,
			})
			if not success: return response
			base += ["sshfs"]
		else:
			success, response = utils.__check_parameters__(empty_value=None, parameters={
				"alias":alias,
				"server_path":server_path,
				"client_path":client_path,
			})
			if not success: return response
			base += ["sshfs", "-p", str(port), "-o", f"IdentityFile={key_path}"]
			alias = f'{username}@{ip}'

		# do.
		output = utils.__execute__(base + [f'{alias}:{server_path}', client_path])
		#output = utils.__execute_script__(utils.__array_to_string__(base + [f'{alias}:{server_path}', client_path], joiner="\n"))

		# check fails.
		if "mount_osxfuse: mount point " in output and "is itself" in output:
			response["error"] = f"Client path [{client_path}] is already mounted."
			return response
		elif "No such file or directory" in output:
			response["error"] = f"Server path [{server_path}] does not exist."
			return response
		elif "" == output:
			if not os.path.exists(client_path):
				response["error"] = f"Could not connect with server [{alias}]."
				return response
			# check success.	
			else:
				response["success"] = True
				response["message"] = f"Successfully mounted directory [{client_path}]."
				return response

		# unknown.
		else:
			l = f"Failed to mount directory [{client_path}]"
			response["error"] = (f"{l}, error: "+output.replace("\n", ". ").replace(". .", ".")+".)").replace(". .",".").replace("\r","").replace("..",".")
			return response
		
		#		
	def unmount(self, 
		# the client path.
		client_path=None, 
		# the forced umount option.
		forced=False, 
		# forced option may require sudo.
		sudo=False,
	):

		# checks.
		success, response = utils.__check_parameter__(client_path, "client_path", None)
		if not success: return response
		command = []
		if sudo: command.append("sudo")
		command += ["umount"]
		if forced: command.append("-f")
		command += [client_path]
		output = utils.__execute__(command=command)
		if output != "":
			l = f"Failed to unmount directory [{client_path}]."
			response["error"] = (f"{l}, error: "+output.replace("\n", ". ").replace(". .", ".")+".)").replace(". .",".").replace("\r","").replace("..",".")
			return response
		else:
			response["success"] = True
			response["message"] = f"Successfully unmounted directory [{client_path}]."
			return response
		#
	
# the scp object class.
class SCP(object):
	def __init__(self):

		# variables.
		a = 1

		#
	def download(self, 
		# the file paths.
		server_path=None, 
		client_path=None,
		directory=False, 
		# the ssh params.
		# option 1:
		alias=None,
		# option 2:
		username=None, 
		ip=None, 
		port=22,
		key_path=None,
	):

		# checks.
		if alias == None:
			success, response = utils.__check_parameters__(empty_value=None, parameters={
				"username":username,
				"ip":ip,
				"server_path":server_path,
				"client_path":client_path,
				"key_path":key_path,
				"port":port,
			})
			if not success: return response
		else:
			success, response = utils.__check_parameters__(empty_value=None, parameters={
				"alias":alias,
				"server_path":server_path,
				"client_path":client_path,
			})
			if not success: return response

		# check client path.
		if os.path.exists(client_path):
			response["error"] = f"Client path [{client_path}] already exists."
			return response

		# do.
		command = self.__build__(
			alias=alias,
			port=port,
			key_path=key_path,)
		if directory: command += ["-r"]
		if alias == None: alias = f'{username}@{ip}'
		output = utils.__execute__(command + [f'{alias}:{server_path}', client_path], shell=False)
		#output = utils.__execute_script__(utils.__array_to_string__(command + [f'{alias}:{server_path}', client_path], joiner="\n"), shell=False)
		
		# check fails.
		if "No such file or directory" in output:
			response["error"] = f"Server path [{server_path}] does not exist."
			return response
		elif "not a regular file" in output:
			response["error"] = f"Server path [{server_path}] is a directory."
			return response
		elif "" == output:
			if not os.path.exists(client_path):
				response["error"] = f"Failed to download [{server_path}]."
				return response
			# check success.	
			else:
				response["success"] = True
				response["message"] = f"Successfully downloaded [{server_path}]."
				return response
		# unknown.
		else:
			l = f"Failed to download [{client_path}]"
			response["error"] = (f"{l}, error: "+output.replace("\n", ". ").replace(". .", ".")+".)").replace(". .",".").replace("\r","").replace("..",".")
			return response
		
		#
	def upload(self, 
		# the file paths.
		server_path=None, 
		client_path=None,
		directory=False, 
		# the ssh params.
		# option 1:
		alias=None,
		# option 2:
		username=None, 
		ip=None, 
		port=22,
		key_path=None,
	):

		# checks.
		if alias == None:
			success, response = utils.__check_parameters__(empty_value=None, parameters={
				"username":username,
				"ip":ip,
				"server_path":server_path,
				"client_path":client_path,
				"key_path":key_path,
				"port":port,
			})
			if not success: return response
		else:
			success, response = utils.__check_parameters__(empty_value=None, parameters={
				"alias":alias,
				"server_path":server_path,
				"client_path":client_path,
			})
			if not success: return response

		# check client path.
		if not os.path.exists(client_path):
			response["error"] = f"Client path [{client_path}] does not exist."
			return response

		# do.
		command = self.__build__(
			alias=alias,
			port=port,
			key_path=key_path,)
		if directory: command += ["-r"]
		if alias == None: alias = f'{username}@{ip}'
		output = utils.__execute__(command + [client_path, f'{alias}:{server_path}'], shell=False)
		#output = utils.__execute_script__(utils.__array_to_string__(command + [client_path, f'{alias}:{server_path}'], joiner="\n"), shell=False)

		# check fails.
		if "No such file or directory" in output:
			response["error"] = f"The base path [{Formats.FilePath(server_path).base()}] of the specified file does not exist on the server."
			return response
		elif "not a regular file" in output:
			response["error"] = f"Client path [{client_path}] is a directory."
			return response
		elif "" == output:
			response["success"] = True
			response["message"] = f"Successfully uploaded [{client_path}]."
			return response
		# unknown.
		else:
			l = f"Failed to upload [{client_path}]"
			response["error"] = (f"{l}, error: "+output.replace("\n", ". ").replace(". .", ".")+".)").replace(". .",".").replace("\r","").replace("..",".")
			return response
		
		#
	# system functions.
	def __build__(self,
		# option 1:
		alias=None,
		# option 2:
		port=22,
		key_path=None,
	):	
		base = []
		if alias != None:
			return base + ['scp']
		else:
			base += ['scp']
			if key_path != None: base += ['-i', key_path,]
			if port != None: base += ['-P', port,]
			return base
	
# the ssh agent object class.
class Agent(object):
	def __init__(self):

		# variables.
		#self.initialize()
		
		# set agent.
		self.SSH_AUTH_SOCK = os.environ.get("SSH_AUTH_SOCK")
		self.SSH_AGENT_PID = os.environ.get("SSH_AGENT_PID")
		if self.SSH_AUTH_SOCK == None or self.SSH_AGENT_PID == None:
			output = subprocess.check_output(["ssh-agent"]).decode()
			self.SSH_AUTH_SOCK = output.split("SSH_AUTH_SOCK=")[1].split(";")[0]
			self.SSH_AGENT_PID = output.split("SSH_AGENT_PID=")[1].split(";")[0]
			os.environ["SSH_AUTH_SOCK"] = self.SSH_AUTH_SOCK
			os.environ["SSH_AGENT_PID"] = self.SSH_AGENT_PID
		
		#
	def add(self, 
		# the keys path.
		path=None, 
		# the keys passphrase.
		passphrase=None, 
		# enable if you are using a smart card.
		smart_card=False, 
		# the smart cards pin code
		pin=None, 
		# default timeout (do not use).
		timeout=0.5,
		# reattempt (do not use).
		reattempt=True,
	):

		# initialize.
		path = path.replace("//", "/")
		response = utils.__default_response__()
		success, response = utils.__check_parameters__(empty_value=None, parameters={
			"path":path
		})
		if not success: return response
		if smart_card:
			success, response = utils.__check_parameters__(empty_value=None, parameters={
				"pin":pin
			})
			if not success: return response
		else:
			if not os.path.exists(path):
				response["error"] = f"Key path [{path}] does not exist."
				return response

		# check agent connection.
		output = utils.__execute__(["ssh-add", "-L"])
		if "Failed to communicate" in output or "agent refused operation" in output or "Error connecting to agent" in output or "Connection refused" in output:
			if reattempt:
				try:
					output = utils.__execute__([f"ssh-add", "-D"])
				except: a=1
				try:
					output = utils.__execute__([f"ssh-add", "-k"])
				except: a=1
				try:
					output = utils.__execute__(f"ssh-agent")
					try: 
						SSH_AUTH_SOCK = output.split("SSH_AUTH_SOCK=")[1].split(";")[0]
						os.environ["SSH_AUTH_SOCK"] = SSH_AUTH_SOCK
					except: a=1
					try: 
						SSH_AGENT_PID = output.split("SSH_AGENT_PID=")[1].split(";")[0]
						os.environ["SSH_AGENT_PID"] = SSH_AGENT_PID
					except: a=1
				except: a=1
				return self.add(
					# the keys path.
					path=path,
					# the keys passphrase.
					passphrase=passphrase,
					# enable if you are using a smart card.
					smart_card=smart_card,
					# the smart cards pin code
					pin=pin,
					# default timeout (do not use).
					timeout=timeout,
					# reattempt (do not use).
					reattempt=False,
				)
			else:
				return r3sponse.error_response("Failed to communicate with the ssh-agent. Try logging out the current system user & logging back in (or execute [$ eval `ssh-agent`]).")

		# with passphrase.
		response = utils.__default_response__()
		if smart_card or passphrase != None:
			#self.initialize()
			if smart_card:
				path = smart_cards.path
				if OS in ["osx"]:
					os.system(f"rm -fr {smart_cards.path}")
					os.system(f"cp {smart_cards.original_path} {smart_cards.path}")
					os.system(f"chmod 644 {smart_cards.path}")
				#file = Files.File(path="/tmp/shell.sh")
				#file.save(f'export SSH_AUTH_SOCK={self.SSH_AUTH_SOCK}\nexport SSH_AGENT_PID={self.SSH_AGENT_PID}\nssh-add -e {path}\nssh-add -s {path}')
				#file.save(f'ssh-add -e {path}\nssh-add -s {path}')
				#file.save(f'ssh-add -s {path}')
				#file.file_path.permission.set(755)
				#spawn = pexpect.spawn(f'sh {file.file_path.path}')
				#file.file_path.delete(forced=True)
				#spawn = pexpect.spawn(f'ssh-add -e {path} && ssh-add -s {path}')
				try:
					output = subprocess.check_output([f"ssh-add", "-e", f"{path}"])
					print("remove card output:",output)
				except: a=1
				spawn = pexpect.spawn(f'ssh-add -s {path}')
			else:
				#file = Files.File(path="/tmp/shell.sh")
				#file.save(f'export SSH_AUTH_SOCK={self.SSH_AUTH_SOCK}\nexport SSH_AGENT_PID={self.SSH_AGENT_PID}\nssh-add {path}')
				#file.file_path.permission.set(755)
				#spawn = pexpect.spawn(f'sh {file.file_path.path}')
				#file.file_path.delete(forced=True)
				spawn = pexpect.spawn(f'ssh-add {path}')

			# send lines.
			output = None
			try:

				# handle pincode.
				if smart_card:
					spawn.expect(
						f'Enter passphrase for PKCS#11:',
						timeout=timeout,
					)
					spawn.sendline(str(pin))
				
				# handle pass.
				else:
					spawn.expect(
						f'Enter passphrase for {path}:',
						timeout=timeout,
					)
					spawn.sendline(passphrase)

			except pexpect.exceptions.TIMEOUT:
				a=1
			except pexpect.exceptions.EOF:
				a=1
			
			# handle output.
			output = spawn.read().decode()

			# check success.
			if "incorrect passphrase" in output.lower():
				return r3sponse.error_response("Provided an incorrect passphrase.")
			elif "incorrect pin" in output.lower():
				return r3sponse.error_response("Provided an incorrect pin code.")
			elif "Failed to communicate" in output or "agent refused operation" in output or "Error connecting to agent" in output or "Connection refused" in output:
				if reattempt:
					try:
						output = utils.__execute__([f"ssh-add", "-D"])
					except: a=1
					try:
						output = utils.__execute__([f"ssh-add", "-k"])
					except: a=1
					try:
						output = utils.__execute__(f"ssh-agent")
						try: 
							SSH_AUTH_SOCK = output.split("SSH_AUTH_SOCK=")[1].split(";")[0]
							os.environ["SSH_AUTH_SOCK"] = SSH_AUTH_SOCK
						except: a=1
						try: 
							SSH_AGENT_PID = output.split("SSH_AGENT_PID=")[1].split(";")[0]
							os.environ["SSH_AGENT_PID"] = SSH_AGENT_PID
						except: a=1
					except: a=1
					return self.add(
						# the keys path.
						path=path,
						# the keys passphrase.
						passphrase=passphrase,
						# enable if you are using a smart card.
						smart_card=smart_card,
						# the smart cards pin code
						pin=pin,
						# default timeout (do not use).
						timeout=timeout,
						# reattempt (do not use).
						reattempt=False,
					)
				else:
					return r3sponse.error_response("Failed to communicate with the ssh-agent. Try logging out the current system user & logging back in (or execute [$ eval `ssh-agent`]).")
			elif "Identity added:" in output or "Card added:" in output: 
				return r3sponse.success_response(f"Successfully added key [{path}] to the ssh agent.")
			elif output != "": 
				return r3sponse.error_response(f"Failed to add key [{path}] to the ssh agent, error: {output}")
			else: 
				return r3sponse.error_response(f"Failed to add key [{path}] to the ssh agent.")

			# handle eof.
			"""try:
				spawn.expect(pexpect.EOF, timeout=timeout)
			except pexpect.ExceptionPexpect as epe:
				response["error"] = f"Failed to add key [{path}] to the ssh agent #3."
				return response"""

		# without pass.
		else:
			output = utils.__execute__(command=["ssh-add", path], shell=False, timeout=timeout)

			# check success.
			if "Failed to communicate" in output or "agent refused operation" in output or "Error connecting to agent" in output or "Connection refused" in output:
				return r3sponse.error_response("Failed to communicate with the ssh-agent.")
			elif "Identity added:" in output: 
				return r3sponse.success_response(f"Successfully added key [{path}] to the ssh agent.")
			else: 
				return r3sponse.error_response(f"Failed to add key [{path}] to the ssh agent.")

		#
	def delete(self):

		# initialize.
		response = utils.__default_response__()

		# delete keys.
		output = utils.__execute__(command=["ssh-add", "-D"])

		# check success.
		if "Could not open a connection to your authentication agent." in output:
			response["error"] = "Failed to communicate with the ssh-agent."
			return response
		elif "All identities removed." in output: 
			response["success"] = True
			response["message"] = f"Successfully removed all keys from the ssh agent."
			return response
		else: 
			response["message"] = f"Failed to remove all keys from the ssh agent."
			return response

		#
	def list(self):
		# initialize.
		response = utils.__default_response__()

		# list keys.
		output = utils.__execute__(command=["ssh-add", "-l"], return_format="array")
		if "Failed to communicate" in output:
			response["error"] = "Failed to communicate with the ssh-agent."
			return response
		elif "The agent has no identities." in output:
			response["keys"] = []
		else:
			response["keys"] = output
		return response

		#
	def check(self, public_key=None):
		
		# initialize.
		response = utils.__default_response__()		

		# params.
		success, response = utils.__check_parameter__(public_key, "public_key", None)
		if not success: return response

		# checks.
		if not os.path.exists(public_key):
			response["error"] = f"Public key path [{public_key}] does not exist."
			return response

		# load public key.
		try:
			public_key = utils.__load_file__(public_key)
		except:
			response["error"] = f"Failed to load public key path [{public_key}]."
			return response

		# retrieve id from public key.
		try:
			public_key_id = public_key.split("[#id:")[1].split("]")[0]
		except IndexError:
			response["error"] = f"Public key [{public_key}] does not contain any id."
			return response

		# list.
		response = self.list()
		if response["error"] != None: return response
		success = False
		for key in response["keys"]:
			try:
				l_id = key.split("[#id:")[1].split("]")[0]
				if l_id == public_key_id:
					success = True 
					break
			except IndexError: a=1

		# success.
		response = utils.__default_response__()		
		if success:
			response["success"] = True
			response["message"] = f"Public key [{public_key}] is added to the ssh agent."
		else:
			response["error"] = f"Public key [{public_key}] is not added to the ssh agent."
		return response

		#
	def initialize(self):

		# initialize.
		response = utils.__default_response__()

		# check communication.
		output = utils.__execute__(command=["ssh-add", "-l"])
		#print("DEBUG; initialize output ssh-add -l:",output)
		if "Failed to communicate" in output or "Error connecting to agent" in output:
			if not self.delete()["success"]:
				l = subprocess.check_output(['eval', '"$(ssh-agent)"'], shell=True).decode()
				output = utils.__execute__(command=["ssh-add", "-l"])
				if "Failed to communicate" in output or "Error connecting to agent" in output:
					response["error"] = "Failed to communicate with the ssh-agent."
					return response
				else:
					output = utils.__execute__(command=["ssh-add", "-l"])
					if "Failed to communicate" in output or "Error connecting to agent" in output:
						response["error"] = "Failed to communicate with the ssh-agent."
						return response
			else:
				output = utils.__execute__(command=["ssh-add", "-l"])
				if "Failed to communicate" in output or "Error connecting to agent" in output:
					response["error"] = "Failed to communicate with the ssh-agent."
					return response

		# success.
		response["success"] = True
		response["message"] = f"Successfully initialized the ssh agent."
		return response

# the sshd object class.
class SSHD(object):
	def __init__(self):
		a=1
	def create(self,
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
				"ip_filter":False,
				"allowed_ips":[],
				# sftp server only.
				"sftp_only":False,
				# the chroot directory (leave null to disable).
				"chroot_directory":None,
				# allowed connection options.
				"x11_forwarding":False,
				"tcp_forwarding":False,
			},
		},
	):

		# check users.
		response = self.__check_user_items__(users)
		if response["error"] != None: return response

		# check utils intalled (must be before __install_banner__).
		response = self.__check_utils_installed__(list(users.keys()))
		if response["error"] != None: return response

		# intall banner.
		if save:
			response = self.__install_banner__(banner=banner, usernames=list(users.keys()))
			if response["error"] != None: return response

		# defaults.
		configuration =  '# SSHD_CONFIG:'
		configuration += '\n# BY VANDENBERGHINC'
		configuration += '\n# MODULE: ssht00ls'
		configuration += '\n# AUTHOR: DAAN VAN DEN BERGH'
		configuration += '\nAcceptEnv LANG LC_*'
		configuration += '\nSubsystem sftp  internal-sftp'
		#configuration += '\nSubsystem sftp  /usr/libexec/sftp-server'
		configuration += '\nLoginGraceTime 60'
		configuration += '\nMaxAuthTries 3'
		configuration += '\nMaxSessions 10'
		configuration += "\nMaxStartups 999"
		configuration += '\nLogLevel VERBOSE'
		configuration += f'\nPort {port}'
		configuration += '\nProtocol 2'

		# defaults.
		configuration += '\nPermitRootLogin {}'.format("no")
		configuration += '\nStrictModes {}'.format("yes")
		configuration += '\nPermitUserEnvironment {}'.format("no")
		configuration += '\nIgnoreRhosts {}'.format("yes")
		configuration += '\nPermitTunnel {}'.format("no")
		configuration += '\nX11Forwarding {}'.format("no")
		configuration += '\nAllowTcpForwarding {}'.format("no")
		configuration += '\nAllowStreamLocalForwarding {}'.format("no")
		configuration += '\nGatewayPorts {}'.format("no")
		configuration += '\nPermitTTY {}'.format("yes")
		for listen_address in listen_addresses:
			configuration += f'\nListenAddress {listen_address}'

		# auth keys.
		configuration += '\nAuthorizedKeysFile {}'.format(".ssh/authorized_keys")

		# banner.
		configuration += '\nBanner .ssh/banner'

		# per users.
		configuration += '\nChallengeResponseAuthentication no'
		for username, info in users.items():
			configuration += f'\n# User: {username}'

			# ip filter.	
			configuration += f'\nMatch User {username}'

			# authentication by password.
			if info["password_authentication"]:
				configuration += '\n    PasswordAuthentication yes'
				configuration += '\n    PermitEmptyPasswords no'
			else:
				configuration += '\n    PasswordAuthentication no'
				configuration += '\n    PermitEmptyPasswords no'

			# authentication by keys.
			if info["key_authentication"]:
				configuration += '\n    PubkeyAuthentication {}'.format('yes')
			else:
				configuration += '\n    PubkeyAuthentication {}'.format('no')


			# chroot directory.
			if isinstance(info["chroot_directory"], str):
				configuration += f'\n    ChrootDirectory {info["chroot_directory"]}'

			# root permission.
			l = "no"
			if info["root_permissions"] and info["key_authentication"]: l = "prohibit-password"
			elif info["root_permissions"]: l = "yes"
			configuration += f'\n    PermitRootLogin {l}'

			# connection options.
			configuration += f'\n    X11Forwarding {self.__convert_boolean__(info["x11_forwarding"])}'
			configuration += f'\n    AllowTcpForwarding {self.__convert_boolean__(info["tcp_forwarding"])}'

			# default options.
			configuration += f'\n    PermitTunnel no'
			configuration += f'\n    AllowStreamLocalForwarding no'
			configuration += f'\n    GatewayPorts no'
			configuration += f'\n    PermitTTY yes'
			
			# check ip filter.
			if info["ip_filter"]:

				# match verified ips.
				configuration += f'\n    Match User {username} Address {self.__sum_list__(info["allowed_ips"])}'

				# check sftp only.
				if info["sftp_only"]:
					configuration += '\n        ForceCommand internal-sftp'

				# shell access.
				else:
					configuration += '\n        ForceCommand .ssh/utils/original.sh'

				# match unverified ips.
				configuration += f'\n    Match User {username} Address *,!{self.__sum_list__(info["allowed_ips"])}'
				configuration += f'\n        ForceCommand .ssh/utils/log.sh "Your ip address is not authorized." "Authorize your ip address to access user [{username}]."'

			# no ip filter.
			else:

				# check sftp only.
				if info["sftp_only"]:
					configuration += '\n    ForceCommand internal-sftp'

				# shell access.
				else:
					configuration += '\n    ForceCommand .ssh/utils/original.sh'

		# match none authorized users.
		#if '*all*' not in list(users.keys()):
		configuration += f'\nMatch User *,!{self.__sum_list__(list(users.keys()))}'
		configuration += '\n    PasswordAuthentication no'
		configuration += '\n    PermitEmptyPasswords no'
		configuration += '\n    PubkeyAuthentication no'
		configuration += f'\n    ForceCommand .ssh/utils/log.sh "You are not authorized to access user [$USER] over ssh."'
		configuration += "\n"

		# save sshd.
		if save:
			file = Files.File(path='/tmp/sshd_config', data=configuration)
			file.file_path.delete(forced=True, sudo=True)
			file.save()
			fp = Formats.FilePath(f"/etc/ssh/sshd_config")
			file.file_path.copy(fp.path, sudo=True)
			fp.permission.set(permission=644, sudo=True)
			fp.ownership.set(owner="root", group=None, sudo=True)
			os.system("sudo systemctl restart ssh")
			if not fp.exists(sudo=True):
				return r3sponse.error_response(f"Failed to save the sshd configuration.")

		# success.
		return r3sponse.success_response("Successfully created the sshd configuration.", {
				"sshd":configuration,
			})

		#
	# system functions.
	def __sum_list__(self, list):
		return Files.Array(path=False, array=list).string(joiner=',')
	def __convert_boolean__(self, boolean):
		if boolean: return "yes"
		else: return "no"
	def __check_user_items__(self, users):

		# iterate.
		for username, info in users.items():
			
			# check options.
			try: info["root_permissions"]
			except KeyError: info["root_permissions"] = True
			try: info["password_authentication"]
			except KeyError: info["password_authentication"] = False
			try: info["key_authentication"]
			except KeyError: info["key_authentication"] = True
			try: info["ip_filter"]
			except KeyError: info["ip_filter"] = False
			try: 
				info["allowed_ips"]
				if not isinstance(info["allowed_ips"], list):
					return r3sponse.error_response(f"Invalid usage, parameter [users.{username}.allowed_ips] is supposed to be a list with allowed ip addresses.")
			except KeyError: info["allowed_ips"] = []
			try: info["sftp_only"]
			except KeyError: info["sftp_only"] = False
			try: info["chroot_directory"]
			except KeyError: info["chroot_directory"] = None
			try: info["x11_forwarding"]
			except KeyError: info["x11_forwarding"] = False
			try: info["tcp_forwarding"]
			except KeyError: info["tcp_forwarding"] = False

		# response.
		return r3sponse.success_response("Successfully checked the user items.")

		#
	def __check_utils_installed__(self, usernames=[]):

		# iterate.
		if isinstance(usernames, str): usernames = [usernames]
		to_install = []
		for username in usernames:
			
			# non existant.
			fp = Formats.FilePath(f"{HOME_BASE}{username}/.ssh/utils/.version")
			if not fp.exists(sudo=True): 
				to_install.append(username)

			# check version.
			else: 
				version = utils.__execute__(["sudo", "cat", fp.path])
				github_version = utils.__execute__(["curl", "https://raw.githubusercontent.com/vandenberghinc/ssht00ls/master/ssht00ls/v1/classes/utils/.version?raw=true"])
				if str(version) != str(github_version):
					to_install.append(username)

		# install.
		if len(to_install) > 0:
			response = self.__install_utils__(to_install)
			if response["error"] != None: return response

		# success.
		return r3sponse.success_response("Successfully verified the ssht00ls utils installation.")

		#
	def __install_utils__(self, usernames=[]):

		# checks.
		if isinstance(usernames, str): usernames = [usernames]
		if len(usernames) == 0: 
			return r3sponse.error_response("No usernames specified.")

		# download.
		path = "/tmp/utils/"
		os.system(f"rm -fr {path}")
		os.system(f"rm -fr {HOME}/Downloads/ssht00ls/")
		os.system(f'git clone https://github.com/vandenberghinc/ssht00ls {HOME}/Downloads/ssht00ls/')
		if not os.path.exists(f"{HOME}/Downloads/ssht00ls/"):
			return r3sponse.error_response("Failed to install the ssht00ls utils. #1")
		os.system(f"mv {HOME}/Downloads/ssht00ls/ssht00ls/v1/classes/utils/ {path}")
		os.system(f"rm -fr {path}/__pycache__")
		os.system(f"rm -fr {path}/__init__.py")
		if not os.path.exists(path):
			return r3sponse.error_response("Failed to install the ssht00ls utils. #2")

		# iterate.
		for username in usernames:

			# check if ssh is correctly installed.
			response = installation.check_installed(username=username)

			# install the ssh correctly for the specified user.
			if response["error"] != None:
				response = installation.install(username=username)
				if response["error"] != None: return response

			# copy.
			fp = Formats.FilePath(f"{HOME_BASE}{username}/.ssh/utils/")
			os.system(f"sudo rm -fr {fp.path}")
			os.system(f"sudo cp -r {path} {fp.path}")
			fp.ownership.set(owner=username, group=None, sudo=True)
			fp.permission.set(permission=755, recursive=True, sudo=True)
			if not fp.exists(sudo=True):
				return r3sponse.error_response("Failed to install the ssht00ls utils. #3")

		# success.
		return r3sponse.success_response("Successfully installed the ssht00ls utils.")

		#
	def __install_banner__(self, banner="", usernames=[]):

		# checks.
		if isinstance(usernames, str): usernames = [usernames]
		if len(usernames) == 0: 
			return r3sponse.error_response("No usernames specified.")

		# save banner.
		file = Files.File(path='/tmp/banner', data=banner)
		file.file_path.delete(forced=True, sudo=True)
		file.save()

		# iterate.
		for username in usernames:
			fp = Formats.FilePath(f"/{HOME_BASE}{username}/.ssh/banner")
			file.file_path.copy(fp.path, sudo=True)
			fp.permission.set(permission=755, sudo=True)
			fp.ownership.set(owner=username, group=None, sudo=True)
			if not fp.exists(sudo=True):
				return r3sponse.error_response(f"Failed to install the banner for user [{username}].")

		# success.
		return r3sponse.success_response("Successfully installed the banner.")

		#
	#

# Initialized classes.
installation = Installation()
config = Config()
sshd = SSHD()
ssh = SSH()
sshfs = SSHFS()
scp = SCP()
agent = Agent()
key = Key()

"""

# --------------------
# SSH Installation.

# check if ssh is correctly installed.
# (leave the username None to use the current user.)
response = installation.check_installed(username=None)

# install the ssh correctly for the specified user.
if response["error"] != None:
	response = installation.install(username=None)

# --------------------
# SSHD Config.

# create and optionally save a sshd configuration.
response = sshd.create(
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

# --------------------
# SSH Key.

# generate a key.
response = key.generate(directory="/path/to/mykey/", passphrase="passphrase123!", comment="my key")

# edit the passphrase of a key.
response = key.edit_passphrase(path="/path/to/mykey/private_key", new="Passphrase123!", old="passphrase123!")

# --------------------
# SSH Config.

# create an ssh alias for the key.
response = config.create_alias(self, 
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
	smart_card=False,)
# if successfull you can use the ssh alias <username>.<server>
# $ ssh <username>.<server>

# create an ssh alias for a smart card.
response = config.create_alias(self, 
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

# --------------------
# SSH Agent.

# initialize the ssh agent.
response = agent.initialize()

# delete all keys from the agent.
response = agent.delete()

# add a key to the agent.
response = agent.add(
	path="/path/to/mykey/private_key", 
	passphrase="TestPass!",)

# add a smart cards key to the agent.
response = agent.add(
	path=smart_card.path, 
	smart_card=True,
	pin=123456,)

# check if a key is added to the agent.
response = agent.check("/path/to/mykey/private_key")

# list all agent keys.
response = agent.list()

# --------------------
# SSHFS.
sshfs = SSHFS()

# mount a remote server directory.
response = sshfs.mount(
	# the directory paths.
	server_path="/path/to/directory/", 
	client_path="/path/to/directory/", 
	# the ssh params.
	alias="administrator.myserver",)
	
# or without a created alias.
response = sshfs.mount(
	# the directory paths.
	server_path="/path/to/directory/", 
	client_path="/path/to/directory/", 
	# the ssh params.
	username="administrator", 
	ip="0.0.0.0", 
	port=22,
	key_path="/path/to/mykey/private_key",)

# unmount a mounted directory.
response = sshfs.unmount(
	client_path="/path/to/directory/", 
	forced=False,
	sudo=False,)

# --------------------
# SCP.
scp = SCP()

# download a server file or directory from a server.
response = scp.download(
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
response = scp.upload(
	# the file paths.
	server_path="/path/to/directory/", 
	client_path="/path/to/directory/",
	directory=True, 
	# the ssh params.
	username="administrator", 
	ip="0.0.0.0", 
	port=22,
	key_path="/path/to/mykey/private_key",)


# --------------------
# SSH.

# start a ssh session in the terminal console.
ssh.session(alias="username.server")

# execute a command on the server over ssh.
response = ssh.command(command=["echo", "$HOME"], alias="username.server")
# or without a created alias.
response = ssh.command(
	# the command.
	command=["echo", "$HOME"], 
	# the ssh params.
	username="administrator", 
	ip="0.0.0.0", 
	port=22,
	key_path="/path/to/mykey/private_key",)

"""






