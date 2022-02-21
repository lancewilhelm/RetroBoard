from apps._appbase import *
import time
import math

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
