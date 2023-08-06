import os
import logging
from urllib.parse import urljoin
import requests

GCP_PROJECT = os.environ["GCP_PROJECT"]
FUNCTION_REGION = os.environ["FUNCTION_REGION"]


def get_auth_header(audience):
    token_url = (
        "http://metadata.google.internal"
        "/computeMetadata/v1/instance/service-accounts/default/identity"
        f"?audience={audience}"
    )
    token = requests.get(
        url=token_url, headers={"Metadata-Flavor": "Google"},
    ).content.decode()
    return {"Authorization": "Bearer " + token}


def call(name, **kwargs):
    url = f"https://{FUNCTION_REGION}-{GCP_PROJECT}.cloudfunctions.net/{name}"
    logging.info("CALL: %s %s", name, kwargs)
    r = requests.post(url, headers=get_auth_header(url), json=kwargs)
    logging.info("RESP: %s %s", r.status_code, r.content)
    return r
