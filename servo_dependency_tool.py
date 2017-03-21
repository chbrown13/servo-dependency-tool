import datetime
import os
import shutil
import subprocess

import cargo_lock_parser
import cargo_toml_updater
import crates_io_checker
import repo_management


def run_cargo_update(pkg):
    print("Running update for %s" % pkg.name)
    if os.path.isfile('mach'):
        mach_path = './mach'
        args = [mach_path, 'cargo-update', '-p', pkg.name]
    else:  # Otherwise use default cargo update command
        cargo_bin_path = os.path.expanduser('~/.cargo/bin/cargo')
        args = [cargo_bin_path, 'update', '-p', pkg.name]
    print('This may take a moment...')
    print(args)
    cmd_out = None
    cmd_err = None
    cmd_out, cmd_err = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    print(cmd_err.decode('utf-8'))
    if 'is ambiguous.' in cmd_err.decode('utf-8'):  # If failure due to ambiguity, use precise version
        if os.path.isfile('mach'):
            mach_path = './mach'
            args = [mach_path, 'cargo-update', '-p', (pkg.name + ':' + pkg.version)]
        else:  # Otherwise use default cargo update command
            cargo_bin_path = os.path.expanduser('~/.cargo/bin/cargo')
            args = [cargo_bin_path, 'update', '-p', (pkg.name + ':' + pkg.version)]
        print('Specifying version %s...' % pkg.version)
        print('This may take a moment...')
        print(args)
        cmd_out = None
        cmd_err = None
        cmd_out, cmd_err = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        print(cmd_err.decode('utf-8'))


# Main

# Perform a "git pull" on the directory above
git_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
print('Performing git pull inside "%s"' % git_path)
repo_management.pull(git_path)

# Create a new branch before making any updates
repo_management.create_new_branch('..', datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S_crate_update"))

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

# "Delete" Cargo.lock to avoid conflicts (rename to Cargo.lock.bak)
os.rename('Cargo.lock', 'Cargo.lock.bak')

# Loop through the packages again and call run_cargo_update
# to run the appropriate update command.
for package_name in lock_file.packages:
    if lock_file.packages[package_name].upgrade_available:
        run_cargo_update(lock_file.packages[package_name])

# Push the updates
