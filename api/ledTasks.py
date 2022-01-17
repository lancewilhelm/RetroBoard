#!/usr/bin/env python3
import time
from utils import matrix, font_dict, settings
import time
from PIL import Image
import logging
import threading
from rgbmatrix import graphics
import math
import asyncio

#-------------------------------------------------------------------------
# Utility functions:
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

cent_x = matrix.width / 2
cent_y = matrix.height / 2

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

	def stopped(self):
		return self._stop_event.is_set()

	def loadSettings(self):
		logging.debug('loading settings for {}'.format(type(self).__name__))
		self.font = graphics.Font()
		self.font_path = settings.active_font
		self.font.LoadFont(self.font_path)
		self.font_height = self.font.height
		self.font_width = self.font.CharacterWidth(ord('L'))
		self.static_color = graphics.Color(settings.static_color['r'], settings.static_color['g'], settings.static_color['b'])
		self.position = {
			'x': cent_x - (5 * self.font_width / 2),
			'y': cent_y + (self.font_height / 2) - 2
		}
		settings.update_bool = False

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
			graphics.DrawText(offscreen_canvas, self.font, self.position['x'], self.position['y'], self.static_color, time_str)
			time.sleep(0.05)	# Time buffer added so as to not overload the system
			offscreen_canvas = matrix.SwapOnVSync(offscreen_canvas)

class Picture(StoppableThread):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.name = 'picture'

	def run(self):
		self.image = Image.open('./images/plant.png').convert('RGB')
		# self.image.resize((matrix.width, matrix.height), Image.ANTIALIAS)

		double_buffer = matrix.CreateFrameCanvas()

		double_buffer.SetImage(self.image, 0)

		matrix.SwapOnVSync(double_buffer)


# Tasks object array for storing active task and the task dictionary to look up new ones
running_tasks = []
task_dict = {
	'clock': Clock(),
	'picture': Picture()
}

def clock_function(self):
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
			graphics.DrawText(offscreen_canvas, self.font, self.position['x'], self.position['y'], self.staticColor, time_str)
			time.sleep(0.05)	# Time buffer added so as to not overload the system
			offscreen_canvas = matrix.SwapOnVSync(offscreen_canvas)