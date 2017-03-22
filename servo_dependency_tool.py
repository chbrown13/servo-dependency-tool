# Servo Dependency Tool
#
# Authors:
#   Chris Brown (dcbrow10@ncsu.edu)
#   Bradford Ingersoll (bingers@ncsu.edu)
#   Qiufeng Yu (qyu4@ncsu.edu)

import datetime
import getpass
import os
import shutil

import cargo_lock_parser
import cargo_toml_updater
import crates_io_checker
import repo_management
import run_cargo_update

#
# Main
#

# Perform a "git pull" on the parent directory
git_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
print('Performing git pull inside "%s"' % git_path)
repo_management.pull(git_path)

# Create a new branch before making any updates
branch_name = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S_crate_update")
repo_management.create_new_branch('..', branch_name)

# Edit .gitignore to add this servo-dependency-tool directory
with open(os.path.join(git_path, '.gitignore'), "r") as f:
    tool_ignored = False
    for line in f:
        if line == 'servo-dependency-tool/':
            tool_ignored = True
if not tool_ignored:
    with open(os.path.join(git_path, '.gitignore'), "a") as f:
        f.write('\n')
        f.write('# Servo Dependency Tool\n')
        f.write('servo-dependency-tool/')

# Check for existence of Cargo.lock file and parse it
for filename in os.listdir(git_path):
    if filename == "Cargo.lock":
        lock_file = cargo_lock_parser.lock_file_parse(os.path.join(git_path, filename))

# Ignore hyper dependencies per Josh Matthews: "Can't update hyper without additional work"
# Do so by removing it from the collection
for package_name in lock_file.packages:
    if package_name.startswith('hyper'):
        del lock_file.packages[package_name]

# Run crates_io_checker which determines the latest version for all packages in lock_file.packages
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
for root, dirs, files in os.walk(git_path):
    if 'servo-dependency-tool' in dirs:
        dirs.remove('servo-dependency-tool')  # Don't visit this tool's directory
    for filename in files:
        if filename.lower() == "cargo.toml":
            toml_file_path = os.path.join(root, filename)
            cargo_toml_updater.toml_file_update(toml_file_path, lock_file)

# "Delete" Cargo.lock to avoid conflicts (rename to Cargo.lock.bak)
os.rename(os.path.join(git_path, 'Cargo.lock'), os.path.join(git_path, 'Cargo.lock.bak'))

# Loop through the packages again and call run_cargo_update
# to run the appropriate update command.
for package_name in lock_file.packages:
    if lock_file.packages[package_name].upgrade_available:
        run_cargo_update.run_update(git_path, lock_file.packages[package_name])

# Push the updates to origin/branch_name
repo_management.push(git_path, branch_name, 'Updated dependencies')

# Pull request on master
print('Initiating pull request...')
gh_username = input('GitHub Username: ')
gh_password = getpass.getpass('GitHub Password: ')
title = 'Updated dependencies in Cargo.toml files to latest versions'
desc = 'Updated all Cargo.toml files with the latest versions found on crates.io for all dependencies and ran \
       "./mach cargo-update -p <package_name> for each'
repo_management.pull_request(gh_username, gh_password, title, 'master', gh_username + ':' + branch_name, desc)
