import time
from flask import Flask
import logging

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

@app.route('/api/time')
def get_current_time():
    return {'time': time.time()}