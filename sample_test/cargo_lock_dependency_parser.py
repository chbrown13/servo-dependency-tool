# Cargo Lock File Version Dependency Parser
#
# This script parses a Cargo .lock file and extracts the crate names
# as well as their dependency versions.
#   NOTE: Must be placed in the same folder as the Cargo.lock file
#
#   From our Initial Steps requirement:
#       "write code that takes a Cargo.lock file as input and determines
#       the list of crate names and versions that are dependencies"

from os import listdir
from os import curdir
import re
import check_crates


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
        self.source = ""
        self.dependencies = []


# Object representing an entire Cargo.lock file
class LockFile:

    def __init__(self):
        self.root = LockRoot()
        self.packages = []


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
                            lock_file.packages.append(lock_package_to_add)
                            lock_package_to_add = LockPackage()
                    elif line.strip().startswith('name'):
                        lock_package_to_add.name = re.findall(r'"(.*?)"', line)[0]
                    elif line.strip().startswith('version'):
                        lock_package_to_add.version = re.findall(r'"(.*?)"', line)[0]
                    elif line.strip().startswith('source'):
                        lock_package_to_add.source = re.findall(r'"(.*?)"', line)[0]
                    elif line.strip().startswith('[metadata]'):
                        lock_file.packages.append(lock_package_to_add)  # add the last entry before breaking out
                        break
                    elif not in_root and line.strip().startswith('"'):  # lines that start with " are dependencies
                        dependency_string = re.findall(r'"(.*?)"', line)[0].split(' ')
                        dependency_to_add.name = dependency_string[0]  # All dependencies should have a name
                        dependency_to_add.version = dependency_string[1]  # All dependencies should have a version
                        if len(dependency_string) == 3:  # If the dependency has a third field, it has a source
                            dependency_to_add.source = dependency_string[2]
                        lock_package_to_add.dependencies.append(dependency_to_add)
                        dependency_to_add = LockDependency()


# Main

lock_file = LockFile()

# This code iterates through all the files in the current directory and calls lock_file_parse
# when the "Cargo.lock" file is found
for filename in listdir(curdir):
    if filename == "Cargo.lock":
        lock_file_parse(filename)

# *** This is temporary code.
# It prints out what was parsed to ensure the parsing and the objects are getting the intended information
print(lock_file.root.name, lock_file.root.version)
check_crates.clone_crates()
for package in lock_file.packages:
    # print(package.name, package.version, package.source)
    # print("%d dependencies" % len(package.dependencies))
    check_crates.check(package)
check_crates.cleanup()

