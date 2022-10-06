import os
import threading
from app import checker
from datetime import datetime
from flask import Flask
import time
import random
import logging


app = Flask(__name__)

start_datetime = datetime.utcnow()

checker_instance = checker.PETROSAdbchecker()

time.sleep(random.randint(5, 150))
threading.Thread(target=checker_instance.run).start()


@app.route("/")
def default():

    return "ok", 200


@app.route("/status")
def queues():
    status = {}

    status['start_datetime'] = start_datetime
    return status, 200


if __name__ == "__main__":
    print('Starting the checker')
    logging.info('Starting the checker')
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
