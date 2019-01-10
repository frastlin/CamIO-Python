from pyaudiogame.ui.grid import Polygon
from pyaudiogame.mixer import Sound

bumperhand_sound = Sound('label_sounds/bumperhand.ogg')

last_label = None

class CamIOPolygon(Polygon):
	def __init__(self, name, poly, bumperhand=False):
		Polygon.__init__(self, poly, callback=self.callback, on_move=self.on_move)
		self.name = name
		self.sound = Sound('playground_sounds/{0}.wav'.format(name), position=(1,1))
		self.label = Sound('label_sounds/{0}.ogg'.format(name))
		self.label.callback = self.play_bumperhand
		self.sound.play(loops=-1)
		self.bumperhand = False

	def callback(self):
		global last_label
		if self != last_label:
			self.label.play()
			last_label = self

	def on_move(self, event):
		global last_label
		if not event.in_poly and last_label == self:
			last_label = None

	def play_bumperhand(self, s=None):
		if self.bumperhand:
			bumperhand_sound.play()