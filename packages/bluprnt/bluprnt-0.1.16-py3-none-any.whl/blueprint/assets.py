def workspaces(**kwargs):
    return "workspaces/{wid}".format(**kwargs)


def configurations(**kwargs):
    return "workspaces/{wid}/configurations/{cid}".format(**kwargs)


def states(**kwargs):
    return "workspaces/{wid}/configurations/{cid}/states/{sid}".format(**kwargs)


def paramSets(**kwargs):
    return "workspaces/{wid}/configurations/{cid}/states/{sid}/paramSets/{psid}".format(**kwargs)
