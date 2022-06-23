from visanz.main.main import main_for_flask
from PIL import Image
import cv2
import numpy as np
import requests
import sys
import time
from flask import Flask, request, render_template, jsonify
sys.path.append('./')
sys.path.append('./../../')

app = Flask(__name__, static_folder='../../AppVisualAnzeights/build',
            static_url_path='/')

img_file = None
npimg = None
queryOptions = {'gnd': False,
                'dateRange': None, 'complexity': None}


@app.route('/api/startWorkflow', methods=['GET', 'POST'])
def start_workflow():

    print('---- START WORKFLOW ----')
    #os.system('{} {}'.format('python3', '../00_MAIN/main.py'))
    global file
    global queryOptions
    nodes, edges, options = main_for_flask(image=file, **queryOptions)
    return jsonify({
        'success': True,
        'nodes': nodes,
        'edges': edges,
        'options': options,
    })


@app.route('/api/time')
def get_current_time():
    return {'time': time.time()}


@app.route('/api/uploadImage', methods=['POST'])
def upload_image():
    global file
    global npimg
    filestr = request.files.get('file').read()
    npimg = np.fromstring(filestr, np.uint8)
    file = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

    return jsonify({
        'success': True,
        'file': 'Received'
    })


@app.route('/api/uploadMessage', methods=['POST'])
def upload_message():
    message = request.get_json(force=True)['message']
    print(message)

    return jsonify({
        'success': True,
        'text': 'Received'
    })


@app.route('/api/uploadDateRange', methods=['POST'])
def upload_DateRange():
    global queryOptions
    queryOptions['dateRange'] = request.get_json(force=True)['dateRange']

    return jsonify({
        'success': True,
        'dateRange': queryOptions['dateRange']
    })


@app.route('/api/uploadComplexity', methods=['POST'])
def upload_Complexity():
    global queryOptions
    queryOptions['complexity'] = request.get_json(force=True)['complexity']

    return jsonify({
        'success': True,
        'complexity': queryOptions['complexity']
    })


@app.route('/api/uploadGnd', methods=['POST'])
def upload_Gnd():
    global queryOptions
    queryOptions['gnd'] = request.get_json(force=True)['gnd']

    return jsonify({
        'success': True,
        'gnd': queryOptions['gnd']
    })


@app.route('/')
def index():
    return app.send_static_file('index.html')


if __name__ == "__main__":
    app.run(port=5000, debug=True)
