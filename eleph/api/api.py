import inspect
from contextvars import ContextVar
from dataclasses import dataclass
from functools import wraps
from inspect import Parameter
from typing import Callable, Optional, Any, Iterator, Literal, Sequence, Mapping, Type, get_origin, \
    get_args, TypeAliasType

from .exceptions import MissingParameter

request_kwargs: ContextVar[dict[str, Any]] = ContextVar("request_kwargs")

Method = Literal["GET", "POST"]

type PathParam = str
type HeaderParam = str
type ValueParam[T] = T
type QueryParam[T] = T
type FormParam[T] = T
type AuthParam[T] = T


class API:
    def get_endpoints(
            self,
            get_oauth_token: Callable[[], Optional[tuple[str, str]]],
            get_request_parameter: Callable[[TypeAliasType, str], Any],
    ) -> Iterator[tuple[str, str, Callable]]:
        for _, member in inspect.getmembers(self):
            if isinstance(member, Endpoint):
                yield member.instantiate(self, get_oauth_token, get_request_parameter)

    def oauth_validate_token(
            self,
            oauth_level: str,
            oauth_scopes: Sequence[str],
            token: tuple[str | None, str | None],
    ) -> Any:
        ...


@dataclass
class Endpoint:
    function: Callable
    path: str
    method: Method
    oauth_level: str
    oauth_scopes: Sequence[str]
    exception_catchers: Mapping[Type[Exception], Callable[[Exception], tuple[Any, int]]]

    def __post_init__(self):
        self.endpoint_parameters = {
            name: _parse_endpoint_parameters(param)
            for name, param in list(inspect.signature(self.function).parameters.items())[1:]
        }

    def instantiate(
            self,
            api: API,
            get_oauth_token: Callable[[], Optional[tuple[str, str]]],
            get_request_parameter: Callable[[TypeAliasType, str], Any],
    ) -> tuple[str, str, Callable]:
        @wraps(self.function)
        def wrapper(**kwargs):
            request_kwargs.set(kwargs)

            try:
                token = get_oauth_token()
                authorization = api.oauth_validate_token(self.oauth_level, self.oauth_scopes, token or (None, None))
                received_kwargs = {}
                for name, (param_type, value_type, default) in self.endpoint_parameters.items():
                    if param_type is AuthParam:
                        received_kwargs[name] = authorization
                    else:
                        try:
                            value = get_request_parameter(param_type, name)
                        except KeyError:
                            if default != Parameter.empty:
                                received_kwargs[name] = default
                            else:
                                raise MissingParameter(name)
                        else:
                            received_kwargs[name] = _cast(value, value_type)
                return self.function(api, **received_kwargs)
            except Exception as exc:
                if type(exc) in self.exception_catchers:
                    return self.exception_catchers[type(exc)](exc)
                else:
                    raise

        return self.path, self.method, wrapper


def endpoint(
        path: str,
        method: Method = "GET",
        oauth_level: str = None,
        oauth_scopes: str | Sequence[str] = (),
        exception_catchers: Mapping[Type[Exception], Callable[[Exception], tuple[Any, int]]] = None,
):
    def decorator(function: Callable) -> Endpoint:
        return Endpoint(
            function=function,
            path=path,
            method=method,
            oauth_level=oauth_level,
            oauth_scopes=[oauth_scopes] if isinstance(oauth_scopes, str) else oauth_scopes,
            exception_catchers=exception_catchers or {}
        )

    return decorator


def _parse_endpoint_parameters(parameter: Parameter) -> tuple[TypeAliasType, type, Any]:
    origin = get_origin(parameter.annotation)
    args = get_args(parameter.annotation)
    if origin in (ValueParam, QueryParam, FormParam, AuthParam):
        param_type = origin
        value_type = args[0]
    elif parameter.annotation in (PathParam, HeaderParam):
        param_type = parameter.annotation
        value_type = str
    else:
        param_type = ValueParam
        value_type = parameter.annotation
    return param_type, value_type, parameter.default


def _cast(value: Any, typ: Any) -> Any:
    if typ in (str,):
        return typ(value)
    else:
        raise NotImplementedError
