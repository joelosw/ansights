import sys
import os
from flask import Flask, request, render_template, jsonify
sys.path.append('./')
sys.path.append('./../..')
from src.visanz.main.main import main_for_flask
app = Flask(__name__)

file = None


@app.route('/api/startWorkflow', methods=['GET', 'POST'])
def start_workflow():

    print('---- START WORKFLOW ----')
    #os.system('{} {}'.format('python3', '../00_MAIN/main.py'))
    nodes, edges, options = main_for_flask(file)
    return jsonify({
        'success': True,
        'nodes': nodes,
        'edges': edges,
        'options': options,
    })


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
