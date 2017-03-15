import git


def push(path):
    repo = git.Repo(path)
    print(repo.git.status())
    # checkout and track a remote branch
    print(repo.git.checkout("master"))
    # add a file
    print(repo.git.add("."))
    # commit
    print(repo.git.commit(m='my commit message'))
    # now we are one commit ahead
    # print(repo.git.status())
    # now push
    print(repo.git.push())