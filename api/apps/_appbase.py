#!/usr/bin/env python3
from setup import settings
import logging
import threading
import numpy as np

if not settings.debug:
	from setup import matrix

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

def set_pixel(x, y, r, g, b):
	if x >= settings.width or y >= settings.height:
		return

	settings.current_canvas[x, y, 0] = r
	settings.current_canvas[x, y, 1] = g
	settings.current_canvas[x, y, 2] = b
	return

def clear_screen():
	settings.current_canvas.fill(0)
	settings.prev_canvas.fill(0)
	settings.web_canvas.fill(0)
	settings.update_canvas_bool = True
	if not settings.debug:
		matrix.Clear()
	return
	
def update_screen():
	if settings.debug:
		settings.web_canvas = settings.current_canvas.copy()
		settings.update_canvas_bool = True
	else:
		diff = settings.current_canvas - settings.prev_canvas
		diff_set = set([(x[0],x[1]) for x in np.argwhere(diff)])
		for p in diff_set:
			matrix.SetPixel(p[0], p[1], settings.current_canvas[p[0], p[1], 0], settings.current_canvas[p[0], p[1], 1], settings.current_canvas[p[0], p[1], 2])
	
	settings.prev_canvas = settings.current_canvas.copy()
	settings.current_canvas.fill(0)
	return

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

def draw_glyph(x, y, glyph, color=None):
	cm = settings.color_matrix
	for i, row in enumerate(glyph.iter_pixels()):
		for j, pixel, in enumerate(row):
			pixel_x = x + j
			pixel_y = y + i
			if pixel and (pixel_x < settings.width and pixel_y < settings.height):
				if color == None:
					set_pixel(pixel_x, pixel_y, cm[pixel_x, pixel_y, 0], cm[pixel_x, pixel_y, 1], cm[pixel_x, pixel_y, 2])
				else:
					set_pixel(pixel_x, pixel_y, color[0], color[1], color[2])

def draw_text(x, y, font, text, color=None):
	char_x = x
	for char in text:
		glyph = font[ord(char)]
		char_y = y + (font.ptSize - glyph.bbH) - glyph.bbY
		char_x += glyph.bbX
		draw_glyph(char_x, char_y, glyph, color)
		char_x += (glyph.advance - glyph.bbX)

def draw_image(img):
	for x in range(settings.width):
		for y in range(settings.height):
			p = img.getpixel((x,y))
			set_pixel(x, y, p[0], p[1], p[2])
	return

cent_x = int(settings.width / 2)
cent_y = int(settings.height / 2)

#-------------------------------------------------------------------------
# LED Driving functions that are dependent on the objects defined above
#-------------------------------------------------------------------------
def start_led_app(app):
	settings.main['running_apps'] = []
	task = settings.app_dict[app]()
	task.start()
	settings.current_thread = task
	settings.main['running_apps'] = [app]
	settings.dump_settings()

def stop_current_led_app():
	settings.current_thread.stop()
	settings.current_thread = None
	settings.main['running_apps'] = []

#-------------------------------------------------------------------------
# Stoppable Thread Class:
#-------------------------------------------------------------------------
class StoppableThread(threading.Thread):
	''' Class used for making threads stoppable. Used to run led tasks on screen while other things run and then stop when requested'''
	def __init__(self,  *args, **kwargs):
		super(StoppableThread, self).__init__(*args, **kwargs)
		self._stop_event = threading.Event()
		self.loadSettings()
		settings.current_canvas.fill(0)
		settings.prev_canvas.fill(0)

	def stop(self):
		logging.debug('stopping thread for {}'.format(type(self).__name__))
		self._stop_event.set()
		clear_screen()

	def stopped(self):
		return self._stop_event.is_set()

	def loadSettings(self):
		logging.debug('loading settings for {}'.format(type(self).__name__))
		self.font = settings.load_font(settings.main['active_font'])
		self.font_width = self.font[ord(' ')].advance
		self.font_height = self.font.ptSize
		settings.update_settings_bool = False

		if settings.main['color_mode'] == 'static':
			set_static_color(settings.main['static_color'])
		elif settings.main['color_mode'] == 'gradient':
			set_color_grad(settings.main['gradient'][0], settings.main['gradient'][-1])