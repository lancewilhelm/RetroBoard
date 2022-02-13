from ast import parse
from flask import Flask
from flask_cors import CORS
from flask_sock import Sock
import sys
import os
import logging
import argparse 
from collections import defaultdict
import json
import numpy as np
from bdflib import reader

#-------------------------------------------------------------------------
# Argparsing
#-------------------------------------------------------------------------
parser = argparse.ArgumentParser()
parser.add_argument('-l', "--logging-level", action="store", help="Determines what logging mode will be displayed on screen. [info (default), debug]", default="info", type=str)
parser.add_argument('-d', '--debug', action='store_true', help='Runs the application without driving the led matrix. The matrix will be simulated at the index page of the api')

args = parser.parse_args()

#-------------------------------------------------------------------------
# Logging configuration
#-------------------------------------------------------------------------
logging.basicConfig(level=logging.DEBUG, filename='log.txt', filemode='w', format='%(asctime)s - %(levelname)s - %(message)s', datefmt="%Y-%m-%d %H:%M:%S")
console = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', "%Y-%m-%d %H:%M:%S")
console.setFormatter(formatter)
if args.logging_level == 'info':
	console.setLevel(logging.INFO)
elif args.logging_level == 'debug':
	console.setLevel(logging.DEBUG)
logging.getLogger().addHandler(console)

#-------------------------------------------------------------------------
# Flask server configuration
#-------------------------------------------------------------------------
logging.debug('creating the api flask object')
api = Flask(__name__)
sock = Sock(api)
CORS(api)       # CORS BS that we likely don't need to worry about'

#-------------------------------------------------------------------------
# LED Matrix configuration
# Only load these items if we are not in debug mode
#-------------------------------------------------------------------------
if not args.debug:
	logging.debug('setting up the led matrix options')

	from rgbmatrix import RGBMatrix, RGBMatrixOptions
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
	options.limit_refresh_rate_hz = 0
	options.disable_hardware_pulsing = True

	matrix = RGBMatrix(options = options)
	offscreen_canvas = matrix.CreateFrameCanvas()

# Grab the list of fonts in the font folder
logging.debug('forming font dictionary')
font_dict = defaultdict(str)
path = 'fonts/'
dir = os.fsencode(path)
dir_list = os.listdir(dir)

for file in dir_list:
	filename = os.fsencode(file).decode('UTF-8')
	if filename.endswith('.bdf'):
		file_path = os.path.join(path, filename)
		font_dict[filename[:-4]] = file_path

#-------------------------------------------------------------------------
# Settings configuration
#-------------------------------------------------------------------------
class Settings():
	def __init__(self):
		# Initialize stored settings with some defaults
		self.main = {}
		self.main['font_dict'] = font_dict
		self.main['active_font'] = 'tom-thumb'
		self.main['static_color'] = {'r': 255, 'g': 255, 'b': 255, 'a': 1}
		self.main['gradient'] = [{'offset': 0.0, 'r': 0, 'g': 0, 'b': 255, 'a': 1}, {'offset': 1.0, 'r': 255, 'g': 0, 'b': 255, 'a': 1}]
		self.main['running_apps'] = ['clock']
		self.main['color_mode'] = 'gradient'
		self.main['brightness'] = 100

		self.ticker = {}
		self.ticker['symbol'] = 'ETH-USD'
		self.ticker['graph_type'] = 'bar'
		self.ticker['graph_resolution'] = '15m'
		self.ticker['graph_period'] = '2d'
 
		# Non stored settings
		self.current_thread = None
		self.update_settings_bool = True
		self.update_canvas_bool = True
		self.width = 64
		self.height = 32
		self.color_matrix = np.ndarray((self.width, self.height, 3), dtype=int)
		self.color_matrix.fill(255)
		self.web_canvas = np.ndarray((self.width, self.height, 3), dtype=int)
		self.web_canvas.fill(0)
		self.apikeys = {}
		self.debug = args.debug

	def dump_settings(self, settings=None):
		logging.debug('dumping settings to settings.json')
		if settings == None:
			settings = {'main': self.main, 'ticker': self.ticker}

		with open('../settings.json', 'w') as filehandle:
			json.dump(settings, filehandle)

	def import_settings(self):
		logging.debug('loading settings from settings.json')
		try:
			with open('../settings.json', 'r') as filehandle:
				settings = json.load(filehandle)

				self.main = settings['main']
				self.ticker = settings['ticker']

				if not self.debug:
					matrix.brightness = self.main['brightness']

				self.update_settings_bool = True

		except FileNotFoundError:
			logging.debug('no settings.json file exists, creating one...')
			self.dump_settings()

	def load_font(self, path):
		logging.debug('loading font {}'.format(path))
		with open(path, 'rb') as filehandle:
			font = reader.read_bdf(filehandle)
		return font

#  Create the settings object and then loads the settings from the stored file.
settings = Settings()
# settings.dump_settings()
settings.import_settings()

logging.debug('utils complete')