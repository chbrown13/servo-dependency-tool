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


class Dependency:

    def __init__(self):
        self.name = ""
        self.version = ""
        self.source = ""


class LockPackage:

    def __init__(self):
        self.name = ""
        self.version = ""
        self.source = ""
        self.dependencies = []


def lock_file_parse(fname):
    with open(fname, 'r') as fp:
        lock_package_to_add = LockPackage()  # temporary LockPackage object
        dependency_to_add = Dependency()  # temporary Dependency object
        in_root = True  # flag used to ignore lines associated with [root]
        for line in fp:
            if line.strip():
                # If [[package]] is found, we've reached a new package
                if line.strip() == "[[package]]":
                    in_root = False
                    # If dependency_to_add has data, add to list and then reset
                    if lock_package_to_add.name != "":
                        packages.append(lock_package_to_add)
                        lock_package_to_add = LockPackage()
                elif not in_root and line.strip().startswith('name'):
                    lock_package_to_add.name = re.findall(r'"(.*?)"', line)[0]
                elif not in_root and line.strip().startswith('version'):
                    lock_package_to_add.version = re.findall(r'"(.*?)"', line)[0]
                elif not in_root and line.strip().startswith('source'):
                    lock_package_to_add.source = re.findall(r'"(.*?)"', line)[0]
                elif not in_root and line.strip().startswith('[metadata]'):
                    packages.append(lock_package_to_add)  # add the last entry before breaking out
                    break
                elif not in_root and line.strip().startswith('"'):  # lines that start with " are dependencies
                    dependency_string = re.findall(r'"(.*?)"', line)[0].split(' ')
                    dependency_to_add.name = dependency_string[0]  # All dependencies should have a name
                    dependency_to_add.version = dependency_string[1]  # All dependencies should have a version
                    if len(dependency_string) == 3:  # If the dependency has a third field, it has a source
                        dependency_to_add.source = dependency_string[2]
                    lock_package_to_add.dependencies.append(dependency_to_add)
                    dependency_to_add = Dependency()


packages = []

for filename in listdir(curdir):
    if filename == "Cargo.lock":
        lock_file_parse(filename)

for package in packages:
    # print("Package")
    print(package.name, package.version, package.source)
    print("%d dependencies" % len(package.dependencies))
