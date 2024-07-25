import uuid
from typing import TypedDict, Literal, NotRequired


############
# ENTITIES #
############


class Account(TypedDict):
    id: str
    username: str
    acct: str


class Application(TypedDict):
    name: str
    website: NotRequired[str | None]
    client_id: NotRequired[str]
    client_secret: NotRequired[str]


class CredentialAccount(TypedDict):
    username: str


class Instance(TypedDict):
    uri: str


class Status(TypedDict):
    pass


class Tag(TypedDict):
    pass


class Search(TypedDict):
    accounts: list[Account]
    statuses: list[Status]
    hashtags: list[Tag]


##################
# MASTODON CLASS #
##################

class Mastodon:
    def __init__(self, uri: str = ""):
        self._uri = uri
        self._instance = uri.split("/")[2]

    def v1_accounts_following(
            self,
            id: str,
            limit: int = None,
    ) -> list[Account]:
        return []

    def v1_accounts_verify_credentials(
            self
    ) -> CredentialAccount:
        return {
            "username": "username"
        }

    def v1_apps(
            self,
            client_name: str = None,
            redirect_uris: str = None,
            scopes: str = "read",
            website: str = None,
            **kwargs
    ) -> Application:
        app: Application = {
            "client_id": str(uuid.uuid4()),
            "client_secret": str(uuid.uuid4())
        }
        if client_name is not None:
            app["name"] = client_name
        if website is not None:
            app["website"] = website
        return app

    def v1_instance(self, **kwargs) -> Instance:
        return {
            "uri": self._uri
        }

    def v1_preferences(self, **kwargs) -> dict[str, str]:
        return {}

    def v1_timelines_home(self, **kwargs) -> list[Status]:
        return []

    def v2_search(
            self,
            q: str = "",
            type: Literal["accounts", "hashtags", "statuses"] = None,
            resolve: bool = False,
            **kwargs
    ) -> Search:
        if type == "accounts":
            return {
                "accounts": [{
                    "id": "ID",
                    "username": "username",
                    "acct": "username"
                }],
                "statuses": [],
                "hashtags": []
            }
        else:
            return {
                "accounts": [],
                "statuses": [],
                "hashtags": []
            }
