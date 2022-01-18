from flask import Flask
from flask_cors import CORS
from rgbmatrix import RGBMatrix, RGBMatrixOptions
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

args = parser.parse_args()

#-------------------------------------------------------------------------
# Logging confuguration
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
options.limit_refresh_rate_hz = 0
options.disable_hardware_pulsing = True

matrix = RGBMatrix(options = options)

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
		font_dict[filename[:-4]] = file_path

#-------------------------------------------------------------------------
# Settings configuration
#-------------------------------------------------------------------------
class Settings():
	def __init__(self):
		# Initialize stored settings with some defaults
		self.font_dict = font_dict
		self.active_font = font_dict['tom-thumb']
		self.static_color = {'r': 255, 'g': 255, 'b': 255, 'a': 1}
		self.grad_start_color = {'r': 0, 'g': 0, 'b': 255, 'a': 1}
		self.grad_end_color = {'r': 255, 'g': 0, 'b': 255, 'a': 1}
		self.running_apps = ['clock']
		self.color_mode = 'static'
		
		# Non stored settings
		self.current_thread = None
		self.update_bool = True
		self.color_matrix = np.ndarray((matrix.width, matrix.height, 3), dtype=int)
		self.color_matrix.fill(255)

	def dump_settings(self, settings=None):
		logging.debug('dumping settings to settings.json')
		if settings == None:
			settings = {
				'font_dict': self.font_dict,
				'active_font': self.active_font,
				'brightness': matrix.brightness,
				'static_color': self.static_color,
				'grad_start_color': self.grad_start_color,
				'grad_end_color': self.grad_end_color,
				'running_apps': self.running_apps,
				'color_mode': self.color_mode
			}

		with open('/home/pi/RetroBoard/settings.json', 'w') as filehandle:
			json.dump(settings, filehandle)

	def import_settings(self):
		logging.debug('loading settings from settings.json')
		try:
			with open('/home/pi/RetroBoard/settings.json', 'r') as filehandle:
				settings = json.load(filehandle)

				self.font_dict = settings['font_dict']
				self.active_font = settings['active_font']
				matrix.brightness = settings['brightness']
				self.static_color = settings['static_color']
				self.grad_start_color = settings['grad_start_color']
				self.grad_end_color = settings['grad_end_color']
				self.running_apps = settings['running_apps']
				self.color_mode = settings['color_mode']
				self.update_bool = True

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