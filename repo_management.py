from git import Repo, Remote
from github3 import login
import git
import traceback


# Function that takes the local git clone directory path and the new branch name as parameters
# and create a new branch in both the local repository and remote
def create_new_branch(path, branch_name):
    repo = Repo(path)
    new_branch = repo.create_head(branch_name)
    new_branch.commit
    repo.git.push("origin", branch_name)


# Function that pushes changes to the master branch of the remote repository.
def push(path, branch, message):
    try:
        repo = Repo(path)
        repo.git.checkout(branch)
        print(repo.git.add("."))
        print(repo.git.commit(m=message))
        print(repo.git.push())
        print(repo.git.status())
    except Exception:
        traceback.print_exc()


# Function that pulls everything from the master branch of the the remote repository to the local git clone.
def pull(path):
    try:
        repo = git.Repo(path)
        origin = repo.remotes.origin
        # only pulls the master branch
        s = origin.pull("master")
        # print(repo.git.status())
    except Exception:
        traceback.print_exc()


# Function that opens a pull request against Servo's github repository from a particular branch on a fork.
def pull_request(username, password, title, base, head, body=None):
    # Login to the forked repo
    gh = login(username, password)
    # Create a Repository instance of servo (with owner Servo and repo name servo)
    repo = gh.repository("Servo", "servo")
    # Now create the pull request
    repo.create_pull(title, base, head, body)
    # :param str title: (required) The title of the pull request.
    # :param str base: (required), The branch of the servo repo which you want the changes pulled into. e.g., 'master'
    # :param str head: (required), The place where your changes are implemented. e.g. 'qiufengyu21:master'
    # :param str body: (optional), The contents of the pull request.
