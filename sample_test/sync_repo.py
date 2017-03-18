from git import Repo, Remote
from github3 import login
import git
import traceback


class SyncRepo:
    def create_new_branch(path, branch_name):
        repo = Repo(path)
        new_branch = repo.create_head(branch_name)
        new_branch.commit
        repo.git.push("origin", branch_name)

    def push(self, path):
        try:
            repo = Repo(path)
            print(repo.git.status())
            repo.git.checkout("master")
            print(repo.git.add("."))
            print(repo.git.commit(m='version update'))
            print(repo.git.push())
        except Exception:
            traceback.print_exc()

    def pull(self, path):
        try:
            repo = git.Repo(path)
            origin = repo.remotes.origin
            # only pulls the master branch
            s = origin.pull("master")
            print(s)
        except Exception:
            traceback.print_exc()

    # PATH = "D:\Dev\Gitpython"
    # pull(PATH)

    # push(PATH)

    def pull_request(self, username, password, title, base, head, body=None):
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
