import time
from flask import Flask

app = Flask(__name__)

@app.route('/api/time')
def get_current_time():
    return {'time': time.time()}

@app.route('/api/news_graph')
def get_current_news_graph():
    return send_file('src/05_Visualization/Models/VisualAnzeights.html')
