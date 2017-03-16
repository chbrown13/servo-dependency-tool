import git
from git import Repo, Remote
import traceback


def push(path):
    try:
        repo = Repo(path)
        print(repo.git.status())
        repo.git.checkout("master")
        print(repo.git.add("."))
        print(repo.git.commit(m='version update'))
        print(repo.git.push())
    except Exception:
        traceback.print_exc()


def pull(path):
    try:
        repo = git.Repo(path)
        origin = repo.remotes.origin
        s = origin.pull()
        print(s)
    except Exception:
        traceback.print_exc()


#PATH = "D:\Dev\Gitpython"
#pull(PATH)

# push(PATH)
