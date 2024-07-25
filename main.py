import logging
import os

import eleph


def create_app():
    logging.basicConfig(level=logging.INFO)
    app = eleph.create_app(
        uri=os.environ.get("URI", "")
    )
    app.config['DEBUG'] = True
    return app


if __name__ == "__main__":
    flask_app = create_app()
    flask_app.run()
