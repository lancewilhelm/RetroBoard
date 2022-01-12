#!/usr/bin/env python3
import time
from utils import matrix
import time
from PIL import Image, ImageDraw
import logging
import threading
from rgbmatrix import graphics
import math

# Tasks object array which stores any current running tasks. This allows
# for threads to be stopped later by recalling their objects back up.
tasks = []

#-------------------------------------------------------------------------
# Utility functions:
#-------------------------------------------------------------------------
# The scale_color function is used to scale up any number into the 0 to 
# 255 scale. This is useful for color calculations
def scale_color(val, lo, hi):
	if val < lo:
		return 0
	if val > hi:
		return 255
	return 255 * (val - lo) / (hi - lo)

# Rotation function used for the rotating block animation. Might be useful
# elsewhere
def rotate(x, y, sin, cos):
	return x * cos - y * sin, x * sin + y * cos

#-------------------------------------------------------------------------
# Stoppable Thread Class:
#  This is a class template that is used for making threads stoppable. We
# will be using it to run led tasks on screen while we do other things
# and then stop them when we request it
#-------------------------------------------------------------------------
class StoppableThread(threading.Thread):
	def __init__(self,  *args, **kwargs):
		super(StoppableThread, self).__init__(*args, **kwargs)
		self._stop_event = threading.Event()

	def stop(self):
		logging.debug('Stopping thread for {}'.format(type(self).__name__))
		self._stop_event.set()

	def stopped(self):
		return self._stop_event.is_set()

#-------------------------------------------------------------------------
# LED Animations: 
#   Animations are in the form of classes from which objects can be made
# wherever needed. This allows them to inherit the stoppable thread class
# that is needed to run these animations asynchronously
#-------------------------------------------------------------------------
# A simple test animation for when we are getting started
class TestAnimation(StoppableThread):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

	def run(self):
		logging.debug('starting test animation')
		# RGB example w/graphics prims.
		# Note, only "RGB" mode is supported currently.
		image = Image.new("RGB", (32, 32))  # Can be larger than matrix if wanted!!
		draw = ImageDraw.Draw(image)  # Declare Draw instance before prims
		# Draw some shapes into image (no immediate effect on matrix)...
		draw.rectangle((0, 0, 31, 31), fill=(0, 0, 0), outline=(0, 0, 255))
		draw.line((0, 0, 31, 31), fill=(255, 0, 0))
		draw.line((0, 31, 31, 0), fill=(0, 255, 0))

		# Then scroll image across matrix...
		for n in range(-32, 33):
			if self.stopped():
				break
			matrix.Clear()
			matrix.SetImage(image, n, n)
			time.sleep(0.05)

# This is a test function for scrolling text
class RotatingBlock(StoppableThread):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

	def run(self):
		logging.debug('starting rotating block')
		cent_x = matrix.width / 2
		cent_y = matrix.height / 2

		rotate_square = min(matrix.width, matrix.height) * 1.41
		min_rotate = cent_x - rotate_square / 2
		max_rotate = cent_x + rotate_square / 2

		display_square = min(matrix.width, matrix.height) * 0.7
		min_display = cent_x - display_square / 2
		max_display = cent_x + display_square / 2

		deg_to_rad = 2 * 3.14159265 / 360
		rotation = 0

		# Pre calculate colors
		col_table = []
		for x in range(int(min_rotate), int(max_rotate)):
			col_table.insert(x, scale_color(x, min_display, max_display))

		offset_canvas = matrix.CreateFrameCanvas()

		while True:
			if self.stopped():
				matrix.Clear()
				return
			rotation += 1
			rotation %= 360

			# calculate sin and cos once for each frame
			angle = rotation * deg_to_rad
			sin = math.sin(angle)
			cos = math.cos(angle)

			for x in range(int(min_rotate), int(max_rotate)):
				for y in range(int(min_rotate), int(max_rotate)):
					# Our rotate center is always offset by cent_x
					rot_x, rot_y = rotate(x - cent_x, y - cent_x, sin, cos)

					if x >= min_display and x < max_display and y >= min_display and y < max_display:
						x_col = col_table[x]
						y_col = col_table[y]
						offset_canvas.SetPixel(rot_x + cent_x, rot_y + cent_y, 255, 0, 255)
					else:
						offset_canvas.SetPixel(rot_x + cent_x, rot_y + cent_y, 0, 0, 0)

			offset_canvas = matrix.SwapOnVSync(offset_canvas)

# Clock application
class Clock(StoppableThread):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

	def run(self):
		logging.debug('starting clock')

		offscreen_canvas = matrix.CreateFrameCanvas()
		font = graphics.Font()
		font.LoadFont("./fonts/7x13.bdf")
		font_height = font.height
		font_width = font.CharacterWidth(ord('L'))
		textColor = graphics.Color(255, 255, 255)
		cent_x = matrix.width / 2
		cent_y = matrix.height / 2
		pos = {
			'x': cent_x - (5 * font_width / 2),
			'y': cent_y + (font_height / 2) - 2
		}

		while True:
			# Check to see if we have stopped
			if self.stopped():
				matrix.Clear()
				return

			offscreen_canvas.Clear()
			# Grab the latest time
			t = time.localtime()
			hours = t.tm_hour
			mins = t.tm_min
			secs = t.tm_sec

			# Create the min string
			if mins < 10:
				minStr = '0' + str(mins)
			else:
				minStr = str(mins)

			# Create the hour string
			if hours < 10:
				hourStr = '0' + str(hours)
			else:
				hourStr = str(hours)

			# Create the time string either with a lit up colon or not
			if secs % 2 == 1:
				# Even seconds, concatenate the strings with a colon in the middle
				timeStr = hourStr + ' ' + minStr
			else:
				# Odd seconds, concatenate the strings with a semicolon(blank) in the middle
				timeStr = hourStr + ':' + minStr
			
			# Write the actual drawing to the canvas and then display
			graphics.DrawText(offscreen_canvas, font, pos['x'], pos['y'], textColor, timeStr)
			time.sleep(0.05)	# Time buffer added so as to not overload the system
			offscreen_canvas = matrix.SwapOnVSync(offscreen_canvas)


