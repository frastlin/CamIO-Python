"""
This is the class each polygon in objects.py uses.
"""
from pyaudiogame.ui.grid import Polygon
from pyaudiogame.mixer import Sound

cwd = 'playground/'

bumperhand_sound = Sound(cwd + 'label_sounds/bumperhand.ogg')

last_label = None

class CamIOPolygon(Polygon):
	def __init__(self, name, poly, height=8, bumperhand=False):
		self.poly = poly
		# to normalize the names so they all work
		name = self.convert_lower_camelcase(name)
		self.name = name
		self.grid = None
		self.bumperhand = bumperhand
		self.height = height

		# These try statements check to see if either the sound of the object and or the label exist in the sound folders. The label is the speech "Stepping sounds" and the sound is the sound of the object.
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
		"""This runs when the user is in the polygon. It runs in the check functions. This function plays the label only when the user has not left the polygon. There was a problem of repeated calls to the label, so perhaps there should be a timed interval after the user leaves the polygon before the label plays."""
		global last_label
		if self != last_label and self.label:
			self.label.play()
			last_label = self

	def _on_move(self, event):
		"""When the user moves out of the label, this resets the last_label to None so that it will play again when the user re-enters the label. Here is where a timer should go."""
		global last_label
		if not event.in_poly and last_label == self:
			last_label = None

	def play_bumperhand(self, s=None):
		if self.bumperhand:
			"""This is not used"""
			bumperhand_sound.play()

	def convert_lower_camelcase(self, text):
		"""Converts to lower camelcase to normalize file names from the names given in the poly file"""
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