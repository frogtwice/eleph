from typing import TypedDict, NotRequired


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
