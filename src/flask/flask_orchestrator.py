from visanz.main.main import main_for_flask
from PIL import Image
import cv2
import numpy as np
import sys
import time
from flask import Flask, request, render_template, jsonify
sys.path.append('./')
sys.path.append('./../..')
app = Flask(__name__)

img_file = None
npimg = None


@app.route('/api/startWorkflow', methods=['GET', 'POST'])
def start_workflow():

    print('---- START WORKFLOW ----')
    #os.system('{} {}'.format('python3', '../00_MAIN/main.py'))
    global file
    global npimg
    nodes, edges, options = main_for_flask(image=file)
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


@app.route("/")
def index():
    return render_template('../../AppVisualAnzeights/public/index.html')


if __name__ == "__main__":
    app.run(port=5000, debug=True)
