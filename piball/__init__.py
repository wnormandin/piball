__version__ = '0.0.0'

import os
import logging


# TODO: better logging config
logging.basicConfig(level=logging.INFO)
db_url = os.getenv('PIBALL_DB_URL')
