import json
import logging
from functools import wraps

from flask import request

logger = logging.getLogger("eleph")


def log_request[T](method: T) -> T:
    @wraps(method)
    def decorator(*args, **kwargs):
        msg = [f"PATH: {request.path}"]
        if len(request.args) > 0:
            msg.append(f"ARGS: {json.dumps(request.args)}")
        if len(request.form) > 0:
            msg.append(f"FORM: {json.dumps(request.form)}")
        logger.info("\n".join(msg))
        return method(*args, **kwargs)

    return decorator
