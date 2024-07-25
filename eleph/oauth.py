from typing import Literal, TypedDict


class Token(TypedDict):
    access_token: str


class HTTPRedirect(Exception):
    def __init__(self, url: str):
        self.url = url


class OAuth:
    def authorize(
            self,
            response_type: Literal["code"] = None,
            client_id: str = None,
            redirect_uri: str = None,
            scope: str = "read",
            force_login: bool = False,
            lang: str = "",
    ) -> str:
        if redirect_uri == "urn:ietf:wg:oauth:2.0:oob":
            return "AUTH_CODE"
        else:
            raise HTTPRedirect(f"{redirect_uri}?code=AUTH_CODE")

    def token(
            self,
            grant_type: Literal["authorization_code", "client_credentials"] = None,
            client_id: str = None,
            client_secret: str = None,
            redirect_uri: str = None,
            code: str = None,
            scope: str = "read",
    ) -> Token:
        return {
            "access_token": "ACCESS_TOKEN"
        }
