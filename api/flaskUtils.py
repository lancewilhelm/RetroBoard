from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

from ledUtils import RotatingBlockGenerator

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/api/rotate', methods=['GET'])
def runRotate():
    rotating_block_generator = RotatingBlockGenerator()
    if (not rotating_block_generator.process()):
        rotating_block_generator.print_help()
    return