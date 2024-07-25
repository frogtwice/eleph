import logging
import os

import eleph

logging.basicConfig(level=logging.INFO)


def create_app():
    app = eleph.create_app(
        uri=os.environ.get("URI", "")
    )
    app.config['DEBUG'] = os.environ.get("DEBUG") in ("1", "True", "true", "yes", "y")
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
    return app


if __name__ == "__main__":
    flask_app = create_app()
    flask_app.run()
