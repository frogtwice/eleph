import logging
import os

import eleph

logging.basicConfig(level=logging.INFO)

app = eleph.FlaskApp(uri=os.environ.get("URI", "")).get_app()
