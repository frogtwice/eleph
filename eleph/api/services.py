from functools import wraps, partial
from typing import Callable, Optional, Any, Iterator, TypeAliasType

from .mastodon import Mastodon
from .exceptions import Redirect
from ..database import Database


def get_endpoints(
        uri: str,
        database: Database,
        get_oauth_token: Callable[[], Optional[tuple[str, str]]],
        get_request_parameter: Callable[[TypeAliasType, str], Any],
        redirect_callback: Callable[[str], Any],
        pre_hook: Callable[[], Any] = lambda: None,
        post_hook: Callable[[Any], Any] = lambda _: None,
) -> Iterator[tuple[str, str, Callable]]:
    for service in [
        Mastodon(uri, database)
    ]:
        for path, method, endpoint in service.get_endpoints(
            get_oauth_token=get_oauth_token,
            get_request_parameter=get_request_parameter,
        ):
            yield path, method, wraps(endpoint)(partial(
                _wrapper,
                endpoint=endpoint,
                redirect_callback=redirect_callback,
                pre_hook=pre_hook,
                post_hook=post_hook
            ))


def _wrapper(
        endpoint: Callable,
        redirect_callback: Callable[[str], Any],
        pre_hook: Callable[[], Any],
        post_hook: Callable[[Any], Any],
        *args,
        **kwargs
):
    try:
        pre_hook()
        result = endpoint(*args, **kwargs)
        post_hook(result)
        return result
    except Redirect as exc:
        return redirect_callback(exc.value)
