from re import match


def valid_id(id_):
    return (
        isinstance(id_, str)
        and 1 <= len(id_) <= 40
        and "/" not in id_
        and id_ not in [".", ".."]
        and not match("__.*__", id_)
    )


def valid_name(name):
    return isinstance(name, str) and 1 <= len(name) <= 50


def valid_repo(repo):
    return isinstance(repo, str) and all(map(valid_id, repo.split("-")))


def valid_asset(asset):
    if isinstance(asset, str):
        parts = list(filter(None, asset.split("/")))
        return len(parts) >= 2 and all(map(valid_id, parts))
    return False


def valid_chid_suffix(suffix):
    return (
        isinstance(suffix, str)
        and 1 <= len(suffix) <= 100
        and match("[a-zA-Z0-9-]+$", suffix)
    )


def valid_chid(chid):
    if isinstance(chid, str):
        parts = chid.split("/")
        return len(parts) == 2 and valid_id(parts[0]) and valid_chid_suffix(parts[1])
    return False


def valid_change_ref(ref):
    if isinstance(ref, str):
        parts = ref.split("/")
        return (
            len(parts) == 3 and valid_id(parts[0]) and valid_chid("/".join(parts[1:]))
        )
    return False


def valid_apply_ref(ref):
    return (
        isinstance(ref, str)
        and ref.startswith("tf/apply")
        and valid_id(ref.split("/")[2])
    )
