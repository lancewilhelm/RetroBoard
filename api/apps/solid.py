from apps._appbase import *
import time

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