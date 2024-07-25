import os

import eleph


def create_app():
    return eleph.create_app(
        uri=os.environ["URI"]
    )


if __name__ == "__main__":
    app = create_app()
    app.run()
