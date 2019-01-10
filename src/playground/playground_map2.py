"""
add xyz coords to move the pos

"""
import pyaudiogame
from pyaudiogame import speak as spk
from pyaudiogame.ui.grid import AdvancedGrid
from pyaudiogame.mixer import Sound, get_listener
from poly_class import CamIOPolygon as P
my_app = pyaudiogame.App("Playground Test")

grid = AdvancedGrid(width=84, height=67, step_sounds=["grid_sounds/step2.ogg", "grid_sounds/step3.ogg"], hit_sounds=["grid_sounds/hit.ogg"])

polys = [
P('bench', [(4,4), (4,7), (8,7), (8,4)])
]

[grid.add_polygon(p) for p in polys]

"""
P('steppingSounds', [(3,10), (3,12), (5,12), (5,10)]),
P('eastGate', [(13,16), (13,19), (14,19), (14,16)]),
P('climbingGiraffe', [(9,20), (9,23), (12,23), (23,20)]),
P('kinderBells', [(5,19), (5,21), (7,21), (7,19)]),
# spin Zone
P('diskSpinner', [(23,21), (23,26), (28,26), (28,21)]),
P('groundCarousel', [(24,15), (24,20), (28,20), (28,15)]),
P('netSpinner',  [(18,27), (18,32), (23,32), (23,27)]),
P('nestSpinner',  [(19,21), (19,24), (22,24), (22,21)]),
P('zoneInfo',  [(16,25), (16,28), (18,28), (18,25)]),
P('cozyCoccoonSpinZone',  [(18,16), (18,18), (21,18), (21,16)], bumperhand=True),
P('benchSpinZone',  [(28,14), (28,16), (30,16), (30,14)]),
# tot zone
P('curvedPosts', [(3,23), (3,25), (5,25), (5,23)], bumperhand=True),

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
			 spk(get_listener())

my_app.run()