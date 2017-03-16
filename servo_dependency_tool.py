import os
import shutil
import subprocess

import cargo_lock_parser
import cargo_toml_updater
import crates_io_checker


def run_cargo_update(pkg_name):
    print("Running update for %s" % pkg_name)
    if os.path.isfile('mach'):  # Check if this is servo root directory (servo users mach to upgrade)
        mach_path = './mach'
        args = [mach_path, 'cargo-update', '-p', pkg_name]
    else:  # Otherwise use default cargo update command
        cargo_bin_path = os.path.expanduser('~/.cargo/bin/cargo')
        args = [cargo_bin_path, 'update', '-p', pkg_name]
    p = subprocess.Popen(args, stdout=subprocess.PIPE)
    print(p.stdout.read().decode('ascii'))


# Main

# This code iterates through all the files in the current directory and calls lock_file_parse
# when the "Cargo.lock" file is found
for filename in os.listdir(os.curdir):
    if filename == "Cargo.lock":
        lock_file = cargo_lock_parser.lock_file_parse(filename)

# *** This is temporary code.
# It prints out what was parsed to ensure the parsing and the objects are getting the intended information
print(lock_file.root.name, lock_file.root.version)
crates_io_checker.clone_crates()
for package_name in lock_file.packages:
    # print(package.name, package.version, package.source)
    # print("%d dependencies" % len(package.dependencies))
    crates_io_checker.check(lock_file.packages[package_name])

# Remove the cloned crates.io-index. We do this here
# so that the upcoming directory tree traversal won't
# go into the crates.io-index folders.
shutil.rmtree('crates.io-index')

# Loop through directory tree
# For each instance of Cargo.toml, call toml_file_update to update
# the version numbers for each dependency
for root, dirs, files in os.walk(os.curdir):
    for filename in files:
        if filename.lower() == "cargo.toml":
            toml_file_path = os.path.join(root, filename)
            cargo_toml_updater.toml_file_update(toml_file_path, lock_file)

# Loop through the packages again and call run_cargo_update
# to run the appropriate update command.
for package_name in lock_file.packages:
    if lock_file.packages[package_name].upgrade_available:
        run_cargo_update(package_name)
