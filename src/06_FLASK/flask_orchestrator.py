import sys
import os
import time
from flask import Flask, request, render_template, jsonify
import visanz.main
from visanz.main import main_for_flask
import numpy as np
from PIL import Image
app = Flask(__name__)

file = None


@app.route('/api/startWorkflow', methods=['GET', 'POST'])
def start_workflow():

    print('---- START WORKFLOW ----')
    global file
    #os.system('{} {}'.format('python3', '../00_MAIN/main.py'))
    filestr = file.read()
    npimg = np.fromstring(filestr, np.uint8)
    img = Image.fromarray(npimg)
    nodes, edges, options = main_for_flask(img)
    return jsonify({
        'success': True,
        'nodes': nodes,
        'edges': edges,
        'groups': options,
    })


@app.route('/api/time')
def get_current_time():
    return {'time': time.time()}


@app.route('/api/uploadImage', methods=['POST'])
def upload_image():
    global file
    file = request.files.get('file')

    print(file)

    return jsonify({
        'success': True,
        'file': 'Received'
    })


@app.route("/")
def index():
    return render_template('../../AppVisualAnzeights/public/index.html')


if __name__ == "__main__":
    app.run(port=5000, debug=True)
