import inspect
from abc import ABC, abstractmethod
from collections.abc import Callable
from contextvars import ContextVar
from functools import wraps
from inspect import Parameter
from typing import Any, Literal, Mapping, Sequence, Type, TypeAliasType, get_origin, get_args, Iterator

type Method = Literal["GET", "POST"]

type PathParam = str
type ValueParam[T] = T

parameter_types = {
    PathParam,
    ValueParam
}

request_kwargs: ContextVar[dict[str, Any]] = ContextVar("request_kwargs")


#######
# API #
#######

class API(ABC):
    @abstractmethod
    def oauth_get_token(self) -> tuple[str, str] | None:
        ...

    @abstractmethod
    def oauth_validate_token(self, level: str, scopes: list[str], token: tuple[str | None, str | None]):
        ...

    @abstractmethod
    def get_parameter(self, typ: Any, name: str) -> Any:
        ...

    def get_endpoints(self) -> Iterator[tuple[Callable, str, str]]:
        for _, member in inspect.getmembers(self):
            try:
                yield member, getattr(member, "__path__"), getattr(member, "__method__")
            except AttributeError:
                pass


############
# ENDPOINT #
############


def endpoint(
        path: str,
        method: Method = "GET",
        oauth_level: str = None,
        oauth_scopes: str | Sequence[str] = (),
        exception_catchers: Mapping[Type[Exception], Callable[[Exception], tuple[Any, int]]] = None,
):
    if isinstance(oauth_scopes, str):
        oauth_scopes = [oauth_scopes]
    exception_catchers = exception_catchers or {}

    def decorator[T](function: T) -> T:
        parameters_type = {
            name: _parse_parameter(param)
            for name, param in list(inspect.signature(function).parameters.items())[1:]
        }

        @wraps(function)
        def wrapper(self: API, **kwargs):
            request_kwargs.set(kwargs)
            try:
                token = self.oauth_get_token()
                self.oauth_validate_token(oauth_level, oauth_scopes, token or (None, None))
                received_kwargs = {}
                for name, (origin, arg, default) in parameters_type.items():
                    try:
                        value = self.get_parameter(origin, name)
                    except KeyError:
                        if default != Parameter.empty:
                            received_kwargs[name] = default
                        else:
                            raise MissingParameter(name)
                    else:
                        received_kwargs[name] = _cast(value, arg)
                return function(self, **received_kwargs)
            except Exception as exc:
                if type(exc) in exception_catchers:
                    return exception_catchers[type(exc)](exc)
                else:
                    raise

        wrapper.__path__ = path
        wrapper.__method__ = method
        return wrapper

    return decorator


def _parse_parameter(parameter: Parameter) -> tuple[TypeAliasType, type, Any]:
    origin = get_origin(parameter.annotation)
    if origin not in parameter_types:
        return ValueParam, parameter.annotation, parameter.default
    elif origin is PathParam:
        return PathParam, str, parameter.default
    else:
        return origin, get_args(parameter.annotation)[0], parameter.default


def _cast(value: Any, typ: Any) -> Any:
    if typ in (str,):
        return typ(value)
    else:
        raise NotImplementedError


##############
# EXCEPTIONS #
##############

class SingleValuedException[T](Exception):
    def __init__(self, value: T):
        self.value = value


###############
# HTTP ERRORS #
###############

class UnprocessableEntity(SingleValuedException[str]):
    pass


####################
# OTHER EXCEPTIONS #
####################

class MissingParameter(SingleValuedException[str]):
    pass


class Redirect(SingleValuedException[str]):
    pass
