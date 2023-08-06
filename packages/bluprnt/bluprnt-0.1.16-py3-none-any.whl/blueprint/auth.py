import json
from base64 import urlsafe_b64decode
from flask import Request, jsonify, abort
from .call import call
from .db import Types

asset_path_templates = {
    Types.WORKSPACES: "workspaces/{wid}",
    Types.CONFIGURATIONS: "workspaces/{wid}/configurations/{cid}",
    Types.STATES: "workspaces/{wid}/configurations/{cid}/states/{sid}",
    Types.PARAM_SETS: "workspaces/{wid}/configurations/{cid}/states/{sid}/paramSets/{pid}",
}


def user_info(request: Request):
    encoded_user_info = request.headers.get("X-Endpoint-Api-Userinfo")
    if encoded_user_info:
        if not encoded_user_info.endswith("=="):
            encoded_user_info += "=="
        return json.loads(urlsafe_b64decode(encoded_user_info))
    return {}


def authorize(request, asset, permission):
    uid = user_info(request)["user_id"]
    resp = call("check_permission", uid=uid, asset=asset, permission=permission)
    if not resp["granted"]:
        resp = jsonify(message="Access denied")
        resp.status_code = 403
        abort(resp)


def auth(permission):
    def wrap(func):
        def wrapped_func(request: Request):
            asset_type = permission.split(".")[0]
            try:
                asset = asset_path_templates[asset_type].format(**request.json)
            except KeyError as e:
                resp = jsonify(message=f"Missing key: {e}")
                resp.status_code = 400
                abort(resp)
            authorize(request, asset, permission)
            return func(request)

        return wrapped_func

    return wrap


class ParsedRequest:
    def __init__(self, request: Request):
        data = request.json
        self.user_info = user_info(request)
        self.data = data
        self.repo = "{}-{}".format(data.get("wid"), data.get("cid"))
        self.change_ref = "{}/{}/{}".format(
            data.get("sid"), self.user_info.get("user_id"), data.get("change_id")
        )
        self.plan_ref = "tf/plan/{}".format(self.change_ref)
        self.apply_ref = "tf/apply/{}".format(data.get("sid"))
        self.source_apply_ref = "tf/apply/{}".format(data.get("source_sid"))
