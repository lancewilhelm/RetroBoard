#!/usr/bin/env python3
import time
from datetime import datetime, timedelta
from setup import matrix, settings
import time
from PIL import Image
import logging
import threading
import numpy as np
import requests
import websocket
import json

#-------------------------------------------------------------------------
# Utility functions/variables:
#-------------------------------------------------------------------------
def scale_color(val, lo, hi):
	'''Scales up any number into the 0 to 255 scale. This is useful for color calculations.'''
	if val < lo:
		return 0
	if val > hi:
		return 255
	return 255 * (val - lo) / (hi - lo)

def rotate(x, y, sin, cos):
	'''Used for the rotating block animation. Might be useful elsewhere'''
	return x * cos - y * sin, x * sin + y * cos

def clamp(n, minn, maxn):
	return max(min(maxn, n), minn)

# Creates a linear color gradient
def set_color_grad(start_color, end_color):
	start_color_array = np.array([start_color['r'], start_color['g'], start_color['b']])
	end_color_array = np.array([end_color['r'], end_color['g'], end_color['b']])
	t_0_pixel = start_color['offset'] * matrix.width
	t_1_pixel = end_color['offset'] * matrix.width

	# Initially this is assuming moving from the far left of the grid to the right. Angles will be added later
	width, height, _ = settings.color_matrix.shape

	for i in range(width):
		new_color = ((end_color_array - start_color_array) * clamp((i - t_0_pixel) / (t_1_pixel - t_0_pixel), 0.0, 1.0) + start_color_array).astype(int)
		settings.color_matrix[i,:] = new_color

def set_static_color(color):
	color_array = np.array([color['r'], color['g'], color['b']])
	settings.color_matrix[:, :] = color_array

def draw_glyph(canvas, x, y, glyph, color=None):
	cm = settings.color_matrix
	for i, row in enumerate(glyph.iter_pixels()):
		for j, pixel, in enumerate(row):
			pixel_x = x + j
			pixel_y = y + i
			if pixel:
				if color == None:
					canvas.SetPixel(pixel_x, pixel_y, cm[pixel_x, pixel_y, 0], cm[pixel_x, pixel_y, 1], cm[pixel_x, pixel_y, 2])
				else:
					canvas.SetPixel(pixel_x, pixel_y, color[0], color[1], color[2])

def draw_text(canvas, x, y, font, text, color=None):
	char_x = x
	for char in text:
		glyph = font[ord(char)]
		char_y = y + (font.ptSize - glyph.bbH) - glyph.bbY
		char_x += glyph.bbX
		draw_glyph(canvas, char_x, char_y, glyph, color)
		char_x += (glyph.advance - glyph.bbX)

cent_x = int(matrix.width / 2)
cent_y = int(matrix.height / 2)

#-------------------------------------------------------------------------
# Stoppable Thread Class:
#-------------------------------------------------------------------------
class StoppableThread(threading.Thread):
	''' Class used for making threads stoppable. Used to run led tasks on screen while other things run and then stop when requested'''
	def __init__(self,  *args, **kwargs):
		super(StoppableThread, self).__init__(*args, **kwargs)
		self._stop_event = threading.Event()
		self.loadSettings()

	def stop(self):
		logging.debug('stopping thread for {}'.format(type(self).__name__))
		self._stop_event.set()
		matrix.Clear()

	def stopped(self):
		return self._stop_event.is_set()

	def loadSettings(self):
		logging.debug('loading settings for {}'.format(type(self).__name__))
		self.font = settings.load_font(settings.font_dict[settings.active_font])
		self.font_width = self.font[ord(' ')].advance
		self.font_height = self.font.ptSize
		self.position = {
			'x': int(cent_x - (5 * self.font_width) / 2),
			'y': int(cent_y - self.font_height / 2)
		}
		settings.update_bool = False

		if settings.color_mode == 'static':
			set_static_color(settings.static_color)
		elif settings.color_mode == 'gradient':
			set_color_grad(settings.gradient[0], settings.gradient[-1])

#-------------------------------------------------------------------------
# LED Animations: 
#   Animations are in the form of classes from which objects can be made
# wherever needed. This allows them to inherit the stoppable thread class
# that is needed to run these animations asynchronously
#-------------------------------------------------------------------------

class Clock(StoppableThread):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.name = 'clock'

	def run(self):
		logging.debug('starting clock')

		# Establish the offscreen buffer to store changes too before publishing
		offscreen_canvas = matrix.CreateFrameCanvas()

		# Run the clock loop until stopped
		while True:
			# Check to see if we have stopped
			if self.stopped():
				matrix.Clear()
				return

			# Check for a settings change that needs fto be loaded
			if settings.update_bool:
				self.loadSettings()

			offscreen_canvas.Clear()
			# Grab the latest time
			t = time.localtime()
			hours = t.tm_hour
			mins = t.tm_min
			secs = t.tm_sec

			# Create the min string
			if mins < 10:
				min_str = '0' + str(mins)
			else:
				min_str = str(mins)

			# Create the hour string
			if hours < 10:
				hour_str = '0' + str(hours)
			else:
				hour_str = str(hours)

			# Create the time string either with a lit up colon or not
			if secs % 2 == 1:
				# Even seconds, concatenate the strings with a colon in the middle
				time_str = hour_str + ' ' + min_str
			else:
				# Odd seconds, concatenate the strings with a semicolon(blank) in the middle
				time_str = hour_str + ':' + min_str
			
			# Write the actual drawing to the canvas and then display
			draw_text(offscreen_canvas, self.position['x'], self.position['y'], self.font, time_str)
			time.sleep(0.05)	# Time buffer added so as to not overload the system
			offscreen_canvas = matrix.SwapOnVSync(offscreen_canvas)

class Picture(StoppableThread):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.name = 'picture'

	def run(self):
		self.image = Image.open('./images/lancesig.png').convert('RGB')
		# self.image.resize((matrix.width, matrix.height), Image.ANTIALIAS)

		double_buffer = matrix.CreateFrameCanvas()

		double_buffer.SetImage(self.image, 0)

		matrix.SwapOnVSync(double_buffer)

class Solid(StoppableThread):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.name = 'solid'

	def run(self):
		cm = settings.color_matrix
		# Establish the offscreen buffer to store changes too before publishing
		offscreen_canvas = matrix.CreateFrameCanvas()

		while True:
			# Check to see if we have stopped
			if self.stopped():
				matrix.Clear()
				return

			# Check for a settings change that needs fto be loaded
			if settings.update_bool:
				self.loadSettings()

			offscreen_canvas.Clear()

			for x in range(matrix.width):
				for y in range(matrix.height):
					offscreen_canvas.SetPixel(x, y, cm[x, y, 0], cm[x, y, 1], cm[x, y, 2])

			time.sleep(0.05)	# Time buffer added so as to not overload the system
			offscreen_canvas = matrix.SwapOnVSync(offscreen_canvas)

class Ticker(StoppableThread):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.name = 'ticker'
		self.ticker = 'BINANCE:ETHUSDT'
		self.ws = websocket.WebSocketApp('wss://ws.finnhub.io?token={}'.format(settings.apikeys['finnhub']), on_open=self.on_ws_open, on_message = self.on_ws_message, on_close = self.on_ws_close)
		self.offscreen_canvas = matrix.CreateFrameCanvas()
		self.historical_prices = {}
		self.graph_color = [255, 255, 255]
		self.graph_height = 18
		self.min_val = 0
		self.max_val = 0
		self.historical_update_time = 0

	def on_ws_message(self, ws, message):
		if self.stopped():
			self.ws.close()
		else:
			try:
				data = json.loads(message)['data']
				price = float(data[0]['p'])
				time = int(data[0]['t'])
				self.offscreen_canvas.Clear()
				draw_text(self.offscreen_canvas, 2, 1, self.font, self.ticker, [255, 255, 255])
				draw_text(self.offscreen_canvas, 2, 7, self.font, '${:.2f}'.format(price), [255, 255, 255])
				price_diff = price - self.c_vals[63]
				if price_diff > 0:
					self.graph_color = [0, 255, 0]
				else:
					self.graph_color = [255, 0, 0]

				draw_text(self.offscreen_canvas, 35, 7, self.font, '{:.2f}'.format(price_diff), self.graph_color)

				# if the timestamp of the current received price is greater than 1s then refresh the historical data
				if time > self.historical_update_time * 1000:
					self.get_historical_prices()

				self.draw_graph()
				self.offscreen_canvas = matrix.SwapOnVSync(self.offscreen_canvas)
			except:
				logging.debug('unable to handle or get live stock price')

	def on_ws_close(self, ws, code, msg):
		print('closing websocket')
	
	def on_ws_open(self, ws):
		send_string = '{"type":"subscribe","symbol":"' + self.ticker + '"}'
		ws.send(send_string)

	def get_historical_prices(self):
		logging.debug('getting historical data')
		resolution = '15'
		to_time = int(time.mktime(datetime.now().timetuple()))
		from_time = int(time.mktime((datetime.now() - timedelta(days = 1)).timetuple()))
		url = 'https://finnhub.io/api/v1/crypto/candle?symbol={}&resolution={}&from={}&to={}&token={}'.format(self.ticker, resolution, from_time, to_time, settings.apikeys['finnhub'])
		r = requests.get(url)
		data = r.json()
		self.historical_prices = data
		self.c_vals = data['c']
		self.max_c_val = max(self.c_vals)
		self.min_c_val = min(self.c_vals)
		self.historical_update_time = int(time.mktime((datetime.now() + timedelta(minutes = 1)).timetuple()))
		
	def draw_graph(self):
		for i in range(matrix.width):
			y = 32 - int((self.c_vals[i] - self.min_c_val) / (self.max_c_val - self.min_c_val) * self.graph_height)
			for j in range(y, matrix.height):
				self.offscreen_canvas.SetPixel(matrix.width - (i + 1), j, self.graph_color[0], self.graph_color[1], self.graph_color[2])

	def run(self):
		logging.debug('starting ticker')

		self.offscreen_canvas.Clear()

		self.get_historical_prices()

		self.ws.run_forever()

		# Run the ticker loop until stopped
		while True:
			# Check to see if we have stopped
			if self.stopped():
				matrix.Clear()
				return

			# Check for a settings change that needs fto be loaded
			if settings.update_bool:
				self.loadSettings()

#-------------------------------------------------------------------------
# LED Driving functions that are dependent on the objects defined above
#-------------------------------------------------------------------------
def start_led_app(app):
	if app == 'clock':
		task = Clock()
		task.start()
		settings.current_thread = task
		settings.running_apps.append('clock')
		settings.dump_settings()
	elif app == 'picture':
		task = Picture()
		task.start()
		settings.current_thread = task
		settings.running_apps.append('picture')
		settings.dump_settings()
	elif app == 'solid':
		task = Solid()
		task.start()
		settings.current_thread = task
		settings.running_apps.append('solid')
		settings.dump_settings()
	elif app == 'ticker':
		task = Ticker()
		task.start()
		settings.current_thread = task
		settings.running_apps.append('ticker')
		settings.dump_settings()

def stop_current_led_app():
	settings.current_thread.stop()
	settings.current_thread = None
	settings.running_apps = []