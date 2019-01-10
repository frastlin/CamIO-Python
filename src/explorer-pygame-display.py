#explorer-pygame-display.py
#(c) James Coughlan, Smith-Kettlewell Eye Research Institute
#This modifies explorer.py by displaying graphics using pygame rather than OpenCV, and using pygame to capture key presses.
#Motivation: pygame.mixer.Channel doesn't work properly without using the pygame.display

#First calculate ground plane:
#either put marker on the table and press the 0 key,
#or else put the stylus in two locations on the table (ideally far apart): press 1 then 2 for the two locations.
#Next press the a and b keys to set the anchor points.
#Then finish by pressing 3 to calculate the pose.
#Annotation function: Press 4 to print XYZ coordinates of current stylus location.
#Press Escape key to exit program.

import numpy as np
import cv2
import time
import sys
from utilities import load_object, save_object, dist2hotspots3D
from stylus import detectMarkers_clean, Stylus, Markers
from sounds import Sounds, AMBIENT_PERIOD
from camera import Camera, CAMERAS, decimations
from geometry import quantize_location
from graphics import plot_stylus_camera, plot_corners, plot_hotspots, update_display
from parameters import *
from UI import *
from smoothing import Smoothing
import pygame

###############
#pyaudiogame code

import pyaudiogame
from pyaudiogame import App, global_keymap, event_queue
from pyaudiogame import speak as spk
from pyaudiogame.ui.grid import AdvancedGrid
from playground.objects import object_list

my_app = App("CamIO")
pyaudiogame.speech.always_print = True

grid = AdvancedGrid(width=76, height=62, step_sounds=["playground/grid_sounds/step2.ogg", "playground/grid_sounds/step3.ogg"], hit_sounds=["playground/grid_sounds/hit.ogg"])
[grid.add_polygon(p) for p in object_list]

# add key commands to the keymap
global_keymap.add([
	{'key': '0', 'event': 'scan_ground_plane_marker'},
{'key':'1','event':'save_at_location_1'},
{'key':'2', 'event':'save_at_location_2'},
{'key':'a', 'event':'save_at_location_a'},
{'key':'b', 'event':'save_at_location_b'},
{'key':'4', 'event':'get_xyz_coordinates'},
{'key':'3', 'event':'save_pose'},
{'key': 'tab', 'event':'switch_grid'},
])

#############################################################
camera = CAMERAS[which_camera]
decimation = decimations[which_camera] #decimation factor for showing image

camera_object = Camera(camera)
marker_object = Markers()
stylus_object = Stylus(which_stylus, stylus_length, camera_object.mtx, camera_object.dist)
print('Stylus:', which_stylus)
smoothing_object = Smoothing()

wb, sheet, board_parameters, hotspots, labels, labels_secondary = load_object(object_path+object_fname)
sound_object = Sounds(object_path, labels, labels_secondary)

cap = cv2.VideoCapture(int_or_ext)	
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,camera_object.h) #set camera image height
cap.set(cv2.CAP_PROP_FRAME_WIDTH,camera_object.w) #set camera image width
cap.set(cv2.CAP_PROP_FOCUS,0) #set focus #5 often good for smaller objects and nearer camera
print('Image height, width:', camera_object.h, camera_object.w)

#global variables
KEYBOARD_GRID = False
LAST_POSE = [0,0,0]
cnt = 0
pose_known = False
stylus_info_at_location_1, stylus_info_at_location_2, stylus_info_at_location_a, stylus_info_at_location_b = None, None, None, None
pose, plane_pose, Tca, stylus_location_XYZ_anno = None, None, None, None
current_hotspot = 0
obs_smoothed_old = 0
corners = None
ids = None

my_app.windowwidth = int(camera_object.w/decimation)
my_app.windowheight = int(camera_object.h/decimation)

# operation functions

def quit():
	try:
		quit_video(cap)
	except:
		pass
	pygame.quit()
	#cv2.destroyAllWindows()
	sys.exit(0)

#############################################################

def play_ambient_sound():
	if stylus_object.visible:
		sound_object.play_ambient_visible()
	else:
		sound_object.play_ambient_invisible()

def in_main_loop():
	"""Runs every loop"""
	global cnt, pose_known, corners, ids, LAST_POSE
	cnt += 1
	ret, frameBGR = cap.read()
	gray = cv2.cvtColor(frameBGR, cv2.COLOR_BGR2GRAY)
	corners, ids = detectMarkers_clean(gray, marker_object.arucodict, marker_object.arucodetectparam)
	stylus_object.apply_image(corners, ids)
	frameBGR = plot_corners(frameBGR, corners, ids)
	if stylus_object.visible:
		frameBGR = plot_stylus_camera(frameBGR, stylus_object.tip_XYZ[0],stylus_object.tip_XYZ[1],stylus_object.tip_XYZ[2], camera_object.mtx, camera_object.dist)
		if pose_known:
			stylus_location_XYZ_anno = estimate_stylus_location_in_annotation_coors(stylus_object.tip_XYZ, Tca, sound_object)
	if pose_known:
		frameBGR = plot_hotspots(frameBGR, hotspots, current_hotspot, pose[0], pose[1], camera_object.mtx, camera_object.dist)
		obs = quantize_location(stylus_object.visible, stylus_location_XYZ_anno, hotspots)
		obs_smoothed = smoothing_object.add_observation(obs, timestamp)
		current_hotspot, obs_smoothed_old = take_action(obs_smoothed, obs_smoothed_old, sound_object)
	if stylus_object.visible and pose_known and LAST_POSE != stylus_location_XYZ_anno:
		LAST_POSE = stylus_location_XYZ_anno
		x, y, z = stylus_location_XYZ_anno
		grid.set_pos(x, y)
	update_display(my_app.displaySurface, frameBGR, decimation)

@my_app.add_handler
def on_input(event):
	global stylus_info_at_location_1, stylus_info_at_location_2, stylus_info_at_location_a, stylus_info_at_location_b, plane_pose, KEYBOARD_GRID
	e = event.keymap_event
	if e == 'scan_ground_plane_marker':
		plane_pose, Tca = scan_ground_plane_marker(corners, ids, camera_object, sound_object)

	if stylus_object.visible:
		if e == 'save_at_location_1':
			stylus_info_at_location_1 = save_stylus_info(stylus_object, sound_object)
		elif e == 'save_at_location_2':
			stylus_info_at_location_2 = save_stylus_info(stylus_object, sound_object)
			plane_pose, Tac = estimate_ground_plane_from_two_stylus_scans(stylus_info_at_location_1, stylus_info_at_location_2, sound_object)
		elif e == 'save_at_location_a':
			stylus_info_at_location_a = save_stylus_info(stylus_object, sound_object)
		elif e == 'save_at_location_b':
			stylus_info_at_location_b = save_stylus_info(stylus_object, sound_object)
		if pose_known:
			if e == 'get_xyz_coordinates':
				spk('stylus XYZ location in annotation coordinates:', stylus_location_XYZ_anno)

	if e == 'save_pose':
		pose_knowna, pose, Tca = estimate_pose(stylus_info_at_location_a, stylus_info_at_location_b, plane_pose, np.array(hotspots[anchor_1_ind]),
											  np.array(hotspots[anchor_2_ind]), sound_object)
	elif e == 'switch_grid':
		KEYBOARD_GRID = not KEYBOARD_GRID
		spk("Keyboard grid on" if KEYBOARD_GRID else "Keyboard grid off")

	if KEYBOARD_GRID:
		grid.move(event)

# schedule the ambient sound to play
event_queue.schedule(function=play_ambient_sound, delay=AMBIENT_PERIOD, repeats=-1)

# add the above functions to the my_app object so they will run, and call run on the my_app object
my_app.in_main_loop = in_main_loop
my_app.quit = quit
my_app.run()