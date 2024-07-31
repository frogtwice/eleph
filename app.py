import logging
import os

import eleph

logging.basicConfig(level=logging.INFO)

app = eleph.create_flask_app(
    "ELEPH",
    uri=os.environ.get("URI", ""),
    log=True
)
