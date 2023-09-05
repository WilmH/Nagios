import os
import urllib.parse
from typing import Dict

import dotenv
import requests
import requests.auth

dotenv.load_dotenv("./nagios.env")

user_name = os.getenv("user")
user_pass = os.getenv("pass")
nagios_url = os.getenv("base_url")

auth = requests.auth.HTTPBasicAuth(user_name, user_pass)
api_url = f"{nagios_url}/cgi-bin/statusjson.cgi"


def get(**parameters: str) -> Dict:
    url_parameter = lambda p: f"{p[0]}={p[1]}"
    formatted_parameters = "&".join([url_parameter(p) for p in parameters.items()])
    request_url = urllib.parse.quote(f"{api_url}?{formatted_parameters}", safe=":=/?&")
    return requests.get(
        request_url,
        auth=auth,
    ).json()
