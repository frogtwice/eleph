from typing import Literal, TypedDict, NotRequired
from urllib.parse import urlencode

from .base import API, endpoint, PathParam
from .exceptions import MissingParameter, Redirect

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


class Announcement(TypedDict):
    pass


class Conversation(TypedDict):
    pass


class CredentialAccount(TypedDict):
    id: str
    username: str
    acct: str
    display_name: str
    note: str
    avatar: str
    avatar_static: str


class Filter(TypedDict):
    pass


class Marker(TypedDict):
    pass


class Notification(TypedDict):
    pass


class Status(TypedDict):
    pass


class Tag(TypedDict):
    pass


class Token(TypedDict):
    access_token: str


class Search(TypedDict):
    accounts: list[Account]
    statuses: list[Status]
    hashtags: list[Tag]


class V1Instance(TypedDict):
    uri: str


##################
# MASTODON CLASS #
##################


class Mastodon(API):
    def __init__(self, uri: str = ""):
        self._uri = uri
        parts = uri.split("/")
        self._instance = parts[2] if len(parts) >= 2 else ""

    @endpoint(
        path="/oauth/authorize",
        exception_catchers={
            MissingParameter: lambda _: (
                    {
                        "error": "invalid_grant",
                        "error_description": "The provided authorization grant is invalid, expired, revoked, does not "
                                             "match the redirection URI used in the authorization request, or was "
                                             "issued to another client."
                    }, 400)
        }
    )
    def oauth_authorize(
            self,
            redirect_uri: str,
            response_type: Literal["code"] = None,
            client_id: str = None,
            scope: str = "read",
            force_login: bool = False,
            lang: str = "",
    ) -> str:
        code = "AUTH_CODE"
        if redirect_uri == "urn:ietf:wg:oauth:2.0:oob":
            return code
        else:
            raise Redirect(f"{redirect_uri}?{urlencode({"code": code})}")

    @endpoint(
        path="/oauth/token"
    )
    def oauth_token(
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

    @endpoint(
        path="/v1/accounts/<id>/following"
    )
    def v1_accounts_following(
            self,
            id: PathParam,
            limit: int = None,
    ) -> list[Account]:
        return []

    @endpoint(
        path="/v1/accounts/verify_credentials"
    )
    def v1_accounts_verify_credentials(
            self,
    ) -> CredentialAccount:
        return {
            "id": "0",
            "username": "username",
            "acct": "username",
            "display_name": "username",
            "note": "test",
            "avatar": "https://files.mastodon.social/accounts/avatars/000/023/634/original/6ca8804dc46800ad.png",
            "avatar_static": "https://files.mastodon.social/accounts/avatars/000/023/634/original/6ca8804dc46800ad.png",
        }

    @endpoint(
        path="/v1/annoucements"
    )
    def v1_announcements(
            self,
    ) -> list[Announcement]:
        return []

    @endpoint(
        path="/v1/apps"
    )
    def v1_apps(
            self,
            client_name: str = None,
            redirect_uris: str = None,
            scopes: str = "read",
            website: str = None,
    ) -> Application:
        return {
            "name": client_name if isinstance(client_name, str) else "",
            "client_id": "CLIENT_ID",
            "client_secret": "CLIENT_SECRET"
        }

    @endpoint(
        path="/v1/conversations"
    )
    def v1_conversations(
            self,
    ) -> list[Conversation]:
        return []

    @endpoint(
        path="/v1/instance"
    )
    def v1_instance(
            self,
    ) -> V1Instance:
        return {
            "uri": self._uri
        }

    @endpoint(
        path="/v1/markers"
    )
    def v1_markers(
            self,
    ) -> dict[str, Marker]:
        return {}

    @endpoint(
        path="/v1/notifications"
    )
    def v1_notifications(
            self,
    ) -> list[Notification]:
        return []

    @endpoint(
        path="/v1/preferences"
    )
    def v1_preferences(
            self,
    ) -> dict[str, str]:
        return {}

    @endpoint(
        path="/v1/timelines/home"
    )
    def v1_timelines_home(
            self,
    ) -> list[Status]:
        return []

    @endpoint(
        path="/v1/timelines/public"
    )
    def v1_timelines_public(
            self,
    ) -> list[Status]:
        return []

    @endpoint(
        path="/v1/filters"
    )
    def v2_filters(
            self,
    ) -> list[Filter]:
        return []

    @endpoint(
        path="/v1/search",
        exception_catchers={
            MissingParameter: lambda exc:
            ({
                "accounts": [],
                "statuses": [],
                "hashtags": []
            }, 200)
        }
    )
    def v2_search(
            self,
            q: str = "",
            type: Literal["accounts", "hashtags", "statuses"] = None,
            resolve: bool = False,
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
