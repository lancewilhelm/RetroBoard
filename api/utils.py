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
class Matrix(object):
    def __init__(self, *args, **kwargs):
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

        self.matrix = RGBMatrix(options = options)

    def rotatingBlock(self):
        cent_x = self.matrix.width / 2
        cent_y = self.matrix.height / 2

        rotate_square = min(self.matrix.width, self.matrix.height) * 1.41
        min_rotate = cent_x - rotate_square / 2
        max_rotate = cent_x + rotate_square / 2

        display_square = min(self.matrix.width, self.matrix.height) * 0.7
        min_display = cent_x - display_square / 2
        max_display = cent_x + display_square / 2

        deg_to_rad = 2 * math.pi/ 360
        rotation = 0
        offset_canvas = self.matrix.CreateFrameCanvas()

        while True:
            rotation += 1
            rotation %= 180

            for x in range(int(min_rotate), int(max_rotate)):
                for y in range(int(min_rotate), int(max_rotate)):
                    ret = rotate(x - cent_x, y - cent_x, deg_to_rad * rotation)
                    rot_x = ret["new_x"]
                    rot_y = ret["new_y"]

                    if x >= min_display and x < max_display and y >= min_display and y < max_display:
                        offset_canvas.SetPixel(rot_x + cent_x, rot_y + cent_y, scale_col(x, min_display, max_display), 255 - scale_col(y, min_display, max_display), scale_col(y, min_display, max_display))
                    else:
                        offset_canvas.SetPixel(rot_x + cent_x, rot_y + cent_y, 0, 0, 0)

            offset_canvas = self.matrix.SwapOnVSync(offset_canvas)

            if rotation == 0:
                return