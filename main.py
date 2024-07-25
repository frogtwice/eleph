import logging
import os

import eleph


def create_app():
    def run(self, *args, **kwargs):
        self.logger.info(f"RUNNING WITH {args} {kwargs}")
        self.run(debug=True)

    logging.basicConfig(level=logging.INFO)
    app = eleph.create_app(
        uri=os.environ.get("URI", "")
    )
    app.run = run
    return app


if __name__ == "__main__":
    flask_app = create_app()
    flask_app.run()
