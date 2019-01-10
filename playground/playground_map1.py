import pyaudiogame
from pyaudiogame import speak as spk
from pyaudiogame.ui.grid import AdvancedGrid
from pyaudiogame.mixer import Sound, get_listener
my_app = pyaudiogame.App("Playground Test")

grid = AdvancedGrid(width=84, height=67, step_sounds=["grid_sounds/step2.ogg", "grid_sounds/step3.ogg"], hit_sounds=["grid_sounds/hit.ogg"])

sound1 = Sound("lable_sounds/bench.ogg", position=[10,10])

def callback2():
#	spk("Fire")
	pass

def on_move2(event):
	if event.in_poly:
		spk("in poly")

grid.add_polygon([(4,4), (4,7), (8,7), (8,4)], callback=callback2, on_move=on_move2, sound=sound1)
"""
steppingSounds = [(3,10), (3,12), (5,12), (5,10)]
eastGate = [(13,16), (13,19), (14,19), (14,16)]
climbingGeraffe = [(9,20), (9,23), (12,23), (23,20)]
kinderBells = [(5,19), (5,21), (7,21), (7,19)]
# tot zone
curvedPosts = [(3,23), (3,25), (5,25), (5,23)] #bumperhand
totZoneSlides = [(5,23), (5,26), (7,26), (7,23)]
totZoneClimbingLoops = [(7,24), (7,27), (9,27), (9,24)]
rockingHorse = [(11,24), (11,25), (13,25), (13,24)]
totZoneBench = [(10,26), (10,27), (12,27), (12,26)]
tottlerZoneInformationPannel = [(14,22), (14,24), (16,24), (16,22)]
# Swing Area
diskSwings = [(8,31), (8,32), (9,40), (12,40), (12,39), (9,31)]
swayFun = [(15,40), (11,42), (10,44), (13,47), (15,45), (17,47)]
bucketSwings = [(6,48), (6,50), (14,56), (15,56), (15,54)]
rolerTable = [(17,45), (15,50), (18,50), (20,45)]
"""
@my_app.add_handler
def on_input(event):
	grid.move(event)
	if event.key and event.state:
		 if event.key == "space":
			 spk(str(get_listener()))

sound1.play(loops=-1)
my_app.run()