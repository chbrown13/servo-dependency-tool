# Cargo Lock File Version Dependency Parser
#
# This script parses a Cargo .lock file and extracts the crate names
# as well as their dependency versions.
#   NOTE: Must be placed in the same folder as the Cargo.lock file
#
#   From our Initial Steps requirement:
#       "write code that takes a Cargo.lock file as input and determines
#       the list of crate names and versions that are dependencies"

import os
import re
import subprocess
import shutil
import check_crates
import cargo_toml_dependency_parser


# Object representing the root. A Cargo.lock file will always have one [[root]]
class LockRoot:

    def __init__(self):
        self.name = ""
        self.version = ""
        self.dependencies = []


# Object representing a dependency. Each [[root]] and [[package]] within a Cargo.lock file can have >= 0 dependencies
class LockDependency:

    def __init__(self):
        self.name = ""
        self.version = ""
        self.source = ""


# Object representing a [[package]] within the Cargo.lock file. A Cargo.lock file can have >= 0 packages
class LockPackage:

    def __init__(self):
        self.name = ""
        self.version = ""
        self.upgrade_available = False
        self.source = ""
        self.dependencies = []


# Object representing an entire Cargo.lock file
class LockFile:

    def __init__(self):
        self.root = LockRoot()
        self.packages = {}  # dictionary


# Method to parse the passed file (a Cargo.lock file)
def lock_file_parse(fname):
    with open(fname, 'r') as fp:
        lock_package_to_add = LockPackage()  # temporary LockPackage object
        dependency_to_add = LockDependency()  # temporary LockDependency object
        in_root = True  # flag to determine whether the current lines are within the root or not
        for line in fp:
            if line.strip():
                if in_root:
                    if line.strip().startswith('name'):
                        lock_file.root.name = re.findall(r'"(.*?)"', line)[0]
                    elif line.strip().startswith('version'):
                        lock_file.root.version = re.findall(r'"(.*?)"', line)[0]
                    elif line.strip().startswith('"'):  # lines that start with " are dependencies
                        dependency_string = re.findall(r'"(.*?)"', line)[0].split(' ')
                        dependency_to_add.name = dependency_string[0]  # All dependencies should have a name
                        dependency_to_add.version = dependency_string[1]  # All dependencies should have a version
                        if len(dependency_string) == 3:  # If the dependency has a third field, it has a source
                            dependency_to_add.source = dependency_string[2]
                        lock_file.root.dependencies.append(dependency_to_add)
                        dependency_to_add = LockDependency()
                    elif line.strip() == "[[package]]":  # End of Root
                        in_root = False
                else:
                    # If [[package]] is found, we've reached a new package
                    if line.strip() == "[[package]]":
                        # If lock_package_to_add has data, add to list and then reset
                        if lock_package_to_add.name != "":
                            lock_file.packages[lock_package_to_add.name] = lock_package_to_add
                            lock_package_to_add = LockPackage()
                    elif line.strip().startswith('name'):
                        lock_package_to_add.name = re.findall(r'"(.*?)"', line)[0]
                    elif line.strip().startswith('version'):
                        lock_package_to_add.version = re.findall(r'"(.*?)"', line)[0]
                    elif line.strip().startswith('source'):
                        lock_package_to_add.source = re.findall(r'"(.*?)"', line)[0]
                    elif line.strip().startswith('[metadata]'):
                        lock_file.packages[lock_package_to_add.name] = lock_package_to_add  # add the last entry
                        break
                    elif not in_root and line.strip().startswith('"'):  # lines that start with " are dependencies
                        dependency_string = re.findall(r'"(.*?)"', line)[0].split(' ')
                        dependency_to_add.name = dependency_string[0]  # All dependencies should have a name
                        dependency_to_add.version = dependency_string[1]  # All dependencies should have a version
                        if len(dependency_string) == 3:  # If the dependency has a third field, it has a source
                            dependency_to_add.source = dependency_string[2]
                        lock_package_to_add.dependencies.append(dependency_to_add)
                        dependency_to_add = LockDependency()


def run_cargo_update(package_name):
    print("Running update for %s" % package_name)
    if os.path.isfile('mach'):  # Check if this is servo root directory (servo users mach to upgrade)
        mach_path = './mach'
        args = [mach_path, 'cargo-update', '-p', package_name]
    else:  # Otherwise use default cargo update command
        cargo_bin_path = os.path.expanduser('~/.cargo/bin/cargo')
        args = [cargo_bin_path, 'update', '-p', package_name]
    p = subprocess.Popen(args, stdout=subprocess.PIPE)
    print(p.stdout.read().decode('ascii'))


# Main

lock_file = LockFile()

# This code iterates through all the files in the current directory and calls lock_file_parse
# when the "Cargo.lock" file is found
for filename in os.listdir(os.curdir):
    if filename == "Cargo.lock":
        lock_file_parse(filename)

# *** This is temporary code.
# It prints out what was parsed to ensure the parsing and the objects are getting the intended information
print(lock_file.root.name, lock_file.root.version)
check_crates.clone_crates()
for package_name in lock_file.packages:
    # print(package.name, package.version, package.source)
    # print("%d dependencies" % len(package.dependencies))
    check_crates.check(lock_file.packages[package_name])

shutil.rmtree('crates.io-index')

for root, dirs, files in os.walk(os.curdir):
    if "crates.io-index" in dirs:
        dirs.remove("crates.io-index")  # don't visit CVS directories
        for filename in files:
            if filename.lower() == "cargo.toml":
                cargo_toml_dependency_parser.toml_file_parse(filename, lock_file)

for package_name in lock_file.packages:
    if lock_file.packages[package_name].upgrade_available:
        run_cargo_update(package_name)
