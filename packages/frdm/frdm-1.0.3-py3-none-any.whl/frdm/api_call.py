import json
import os
import requests

URL = "https://api.freedomrobotics.ai"
TOKEN = None
SECRET = None

class Error(Exception):
    pass

class UnauthorizedError(Error):
    pass

class NotFoundError(Error):
    pass

class ServerError(Error):
    pass

def api_auth(token, secret):
    global TOKEN, SECRET
    TOKEN = token
    SECRET = secret

def api_call(method, path, data = None, params = None, no_auth = False):
    if no_auth:
        auth_headers = {}
    else:
        auth_headers = {
            "mc_token": TOKEN,
            "mc_secret": SECRET
        }

    if method == "GET":
        r = requests.get(
                URL.strip("/") + "/" + path.strip("/"),
                headers = auth_headers,
                params = params
        )
    elif method == "POST":
        r = requests.post(
                URL.strip("/") + "/" + path.strip("/"),
                headers = auth_headers,
                json = data
        )
    elif method == "PUT":
        r = requests.put(
                URL.strip("/") + "/" + path.strip("/"),
                headers = auth_headers,
                json = data
        )
    r.raise_for_status()

    if r.status_code == 404:
        raise NotFoundError("not found: %s" % r.url)

    if r.status_code == 401:
        return_obj = json.loads(r.text)
        raise UnauthorizedError(return_obj.get("Message",""))
        return

    if r.status_code == 500 or r.status_code == 502:
        return_obj = json.loads(r.text)
        raise ServerError(return_obj.get("message","") + " trying to access " + r.url)
        return

    try:
        return_obj = json.loads(r.text)
        return return_obj
    except:
        raise ServerError("Error parsing API response: [%d] %s" % (r.status_code, r.text))
