from git import Repo, Remote
import git
import os
import shutil
import json

CRATES = "crates.io-index"
packages = ["winapi-build","log","z3", "tpst"] # TODO: list of LockDependency/LockPackage objects from cargo_lock_dependency_parse.py
depend = {}

# Delete repo and files when done
def cleanup():
	shutil.rmtree(CRATES, ignore_errors=True)
	os.rmdir(CRATES)

# Check for updates for input packages
def check_update(pack):
	if pack not in depend.keys():
		return
	else:
		# Check input versions vs latest versions and update
		print "Checking updates for '%s'..."%pack

# Read dependency information from crates.io-index file and store in dict
def read_file(path):
	if path is None:
		return
	filename = os.path.basename(path)
	d = []
	for line in open(path,'r'):
		d.append(json.loads(line))
	depend[filename] = d

# Check if file is in the current path
def check_folder(name, path):
	if name in os.listdir(path):
		file = os.path.join(path,name)
		return file
	return None

# Check if a package exists in crates.io-index
def check_package(pack):
	file = None
	if len(pack) > 3:
		split = [pack[i:i+2] for i in range(0, len(pack), 2)]
		path = os.path.join(CRATES,split[0])
		i = 0
		while(file is None):
			i += 1
			if os.path.exists(path):
				file = check_folder(pack,path)
			else:
				# path doesn't exist
				break
			try:
				path = os.path.join(path,split[i])
			except IndexError:
				break				
	else:
		if len(pack) == 3:
			file = check_folder(pack,os.path.join(CRATES,"3",pack[0]))
		else:
			file = check_folder(pack,os.path.join(CRATES,str(len(pack))))

	if file is None:
		print "Package '%s' Not Found" % pack
		return
	else:
		print "Found package '%s'" % pack
		return file

def clone_crates():
	try:
		repo = Repo.clone_from("https://github.com/rust-lang/crates.io-index.git", CRATES)	
	except git.exc.GitCommandError:
		# crates.io-index repo already exists
		# TODO: pull latest version
		repo = Repo(CRATES)

clone_crates()
for p in packages:
	f = check_package(p)
	read_file(f)
	check_update(p)