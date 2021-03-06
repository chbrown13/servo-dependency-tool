from git import Repo, Remote
import git
import os
import platform
import json
import repo_management

CRATES = "crates.io-index"

depend = {}


# Delete repo and files when done
def cleanup():
    if platform.system() == "Windows":
        rm = 'rmdir /S /Q "%s"' % CRATES
    else:
        rm = "rm -rf %s" % CRATES
    os.system(rm)


# Check for upgrades for input packages
def check_upgrade(package):
    if package.name not in depend.keys():
        # Error somewhere
        print("Package not found")
        return False
    else:
        # Check input version vs latest version
        current = package.version
        latest = depend[package.name][-1]["vers"]
        print("Checking for '%s' upgrades... current= %s, latest= %s" % (package.name, current, latest))
        package.version = latest
        return current != latest


# Read dependency information from crates.io-index file and store in dict
def read_file(path):
    if path is None:
        return
    filename = os.path.basename(path)
    d = []
    with open(path, 'r') as f:
        for line in f:
            d.append(json.loads(line))
    depend[filename] = d


# Check if file is in the current path
def check_folder(name, path):
    try:
        if name in os.listdir(path):
            file = os.path.join(path, name)
            return file
    except FileNotFoundError:
        return None
    return None


# Check if a package exists in crates.io-index
def check_package(package):
    file = None
    pack = package.name
    if len(pack) > 3:
        split = [pack[i:i+2] for i in range(0, len(pack), 2)]
        path = os.path.join(CRATES, split[0])
        i = 0
        while file is None:
            i += 1
            if os.path.exists(path):
                file = check_folder(pack, path)
            else:
                # path doesn't exist
                break
            try:
                path = os.path.join(path, split[i])
            except IndexError:
                break
    else:
        if len(pack) == 3:
            file = check_folder(pack, os.path.join(CRATES, "3", pack[0]))
        else:
            file = check_folder(pack, os.path.join(CRATES, str(len(pack))))

    if file is None:
        print("Package '%s' Not Found" % pack)
        return
    else:
        # print("Found package '%s'"%pack)
        return file


def clone_crates():
    try:
        print("Cloning crates.io-index repository...(This may take a while)") # Git submodules may avoid this
        repo = Repo.clone_from("https://github.com/rust-lang/crates.io-index.git", CRATES)
    except git.exc.GitCommandError:
        # crates.io-index repo already exists
        git_path = os.path.abspath(os.path.join(os.path.dirname((CRATES)),CRATES))
        repo_management.pull(git_path)


def check(p):
    f = check_package(p)
    read_file(f)
    p.upgrade_available = check_upgrade(p)
