from .call import call


def _github(**kwargs):
    return call("github", **kwargs)


def create_repo(repo):
    return _github(
        root="orgs",
        path="repos",
        method="POST",
        body={"name": repo, "private": True, "has_issues": False, "has_wiki": False,},
    )


def delete_repo(repo):
    return _github(root="repos", path=repo, method="DELETE")


def get_ref(repo, refname):
    return _github(root="repos", path=f"{repo}/git/refs/heads/{refname}", method="GET")


def create_ref(repo, refname, sha):
    return _github(
        root="repos",
        path=f"{repo}/git/refs",
        method="POST",
        body={"ref": f"refs/heads/{refname}", "sha": sha},
    )


def create_merge(repo, base, head, message):
    return _github(
        root="repos",
        path=f"{repo}/merges",
        method="POST",
        body={"base": base, "head": head, "commit_message": message},
    )


def get_contents(repo, filename, branch):
    return _github(
        root="repos", path=f"{repo}/contents/{filename}?ref={branch}", method="GET",
    )


def update_contents(repo, filename, content, branch, message):
    return _github(
        root="repos",
        path=f"{repo}/contents/{filename}",
        method="PUT",
        body={"message": message, "branch": branch, "content": content},
    )


def delete_contents(repo, filename, branch, message):
    return _github(
        root="repos",
        path=f"{repo}/contents/{filename}",
        method="DELETE",
        body={"message": message, "branch": branch},
    )
