from apps._appbase import *
import time
import yfinance as yf
from datetime import datetime, timedelta

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
		display_symbol = settings.ticker['symbol']

		draw_text(2, 1, self.font, display_symbol, [255, 255, 255])

		if len(self.df) > 0:
			price = '${:.2f}'.format(self.c_vals[0])
			draw_text(2, 7, self.font, price, [255, 255, 255])
			price_diff = self.c_vals[0] - self.c_vals[-1]
			if price_diff > 0:
				self.graph_color = [0, 255, 0]
				price_diff = '+' + '{:.2f}'.format(price_diff)
			else:
				self.graph_color = [255, 0, 0]
				price_diff = '{:.2f}'.format(price_diff)

			price_diff_location = len(price) * 4 + 2
			draw_text(price_diff_location, 7, self.font, '{}'.format(price_diff), self.graph_color)

			c_y = [settings.height - int((self.c_vals[i] - min(self.c_vals)) / (max(self.c_vals) - min(self.c_vals)) * self.graph_height) - 1 for i in range(len(self.c_vals))]
			h_y = [settings.height - int((self.h_vals[i] - min(self.l_vals)) / (max(self.h_vals) - min(self.l_vals)) * self.graph_height) - 1 for i in range(len(self.h_vals))]
			l_y = [settings.height - int((self.l_vals[i] - min(self.l_vals)) / (max(self.h_vals) - min(self.l_vals)) * self.graph_height) - 1 for i in range(len(self.h_vals))]
			
			if settings.ticker['graph_type'] == 'diff':
				# Draw axis in gray
				for i, y in enumerate(c_y):
					if self.c_vals[i] < self.c_vals[-1]:
						for j in range(c_y[-1], y + 1):
							set_pixel(settings.width - (i + 1), j, 50, 0, 0)
						set_pixel(settings.width - (i + 1), y, 250, 0, 0)
						if i != (len(c_y)-1) and y > c_y[i + 1]:
							for j in range(max(c_y[i+1], c_y[-1]), y):
								set_pixel(settings.width - (i + 1), j, 250, 0, 0)
						if i != 0 and y > c_y[i - 1]:
							for j in range(max(c_y[i-1], c_y[-1]), y):
								set_pixel(settings.width - (i + 1), j, 250, 0, 0)
					else:
						for j in range(y, c_y[-1] + 1):
							set_pixel(settings.width - (i + 1), j, 0, 50, 0)
						set_pixel(settings.width - (i + 1), y, 0, 250, 0)
						if i != (len(c_y)-1) and y < c_y[i + 1]:
							for j in range(y, min(c_y[i+1], c_y[-1])):
								set_pixel(settings.width - (i + 1), j, 0, 250, 0)
						if i != 0 and y < c_y[i - 1]:
							for j in range(y, min(c_y[i-1], c_y[-1])):
								set_pixel(settings.width - (i + 1), j, 0, 250, 0)

			elif settings.ticker['graph_type'] == 'filled':
				for i, y in enumerate(c_y):
					for j in range(y, settings.height):
						set_pixel(settings.width - (i + 1), j, self.graph_color[0] * 0.2, self.graph_color[1] * 0.2, self.graph_color[2] * 0.2)
					set_pixel(settings.width - (i + 1), y, self.graph_color[0], self.graph_color[1], self.graph_color[2])
					if i != 0 and y < c_y[i-1]:
						for j in range(y, c_y[i-1]):
							set_pixel(settings.width - (i + 1), j, self.graph_color[0], self.graph_color[1], self.graph_color[2])
					elif i != len(c_y) and y > c_y[i-1]:
						for j in range(c_y[i-1], y):
							set_pixel(settings.width - (i), j, self.graph_color[0], self.graph_color[1], self.graph_color[2])
					
			elif settings.ticker['graph_type'] == 'bar':
				for i, c_val in enumerate(self.c_vals):
					if c_val - self.o_vals[i] > 0:
						if h_y[i] != l_y[i]:
							for j in range(h_y[i], l_y[i]):
								set_pixel(settings.width - (i + 1), j, 0, 255, 0)
						else:
							set_pixel(settings.width - (i + 1), h_y[i], 0, 255, 0)
					else:
						if h_y[i] != l_y[i]:
							for j in range(h_y[i], l_y[i]):
								set_pixel(settings.width - (i + 1), j, 255, 0, 0)
						else:
							set_pixel(settings.width - (i + 1), h_y[i], 255, 0, 0)
		else:
			draw_text(19, 20, self.font, 'NO DATA', [255, 255, 255])

		update_screen()

	def run(self):
		logging.debug('starting ticker')

		self.price_update_time = int(time.mktime((datetime.now() + timedelta(seconds = 15)).timetuple()))
		self.get_prices()
		self.draw_screen()

		# Run the ticker loop until stopped
		while True:
			# Check to see if we have stopped
			if self.stopped():
				clear_screen()
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