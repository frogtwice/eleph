from functools import wraps, partial
from typing import Callable, Optional, Any, Iterator

from eleph.api import Redirect
from .base import ParameterType
from .mastodon import Mastodon


def get_endpoints(
        get_oauth_token: Callable[[], Optional[tuple[str, str]]],
        get_request_parameter: Callable[[ParameterType, str], Any],
        redirect_callback: Callable[[str], Any],
        pre_hook: Callable[[], Any] = lambda: None,
        post_hook: Callable[[Any], Any] = lambda _: None,
        uri: str = "",
) -> Iterator[tuple[str, str, Callable]]:
    for service in [
        Mastodon(uri)
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
