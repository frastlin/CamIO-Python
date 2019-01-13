from pyaudiogame.ui.grid import AdvancedGrid as _AdvancedGrid
from pyaudiogame.mixer import set_listener

class AdvancedGrid(_AdvancedGrid):

	def _check(self, x, y, z):
		for p in self.grid.objects:
			if z != None and p.__dict__.get('height') != None and z > p.height:
				return None
			on_move_event = self.grid.get_move_event(x, y, p)
			p.on_move(on_move_event)
			if on_move_event  .in_poly:
				return p.callback()

	def xyz_set_pos(self, x, y, z=None, play_hit_sounds=False, play_step_sounds=False):
		if not self._check(x, y, z):
			self.pos = (x, y)
			if play_step_sounds: self.step_sounds.play()
			self.on_step(self)
			if self.move_listener:
				set_listener(x, y, 90)
			return False
		else:
			if play_hit_sounds: self.hit_sounds.play()
			self.on_hit(self)
			return True
