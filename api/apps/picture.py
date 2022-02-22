from apps._appbase import *
from PIL import Image

class Picture(StoppableThread):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.name = 'picture'

	def run(self):
		self.image = Image.open('./images/lancesig.png').convert('RGB')
		# self.image.resize((settings.width, settings.height), Image.ANTIALIAS)
		draw_image(self.image)

		update_screen()