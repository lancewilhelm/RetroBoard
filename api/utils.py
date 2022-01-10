from flask import Flask
from flask_cors import CORS
from celery import Celery
from rgbmatrix import RGBMatrix, RGBMatrixOptions
import sys
import os

# Create the quart object
api = Flask(__name__)
CORS(api)       # CORS BS that we likely don't need to worry about'

celery_app = Celery(
        'tasks',
        backend='rpc://',
        broker='pyamqp://',
        imports=('ledTasks',)
    )

sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/..'))

options = RGBMatrixOptions()

# Refer to the rpi-rgb-led-matrix python binding docs for the meanings of each option
# Configuration for the matrix
options = RGBMatrixOptions()
options.rows = 32
options.cols = 64
options.chain_length = 1
options.parallel = 1
options.hardware_mapping = 'adafruit-hat'
options.drop_privileges = False

matrix = RGBMatrix(options = options)