from typing import Literal, TypedDict


class Token(TypedDict):
    access_token: str


class OAuth:
    def authorize(
            self,
            response_type: Literal["code"],
            client_id: str,
            redirect_uri: str,
            scope: str = "read",
            force_login: bool = False,
            lang: str = "",
    ) -> str:
        return "AUTH_CODE"

    def token(
            self,
            grant_type: Literal["authorization_code", "client_credentials"],
            client_id: str,
            client_secret: str,
            redirect_uri: str,
            code: str = None,
            scope: str = "read",
    ) -> Token:
        return {
            "access_token": "ACCESS_TOKEN"
        }
