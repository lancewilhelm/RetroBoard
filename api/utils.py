from flask import Flask
from flask_cors import CORS
from rgbmatrix import RGBMatrix, RGBMatrixOptions
import sys
import os
import logging 

# Configure the logging to write to file as well as screen
logging.basicConfig(level=logging.DEBUG, filename='log.txt', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
console = logging.StreamHandler()
console.setLevel(logging.INFO)
logging.getLogger().addHandler(console)

# Create the quart object
logging.debug('creating the api flask object')
api = Flask(__name__)
CORS(api)       # CORS BS that we likely don't need to worry about'


# Setup the LED matrix using the rpi-rgb-led-matrix library
logging.debug('setting up the led matrix options')
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/..'))
options = RGBMatrixOptions()

# Configuration for the matrix. Refer to the rpi-rgb-led-matrix python binding docs for the meanings of each option
options = RGBMatrixOptions()
options.rows = 32
options.cols = 64
options.chain_length = 1
options.parallel = 1
options.hardware_mapping = 'adafruit-hat'
options.drop_privileges = False
options.gpio_slowdown = 1
options.pwm_lsb_nanoseconds = 130
options.brightness = 100
options.multiplexing = 0
options.scan_mode = 1
options.pwm_bits = 11	# this seems to affect flickering of the leds somewhat
options.led_rgb_sequence = 'RGB'
options.row_address_type = 0

matrix = RGBMatrix(options = options)

logging.debug('utils complete')