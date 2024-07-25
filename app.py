import logging
import os

import eleph

logging.basicConfig(level=logging.INFO)

app = eleph.create_app(uri=os.environ.get("URI", ""))
