from pyaudiogame.ui.grid import Polygon
from pyaudiogame.mixer import Sound

cwd = 'playground/'

bumperhand_sound = Sound(cwd + 'label_sounds/bumperhand.ogg')

last_label = None

class CamIOPolygon(Polygon):
	def __init__(self, name, poly, height=8, bumperhand=False):
		Polygon.__init__(self, poly, callback=self.callback, on_move=self.on_move)
			name = self.convert_lower_camelcase(name)
		self.name = name
		self.bumperhand = bumperhand
		self.height = height

		try:
			self.sound = Sound('{1}playground_sounds/{0}.ogg'.format(name, cwd), position=(1,1))
			self.sound.play(loops=-1)
		except:
			self.sound = None

		try:
			self.label = Sound('{1}label_sounds/{0}.ogg'.format(name, cwd))
			self.label.callback = self.play_bumperhand
		except:
			self.label = None

	def callback(self):
		global last_label
		if self != last_label and self.label:
			self.label.play()
			last_label = self

	def on_move(self, event):
		global last_label
		if not event.in_poly and last_label == self:
			last_label = None

	def play_bumperhand(self, s=None):
		if self.bumperhand:
			bumperhand_sound.play()

	def convert_lower_camelcase(self, text):
		"""Converts to lower camelcase"""
		li = text.split(" ")
		if len(li) > 1:
			t = []
			for word_index in range(len(li)):
				if word_index == 0:
					t.append(li[word_index][0].lower() + li[word_index][1:])
				else:
					t.append(li[word_index].title())
			text = " ".join(t)
		elif len(text) > 1 and text[0].isupper():
			text = text[0].lower() + text[1:]
		return text