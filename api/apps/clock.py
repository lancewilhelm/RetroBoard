from apps._appbase import *
import time

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

		# Run the clock loop until stopped
		while True:
			# Check to see if we have stopped
			if self.stopped():
				clear_screen()
				return

			# Check for a settings change that needs fto be loaded
			if settings.update_settings_bool:
				self.loadSettings()
			
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
			draw_text(self.position['x'], self.position['y'], self.font, time_str)
			update_screen()

			time.sleep(0.05)	# Time buffer added so as to not overload the system