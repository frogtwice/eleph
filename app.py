import logging
import os

import eleph
from eleph import MYSQLDatabase

logging.basicConfig(level=logging.INFO)

database = MYSQLDatabase(
    host=os.environ["MYSQL_HOST"],
    user=os.environ["MYSQL_USER"],
    password=os.environ["MYSQL_PASSWORD"],
    database=os.environ["MYSQL_DATABASE"]
)


app = eleph.create_flask_app(
    "ELEPH",
    uri=os.environ["URI"],
    database=database,
    log=True
)
