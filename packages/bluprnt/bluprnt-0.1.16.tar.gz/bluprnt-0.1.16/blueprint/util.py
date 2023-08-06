import json
from base64 import b64encode
from copy import deepcopy


def repo_name(wid, cid):
    return "{}-{}".format(wid, cid)


def change_ref(sid, chid):
    return "{}/{}".format(sid, chid)


def plan_ref(sid, chid):
    return "tf/plan/{}".format(change_ref(sid, chid))


def apply_ref(sid):
    return "tf/apply/{}".format(sid)


def encode_content(content):
    return b64encode(json.dumps(content, sort_keys=True, indent=0).encode()).decode()


def merge_dict(x, y):
    overlapping_keys = x.keys() & y.keys()
    for k in overlapping_keys:
        merge_dict(x[k], y[k])
    for k in y.keys() - overlapping_keys:
        x[k] = deepcopy(y[k])
    return x