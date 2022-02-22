import time
import math
from setup import settings, matrix
import numpy as np
from apps._appbase import StoppableThread

current_frame = np.ndarray((settings.width, settings.height, 3), dtype=int)
previous_frame = current_frame.copy()

def clamp(n, minn, maxn):
	return max(min(maxn, n), minn)
	
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

def set_pixel(canvas, x, y, r, g, b):
	global current_frame
	if x >= settings.width or y >= settings.height:
		return

	if settings.debug:
		canvas[x, y, 0] = r
		canvas[x, y, 1] = g
		canvas[x, y, 2] = b
	else:
	# 	canvas.SetPixel(x, y, r, g, b)
		current_frame[x, y, 0] = r
		current_frame[x, y, 1] = g
		current_frame[x, y, 2] = b
	return

def clear_screen(canvas):
	if settings.debug:
		temp_canvas = np.ndarray((settings.width, settings.height, 3), dtype=int)
		temp_canvas.fill(0)
		return temp_canvas
	else:
		matrix.Clear()
		return canvas

def update_screen(canvas, current_frame, previous_frame):
	if settings.debug:
		settings.web_canvas = canvas
		settings.update_canvas_bool = True
		return canvas
	else:
		diff = current_frame - previous_frame
		diff_set = set([(x[0],x[1]) for x in np.argwhere(diff)])
		for p in diff_set:
			matrix.SetPixel(p[0], p[1], current_frame[p[0], p[1], 0], current_frame[p[0], p[1], 1], current_frame[p[0], p[1], 2])

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

offscreen_canvas = matrix.CreateFrameCanvas()

cent_x = int(settings.width / 2)
cent_y = int(settings.height / 2)

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

		# Run the clock loop until stopped
		while True:
			# Check to see if we have stopped
			if self.stopped():
				self.offscreen_canvas = clear_screen(self.offscreen_canvas)
				return

			# Check for a settings change that needs fto be loaded
			if settings.update_settings_bool:
				self.loadSettings()

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

			# self.offscreen_canvas = clear_screen(self.offscreen_canvas)
			draw_text(self.offscreen_canvas, hour_x, self.position['y'] - 3, self.font, hour_str)
			draw_text(self.offscreen_canvas, min_x, self.position['y'] + 3, self.font, min_str)
			update_screen(self.offscreen_canvas, current_frame, previous_frame)
			previous_frame = current_frame.copy()
			current_frame = np.ndarray((settings.width, settings.height, 3), dtype=int)

			time.sleep(0.05)	# Time buffer added so as to not overload the system

o = TextClock()
o.start()