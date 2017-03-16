# Cargo.toml File Updater
#
# This script parses a cargo.toml file and updates all of the version numbers
# to the version numbers from the lock_file object

import re


# Method to update the passed file (a Cargo.toml file)
def toml_file_update(fname, lock_file):
    with open(fname, 'r+') as fp:
        in_dependencies = False
        lines = fp.readlines()
        fp.seek(0)
        fp.truncate()
        for line in lines:
            if line.strip():
                if in_dependencies:
                    dependency_name = line.split(' ')[0]
                    if dependency_name in lock_file.packages:  # Check if package exists
                        if lock_file.packages[dependency_name].upgrade_available:  # Check if upgrade was found
                            if len(line.split(' ')) == 3:  # Line with format: <package> = "<version>"
                                version_string = '"' + lock_file.packages[dependency_name].version + '"'
                                line = re.sub(r'"(.*?)"', version_string, line)
                            elif 'version = "' in line:
                                version_string = 'version = "' + lock_file.packages[dependency_name].version + '"'
                                line = re.sub(r'version = "(.*?)"', version_string, line)
                elif line.strip().endswith('dependencies]'):
                    in_dependencies = True
                else:
                    in_dependencies = False
            fp.write(line)
