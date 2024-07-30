import logging
import os

import eleph

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("app")

flask_app = eleph.FlaskApp(uri=os.environ.get("URI", ""))
app = flask_app.get_app()
