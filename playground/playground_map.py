import pyaudiogame
from pyaudiogame import speak as spk
from pyaudiogame.ui.grid import AdvancedGrid
my_app = pyaudiogame.App("Playground Test")

grid = AdvancedGrid(step_sounds=["grid_sounds/step2.ogg", "grid_sounds/step3.ogg"], hit_sounds=["grid_sounds/hit.ogg"])

def callback2():
	spk("Fire")



grid.add_polygon([(4,4), (5, 7), (8,7), (8,4)], callback=callback2)

@my_app.add_handler
def on_input(event):
	grid.move(event)

my_app.run()