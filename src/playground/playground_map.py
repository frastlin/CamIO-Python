import pyaudiogame
from pyaudiogame import speak as spk
from pyaudiogame.ui.grid import AdvancedGrid
from pyaudiogame.mixer import Sound, get_listener
my_app = pyaudiogame.App("Playground Test")

grid = AdvancedGrid(step_sounds=["grid_sounds/step2.ogg", "grid_sounds/step3.ogg"], hit_sounds=["grid_sounds/hit.ogg"])

sound1 = Sound("playground_sounds/bench.ogg", position=[10,10])

def callback2():
#	spk("Fire")
	pass

def on_move2(event):
	if event.in_poly:
		spk("in poly")

grid.add_polygon([(4,4), (4,7), (8,7), (8,4)], callback=callback2, on_move=on_move2, sound=sound1)

@my_app.add_handler
def on_input(event):
	grid.move(event)
	if event.key and event.state:
		 if event.key == "space":
			 spk(str(get_listener()))

sound1.play(loops=-1)
my_app.run()