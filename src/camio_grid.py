from pyaudiogame.ui.grid import AdvancedGrid as _AdvancedGrid
# The listener is to move what the user hears around the soundscape
from pyaudiogame.mixer import set_listener

class AdvancedGrid(_AdvancedGrid):

	def _check(self, x, y, z):
		"""Check runs whenever there is a possible change in position. It looks to see if one can move in that location or not. It is run for every object in the grid every time the user changes pos."""
		for p in self.grid.objects:
			# These are the only 2 lines related to the Z coordinate, so comment it out if Z is not desired
			if z != None and p.__dict__.get('height') != None and z > p.height:
				return None
			# The on_move_event contains information about if the user is in the poly, and if not, where the player is in relation to the poly.
			on_move_event = self.grid.get_move_event(x, y, p)
			# on_move happens whenever the player moves. It controlls sounds in this instance.
			p.on_move(on_move_event)
			if on_move_event.in_poly:
				return p.callback()

	def xyz_set_pos(self, x, y, z=None, play_hit_sounds=False, play_step_sounds=False):
		"""This is the function that is called whenever there is a change in the position of the player, either through the stylus or the keyboard."""
		# the poly objects return True if they are an obsticle that you can't pass. Only the walls return true currently. Otherwise, they play the label "Stepping Sounds" or whatnot when the callback is called and return False.
		if not self._check(x, y, z):
			self.pos = (x, y)
			# These are the sounds that play when the keyboard calls this function.
			if play_step_sounds: self.step_sounds.play()
			self.on_step(self)
			if self.move_listener:
				set_listener(x, y, 90)
			return False
		else:
			# This is the "uh" sound when you hit a wall.
			if play_hit_sounds: self.hit_sounds.play()
			self.on_hit(self)
			return True
