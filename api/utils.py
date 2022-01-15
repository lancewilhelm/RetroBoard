from posixpath import defpath
from flask import Flask
from flask_cors import CORS
from rgbmatrix import RGBMatrix, RGBMatrixOptions
import sys
import os
import logging
import argparse 
from collections import defaultdict

#-------------------------------------------------------------------------
# Argparsing
#-------------------------------------------------------------------------
parser = argparse.ArgumentParser()
parser.add_argument('-d', "--debug-mode", action="store", help="Determines what debug mode will be displayed on screen. [info (default), debug, warning, critical]", default="info", type=str)

args = parser.parse_args()

#-------------------------------------------------------------------------
# Logging confuguration
#-------------------------------------------------------------------------
logging.basicConfig(level=logging.DEBUG, filename='log.txt', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
console = logging.StreamHandler()
if args.debug_mode == 'info':
	console.setLevel(logging.INFO)
elif args.debug_mode == 'debug':
	console.setLevel(logging.DEBUG)
logging.getLogger().addHandler(console)

#-------------------------------------------------------------------------
# Flask server configuration
#-------------------------------------------------------------------------
logging.debug('creating the api flask object')
api = Flask(__name__)
CORS(api)       # CORS BS that we likely don't need to worry about'

#-------------------------------------------------------------------------
# LED Matrix configuration
#-------------------------------------------------------------------------
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
cent_x = matrix.width / 2
cent_y = matrix.height / 2

# Grab the list of fonts in the font folder
logging.debug('forming font dictionary')
font_dict = defaultdict(str)
path = '/home/pi/RetroBoard/api/fonts/'
dir = os.fsencode(path)
dir_list = os.listdir(dir)

for file in dir_list:
	filename = os.fsencode(file).decode('UTF-8')
	if filename.endswith('.bdf'):
		file_path = os.path.join(path, filename)
		font_dict[filename[:-4]] = file_path#

logging.debug('utils complete')