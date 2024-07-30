import logging
import os

import eleph

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("app")

logger.info("Flask App: Creating...")
flask_app = eleph.FlaskApp(uri=os.environ.get("URI", ""))
logger.info("Flask App: Created.")
app = flask_app.get_app()
