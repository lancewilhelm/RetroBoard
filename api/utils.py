from flask import Flask
from flask_cors import CORS
from celery import Celery
from rgbmatrix import RGBMatrix, RGBMatrixOptions
import sys
import os

# Create the quart object
api = Flask(__name__)
CORS(api)       # CORS BS that we likely don't need to worry about'

def make_celery(app):
    celery = Celery(
        app.import_name,
        backend='rpc://',
        broker='pyamqp://',
        imports=('ledTasks',)
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery

celery_app = make_celery(api)

sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/..'))

options = RGBMatrixOptions()

# Refer to the rpi-rgb-led-matrix python binding docs for the meanings of each option
options.hardware_mapping = 'adafruit-hat'
options.rows = 32
options.cols = 64
options.chain_length = 1
options.parallel = 1
options.row_address_type = 0
options.multiplexing = 0
options.pwm_bits = 11
options.brightness = 100
options.pwm_lsb_nanoseconds = 130
options.led_rgb_sequence = 'RGB'
options.pixel_mapper_config = ''
options.gpio_slowdown = 1
options.disable_hardware_pulsing = False

matrix = RGBMatrix(options = options)