import time
from flask import Flask

app = Flask(__name__)

@app.route('/api/time')
def get_current_time():
    return {'time': time.time()}

@app.route('/api/image', methods=['POST'])
def start_main():
    
    return send_file('src/05_Visualization/Models/VisualAnzeights.html')
