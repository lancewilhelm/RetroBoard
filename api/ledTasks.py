#!/usr/bin/env python3
import time
from datetime import datetime, timedelta
from setup import settings, sock
import time
from PIL import Image
import logging
import threading
import numpy as np
import yfinance as yf
import math
import json

# If we are not in debug mode then import the led matrix
if not settings.debug:
	from setup import matrix
	offscreen_canvas = matrix.CreateFrameCanvas()

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

def set_pixel(canvas, x, y, r, g, b):
	if x >= settings.width or y >= settings.height:
		return

	if settings.debug:
		canvas[x, y, 0] = r
		canvas[x, y, 1] = g
		canvas[x, y, 2] = b
	else:
		canvas.SetPixel(x, y, r, g, b)
	return

def clear_screen(canvas):
	if settings.debug:
		temp_canvas = np.ndarray((settings.width, settings.height, 3), dtype=int)
		temp_canvas.fill(0)
		return temp_canvas
	else:
		matrix.Clear()
		return canvas
	
def update_screen(canvas):
	if settings.debug:
		settings.web_canvas = canvas
		settings.update_canvas_bool = True
		return canvas
	else:
		return matrix.SwapOnVSync(canvas)

# Creates a linear color gradient
def set_color_grad(start_color, end_color):
	start_color_array = np.array([start_color['r'], start_color['g'], start_color['b']])
	end_color_array = np.array([end_color['r'], end_color['g'], end_color['b']])
	t_0_pixel = start_color['offset'] * settings.width
	t_1_pixel = end_color['offset'] * settings.width

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
			if pixel and (pixel_x < settings.width and pixel_y < settings.height):
				if color == None:
					set_pixel(canvas, pixel_x, pixel_y, cm[pixel_x, pixel_y, 0], cm[pixel_x, pixel_y, 1], cm[pixel_x, pixel_y, 2])
				else:
					set_pixel(canvas, pixel_x, pixel_y, color[0], color[1], color[2])

def draw_text(canvas, x, y, font, text, color=None):
	char_x = x
	for char in text:
		glyph = font[ord(char)]
		char_y = y + (font.ptSize - glyph.bbH) - glyph.bbY
		char_x += glyph.bbX
		draw_glyph(canvas, char_x, char_y, glyph, color)
		char_x += (glyph.advance - glyph.bbX)

# Websocket test
@sock.route('/data')
def send_data(sock):
	while True:
		if settings.update_canvas_bool:
			sock.send(json.dumps(settings.web_canvas.tolist()))
			settings.update_canvas_bool = False

cent_x = int(settings.width / 2)
cent_y = int(settings.height / 2)

#-------------------------------------------------------------------------
# Stoppable Thread Class:
#-------------------------------------------------------------------------
class StoppableThread(threading.Thread):
	''' Class used for making threads stoppable. Used to run led tasks on screen while other things run and then stop when requested'''
	def __init__(self,  *args, **kwargs):
		super(StoppableThread, self).__init__(*args, **kwargs)
		self._stop_event = threading.Event()
		self.loadSettings()
		if settings.debug:
			self.offscreen_canvas = np.ndarray((settings.width, settings.height, 3), dtype=int)
			self.offscreen_canvas.fill(0)
		else:
			self.offscreen_canvas = matrix.CreateFrameCanvas()

	def stop(self):
		logging.debug('stopping thread for {}'.format(type(self).__name__))
		self._stop_event.set()
		self.offscreen_canvas = clear_screen(self.offscreen_canvas)

	def stopped(self):
		return self._stop_event.is_set()

	def loadSettings(self):
		logging.debug('loading settings for {}'.format(type(self).__name__))
		self.font = settings.load_font(settings.main['font_dict'][settings.main['active_font']])
		self.font_width = self.font[ord(' ')].advance
		self.font_height = self.font.ptSize
		settings.update_settings_bool = False

		if settings.main['color_mode'] == 'static':
			set_static_color(settings.main['static_color'])
		elif settings.main['color_mode'] == 'gradient':
			set_color_grad(settings.main['gradient'][0], settings.main['gradient'][-1])

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
		self.position = {
			'x': int(cent_x - (5 * self.font_width) / 2),
			'y': int(cent_y - self.font_height / 2)
		}

	def run(self):
		logging.debug('starting clock')
		# if not settings.debug:
		# 	offscreen_canvas = matrix.CreateFrameCanvas()

		# Run the clock loop until stopped
		while True:
			# Check to see if we have stopped
			if self.stopped():
				self.offscreen_canvas = clear_screen(self.offscreen_canvas)
				return

			# Check for a settings change that needs fto be loaded
			if settings.update_settings_bool:
				self.loadSettings()

			self.offscreen_canvas = clear_screen(self.offscreen_canvas)
			
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
			draw_text(self.offscreen_canvas, self.position['x'], self.position['y'], self.font, time_str)
			self.offscreen_canvas = update_screen(self.offscreen_canvas)

			time.sleep(0.05)	# Time buffer added so as to not overload the system

class TextClock(StoppableThread):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.name = 'text_clock'
		self.num2words = {1: 'One', 2: 'Two', 3: 'Three', 4: 'Four', 5: 'Five', 6: 'Six', 7: 'Seven', 8: 'Eight', 9: 'Nine', 10: 'Ten', 11: 'Eleven', 12: 'Twelve', 13: 'Thirteen', 14: 'Fourteen', 15: 'Fifteen', 16: 'Sixteen', 17: 'Seventeen', 18: 'Eighteen', 19: 'Nineteen', 20: 'Twenty', 30: 'Thirty', 40: 'Forty', 50: 'Fifty', 60: 'Sixty', 70: 'Seventy', 80: 'Eighty', 90: 'Ninety', 0: 'Zero'}
		self.position = {
			'x': int(cent_x - (5 * self.font_width) / 2),
			'y': int(cent_y - self.font_height / 2)
		}

	def run(self):
		logging.debug('starting text clock')

		# Run the clock loop until stopped
		while True:
			# Check to see if we have stopped
			if self.stopped():
				self.offscreen_canvas = clear_screen(self.offscreen_canvas)
				return

			# Check for a settings change that needs fto be loaded
			if settings.update_settings_bool:
				self.loadSettings()

			self.offscreen_canvas = clear_screen(self.offscreen_canvas)

			# Grab the latest time
			t = time.localtime()
			hours = t.tm_hour
			mins = t.tm_min

			# Create the min string
			if mins < 20:
				min_str = self.num2words[mins]
			else:
				min_str = self.num2words[(math.floor(mins / 10) * 10)] + ' ' + self.num2words[(mins - (math.floor(mins / 10) * 10))]

			# Create the hour string
			if hours < 20:
				hour_str = self.num2words[hours]
			else:
				hour_str = self.num2words[(math.floor(hours / 10) * 10)] + ' ' + self.num2words[(hours - (math.floor(hours / 10) * 10))]
			
			# Write the actual drawing to the canvas and then display
			hour_x = int(cent_x - (len(hour_str) * 4 / 2))
			min_x = int(cent_x - (len(min_str) * 4 / 2))
			draw_text(self.offscreen_canvas, hour_x, self.position['y'] - 3, self.font, hour_str)
			draw_text(self.offscreen_canvas, min_x, self.position['y'] + 3, self.font, min_str)
			self.offscreen_canvas = update_screen(self.offscreen_canvas)
			time.sleep(0.05)	# Time buffer added so as to not overload the system

class Picture(StoppableThread):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.name = 'picture'

	def run(self):
		self.image = Image.open('./images/lancesig.png').convert('RGB')
		# self.image.resize((settings.width, settings.height), Image.ANTIALIAS)

		self.offscreen_canvas.SetImage(self.image, 0)

		update_screen(self.offscreen_canvas)

class Solid(StoppableThread):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.name = 'solid'

	def run(self):
		cm = settings.color_matrix

		while True:
			# Check to see if we have stopped
			if self.stopped():
				self.offscreen_canvas = clear_screen(self.offscreen_canvas)
				return

			# Check for a settings change that needs fto be loaded
			if settings.update_settings_bool:
				self.loadSettings()

			self.offscreen_canvas = clear_screen(self.offscreen_canvas)

			for x in range(settings.width):
				for y in range(settings.height):
					set_pixel(self.offscreen_canvas, x, y, cm[x, y, 0], cm[x, y, 1], cm[x, y, 2])

			time.sleep(0.05)	# Time buffer added so as to not overload the system
			self.offscreen_canvas = update_screen(self.offscreen_canvas)

class Ticker(StoppableThread):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.name = 'ticker'

		self.graph_color = [255, 255, 255]
		self.graph_height = 16
		self.min_val = 0
		self.max_val = 0
		self.price_update_time = 0

	def get_prices(self):
		logging.debug('getting prices')
		
		yf_ticker = yf.Ticker(settings.ticker['symbol'])
		self.df = yf_ticker.history(period=settings.ticker['graph_period'], interval=settings.ticker['graph_resolution'], prepost=True).sort_index(ascending=False).reset_index()
		if len(self.df) > 0:
			self.df['t'] = self.df['Datetime'].apply(lambda x: int(x.value / 10**6))
			self.df = self.df[:64]

			self.c_vals = list(self.df['Close'])
			self.o_vals = list(self.df['Open'])
			self.l_vals = list(self.df['Low'])
			self.h_vals = list(self.df['High'])
			self.t_vals = list(self.df['t'])
		
	def draw_screen(self):
		self.offscreen_canvas = clear_screen(self.offscreen_canvas)
		display_symbol = settings.ticker['symbol']

		draw_text(self.offscreen_canvas, 2, 1, self.font, display_symbol, [255, 255, 255])

		if len(self.df) > 0:
			price = '${:.2f}'.format(self.c_vals[0])
			draw_text(self.offscreen_canvas, 2, 7, self.font, price, [255, 255, 255])
			price_diff = self.c_vals[0] - self.c_vals[-1]
			if price_diff > 0:
				self.graph_color = [0, 255, 0]
				price_diff = '+' + '{:.2f}'.format(price_diff)
			else:
				self.graph_color = [255, 0, 0]
				price_diff = '{:.2f}'.format(price_diff)

			price_diff_location = len(price) * 4 + 2
			draw_text(self.offscreen_canvas, price_diff_location, 7, self.font, '{}'.format(price_diff), self.graph_color)

			c_y = [settings.height - int((self.c_vals[i] - min(self.c_vals)) / (max(self.c_vals) - min(self.c_vals)) * self.graph_height) - 1 for i in range(len(self.c_vals))]
			h_y = [settings.height - int((self.h_vals[i] - min(self.l_vals)) / (max(self.h_vals) - min(self.l_vals)) * self.graph_height) - 1 for i in range(len(self.h_vals))]
			l_y = [settings.height - int((self.l_vals[i] - min(self.l_vals)) / (max(self.h_vals) - min(self.l_vals)) * self.graph_height) - 1 for i in range(len(self.h_vals))]
			
			if settings.ticker['graph_type'] == 'diff':
				# Draw axis in gray
				for i, y in enumerate(c_y):
					if self.c_vals[i] < self.c_vals[-1]:
						for j in range(c_y[-1], y + 1):
							set_pixel(self.offscreen_canvas, settings.width - (i + 1), j, 50, 0, 0)
						set_pixel(self.offscreen_canvas, settings.width - (i + 1), y, 250, 0, 0)
						if i != (len(c_y)-1) and y > c_y[i + 1]:
							for j in range(max(c_y[i+1], c_y[-1]), y):
								set_pixel(self.offscreen_canvas, settings.width - (i + 1), j, 250, 0, 0)
						if i != 0 and y > c_y[i - 1]:
							for j in range(max(c_y[i-1], c_y[-1]), y):
								set_pixel(self.offscreen_canvas, settings.width - (i + 1), j, 250, 0, 0)
					else:
						for j in range(y, c_y[-1] + 1):
							set_pixel(self.offscreen_canvas, settings.width - (i + 1), j, 0, 50, 0)
						set_pixel(self.offscreen_canvas, settings.width - (i + 1), y, 0, 250, 0)
						if i != (len(c_y)-1) and y < c_y[i + 1]:
							for j in range(y, min(c_y[i+1], c_y[-1])):
								set_pixel(self.offscreen_canvas, settings.width - (i + 1), j, 0, 250, 0)
						if i != 0 and y < c_y[i - 1]:
							for j in range(y, min(c_y[i-1], c_y[-1])):
								set_pixel(self.offscreen_canvas, settings.width - (i + 1), j, 0, 250, 0)

			elif settings.ticker['graph_type'] == 'filled':
				for i, y in enumerate(c_y):
					for j in range(y, settings.height):
						set_pixel(self.offscreen_canvas, settings.width - (i + 1), j, self.graph_color[0] * 0.2, self.graph_color[1] * 0.2, self.graph_color[2] * 0.2)
					set_pixel(self.offscreen_canvas, settings.width - (i + 1), y, self.graph_color[0], self.graph_color[1], self.graph_color[2])
					if i != 0 and y < c_y[i-1]:
						for j in range(y, c_y[i-1]):
							set_pixel(self.offscreen_canvas, settings.width - (i + 1), j, self.graph_color[0], self.graph_color[1], self.graph_color[2])
					elif i != len(c_y) and y > c_y[i-1]:
						for j in range(c_y[i-1], y):
							set_pixel(self.offscreen_canvas, settings.width - (i), j, self.graph_color[0], self.graph_color[1], self.graph_color[2])
					
			elif settings.ticker['graph_type'] == 'bar':
				for i, c_val in enumerate(self.c_vals):
					if c_val - self.o_vals[i] > 0:
						if h_y[i] != l_y[i]:
							for j in range(h_y[i], l_y[i]):
								set_pixel(self.offscreen_canvas, settings.width - (i + 1), j, 0, 255, 0)
						else:
							set_pixel(self.offscreen_canvas, settings.width - (i + 1), h_y[i], 0, 255, 0)
					else:
						if h_y[i] != l_y[i]:
							for j in range(h_y[i], l_y[i]):
								set_pixel(self.offscreen_canvas, settings.width - (i + 1), j, 255, 0, 0)
						else:
							set_pixel(self.offscreen_canvas, settings.width - (i + 1), h_y[i], 255, 0, 0)
		else:
			draw_text(self.offscreen_canvas, 19, 20, self.font, 'NO DATA', [255, 255, 255])

		self.offscreen_canvas = update_screen(self.offscreen_canvas)

	def run(self):
		logging.debug('starting ticker')

		self.price_update_time = int(time.mktime((datetime.now() + timedelta(seconds = 15)).timetuple()))
		self.get_prices()
		self.draw_screen()

		# Run the ticker loop until stopped
		while True:
			# Check to see if we have stopped
			if self.stopped():
				self.offscreen_canvas = clear_screen(self.offscreen_canvas)
				return

			# Check for a settings change that needs to be loaded
			if settings.update_settings_bool:
				self.loadSettings()
				self.get_prices()
				self.draw_screen()
				self.price_update_time = int(time.mktime((datetime.now() + timedelta(seconds = 15)).timetuple()))
			
			t = int(time.mktime(datetime.now().timetuple()))
			if t > self.price_update_time:
				self.get_prices()
				self.draw_screen()
				self.price_update_time = int(time.mktime((datetime.now() + timedelta(seconds = 15)).timetuple()))

			time.sleep(0.05)

#-------------------------------------------------------------------------
# LED Driving functions that are dependent on the objects defined above
#-------------------------------------------------------------------------
def start_led_app(app):
	if app == 'clock':
		task = Clock()
		task.start()
		settings.current_thread = task
		settings.main['running_apps'].append(task.name)
		settings.dump_settings()
	elif app == 'text_clock':
		task = TextClock()
		task.start()
		settings.current_thread = task
		settings.main['running_apps'].append(task.name)
		settings.dump_settings()
	elif app == 'picture':
		task = Picture()
		task.start()
		settings.current_thread = task
		settings.main['running_apps'].append(task.name)
		settings.dump_settings()
	elif app == 'solid':
		task = Solid()
		task.start()
		settings.current_thread = task
		settings.main['running_apps'].append(task.name)
		settings.dump_settings()
	elif app == 'ticker':
		task = Ticker()
		task.start()
		settings.current_thread = task
		settings.main['running_apps'].append(task.name)
		settings.dump_settings()

def stop_current_led_app():
	settings.current_thread.stop()
	settings.current_thread = None
	settings.main['running_apps'] = []