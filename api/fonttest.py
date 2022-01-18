from curses import color_content
from bdflib import reader
from setup import matrix, settings
from rgbmatrix import graphics
import time
import numpy as np

with open('./fonts/tom-thumb.bdf', 'rb') as filehandle:
	font = reader.read_bdf(filehandle)

color_matrix = np.ndarray((matrix.width, matrix.height, 3), dtype=int)

# Creates a linear color gradient
def create_color_grad(cm, start_color, end_color):
	# Initially this is assuming moving from the far left of the grid to the right. Angles will be added later
	width, height, _ = cm.shape
	cm_copy = np.copy(cm)

	for i in range(width):
		new_color = ((end_color - start_color) * (i / width) + start_color).astype(int)
		cm_copy[i,:] = new_color

	return cm_copy

def draw_glyph(canvas, x, y, cm, font, glyph):
	for i, row in enumerate(glyph.iter_pixels()):
		for j, pixel, in enumerate(row):
			pixel_x = x + j
			pixel_y = y + i
			if pixel:
				canvas.SetPixel(pixel_x, pixel_y, cm[pixel_x, pixel_y, 0], cm[pixel_x, pixel_y, 1], cm[pixel_x, pixel_y, 2])

def draw_text(canvas, x, y, cm, font, text):
	char_x = x
	for char in text:
		glyph = font[ord(char)]
		char_y = y + (font.ptSize - glyph.bbH)
		draw_glyph(canvas, char_x, char_y, cm, font, glyph)
		char_x += glyph.advance

cent_x = int(matrix.width / 2)
cent_y = int(matrix.height / 2)

offscreen_canvas = matrix.CreateFrameCanvas()

offscreen_canvas.Clear()

color_matrix = create_color_grad(color_matrix, np.array([0, 0, 255]), np.array([255, 255, 0]))
draw_text(offscreen_canvas, 10, 14, color_matrix, font, 'Hello World!')
offscreen_canvas = matrix.SwapOnVSync(offscreen_canvas)

while True:
	time.sleep(0.05)