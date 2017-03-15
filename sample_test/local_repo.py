import git
from git import Repo, Remote


def commit(path):
    repo = Repo(path)
    print(repo.git.status())
    print(repo.git.add("."))
    print(repo.git.commit(m='my commit message'))
    print(repo.git.push())


def pull(path):
    repo = git.Repo(path)
    origin = repo.remotes.origin
    origin.pull()