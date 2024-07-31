import logging
from typing import TypeAliasType

from flask import Flask, request, redirect
from werkzeug.exceptions import BadRequestKeyError

from ..api import get_endpoints, request_kwargs, PathParam, ValueParam, QueryParam, FormParam, HeaderParam
from ..database import Database


def create_flask_app(
        name: str,
        uri: str,
        database: Database,
        log: bool = False,
):
    if log:
        logger = logging.getLogger("ELEPH_FLASK")

        def pre_hook():
            message = [f"PATH: {request.path}, METHOD: {request.method}"]
            if len(request.args) > 0:
                message.append(f"ARGS: {dict(request.args)}")
            if len(request.form) > 0:
                message.append(f"FORM: {dict(request.form)}")
            logger.info("\n".join(message))

        def post_hook(result):
            logger.info(f"RESULT: {result}")

    else:
        def pre_hook():
            pass

        def post_hook(_):
            pass

    app = Flask(name)
    for path, method, endpoint in get_endpoints(
            uri=uri,
            database=database,
            get_oauth_token=_get_oauth_token,
            get_request_parameter=_get_request_parameter,
            redirect_callback=lambda url: redirect(url),
            pre_hook=pre_hook,
            post_hook=post_hook,
    ):
        app.route(path, methods=[method])(endpoint)
    return app


def _get_oauth_token():
    match request.headers.get("Authorization", "").split(" "):
        case [token_type, token]:
            return token_type, token


def _get_request_parameter(parameter_type: TypeAliasType, name: str):
    if parameter_type == PathParam:
        return request_kwargs.get()[name]
    elif parameter_type == ValueParam:
        try:
            return request.values[name]
        except BadRequestKeyError:
            raise KeyError
    else:
        raise NotImplementedError
