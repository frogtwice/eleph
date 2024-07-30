import logging
from functools import wraps, partial
from typing import Any

from flask import Flask, request, redirect
from werkzeug.exceptions import BadRequestKeyError

from .api import Redirect, PathParam, request_kwargs, ValueParam
from .mastodon import Mastodon


class FlaskApp(Mastodon):
    def __init__(self, uri: str):
        Mastodon.__init__(self, uri)
        self._logger = logging.getLogger("eleph")
        self._app = Flask("eleph")
        for endpoint, path, method in self.get_endpoints():
            self._app.route(path, methods=[method])(
                wraps(endpoint)(partial(self.request_wrapper, endpoint)))

    def get_app(self):
        return self._app

    def oauth_get_token(self) -> tuple[str, str] | None:
        match request.headers.get("Authorize", "").split(" "):
            case ["Bearer", token]:
                return "Bearer", token

    def get_parameter(self, typ: Any, name: str) -> Any:
        if typ == PathParam:
            return request_kwargs.get()[name]
        elif typ == ValueParam:
            try:
                return request.values[name]
            except BadRequestKeyError:
                raise KeyError
        else:
            raise NotImplementedError

    def request_wrapper(self, endpoint, *args, **kwargs):
        message = [f"PATH: {request.path}, METHOD: {request.method}"]
        if len(request.args) > 0:
            message.append(f"ARGS: {request.args}")
        if len(request.form) > 0:
            message.append(f"FORM: {request.form}")
        try:
            result = endpoint(*args, **kwargs)
            message.append(f"RESULT: {result}")
            return result
        except Redirect as exc:
            return redirect(exc.value)
        finally:
            self._logger.info("\n".join(message))
