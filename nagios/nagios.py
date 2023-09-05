import urllib.parse
from typing import Any, Dict, Tuple

import requests
import requests.auth


class NagiosAPIException(Exception):
    def __init__(self, result_dict: Dict[str, str]):
        type_text = result_dict["type_text"]
        type_code = result_dict["type_code"]
        message = result_dict["message"]
        super().__init__(self, f"{type_text}({type_code}): {message}")


def dict_to_http_parameters(d: Dict[str, str]) -> str:
    """
    Given a str -> str dict, translate to a list of http params and return
    """
    return "&".join([f"{p[0]}={p[1]}" for p in d.items()])


class NagiosAPIConnection:
    def __init__(self, user_name: str, user_pass: str, base_url: str):
        self.auth = requests.auth.HTTPBasicAuth(user_name, user_pass)
        self.url = base_url + "/cgi-bin/"

    def build_request_url(self, cgi: str, parameters: Dict[str, str]) -> str:
        url = urllib.parse.quote(
            f"{self.url + cgi}json.cgi?{dict_to_http_parameters(parameters)}",
            safe=":=/?&",
        )
        return url

    def _get(self, cgi: str, parameters: Dict[str, str]) -> requests.Response:
        if cgi not in ["status", "archive", "object"]:
            raise Exception(f"CGI must be one of: status, archive, object")

        response = requests.get(
            self.build_request_url(cgi, parameters),
            auth=self.auth,
        )

        if not response.json()["result"]["type_text"] == "Success":
            raise NagiosAPIException(response.json()["result"])

        return response

    def status(self, **parameters: str) -> Tuple[requests.Response, requests.Response]:
        result = self._get("status", parameters).json()
        return result["result"], result["data"][parameters["query"]]

    def object(self, **parameters: str) -> Tuple[requests.Response, requests.Response]:
        result = self._get("object", parameters).json()
        return result["result"], result["data"][parameters["query"]]

    def archive(self, **parameters: str) -> Tuple[requests.Response, requests.Response]:
        result = self._get("archive", parameters).json()
        return result["result"], result["data"][parameters["query"]]
