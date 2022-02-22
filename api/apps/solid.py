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
				clear_screen()
				return

			# Check for a settings change that needs fto be loaded
			if settings.update_settings_bool:
				self.loadSettings()
				
			for x in range(settings.width):
				for y in range(settings.height):
					set_pixel(x, y, cm[x, y, 0], cm[x, y, 1], cm[x, y, 2])

			update_screen()
			time.sleep(0.05)	# Time buffer added so as to not overload the system