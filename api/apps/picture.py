from apps._appbase import *
from PIL import Image

class Picture(StoppableThread):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.name = 'picture'

	def run(self):
		self.image = Image.open('./images/lancesig.png').convert('RGB')
		# self.image.resize((settings.width, settings.height), Image.ANTIALIAS)

		self.offscreen_canvas.SetImage(self.image, 0)

		update_screen(self.offscreen_canvas)