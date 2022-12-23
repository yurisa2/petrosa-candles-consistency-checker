from app import checker
from datetime import datetime
import time
import random
import logging


start_datetime = datetime.utcnow()

logging.warning('Will start now')
checker_instance = checker.PETROSAdbchecker()

time.sleep(random.randint(5, 150))
checker_instance.run()

