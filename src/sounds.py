#sounds.py
#(c) James Coughlan, Smith-Kettlewell Eye Research Institute

from gtts import gTTS #use to generate .mp3 files (saved in advance) for each possible utterance
import pygame #to play sounds
import os
from pyaudiogame.mixer import Sound

# Overview:
# Need to be able to halt TTS utterance in progress,
# and need to be able to play other sounds simultaneously without disturbing TTS playback.
# To accomplish this, play .mp3 as TTS sounds, and .wav as non-TTS sounds.
# Background:
# 1) While pygame.mixer.music can only play one mp3 file at a time,
# multiple pygame.mixer.Sound objects can be played simultaneously.
# 2) gTTS only generates .mp3 files, not .wav
# 3) James’s experience with pygame.mixer.Channel(0).play(pygame.mixer.Sound(...)) :
# Only some .wav formats work. One is Wave PCM signed 16 bit, 16000 Hz, stereo

AMBIENT_INVISIBLE = Sound('../res/sounds-common/beat-single.wav') #AMBIENT sound (single beat) indicates ground plane visible
AMBIENT_VISIBLE = Sound('../res/sounds-common/beat-double.wav') #AMBIENT2 sound indicates stylus visible
AMBIENT_PERIOD = 1.0 #period of ambient sound, in sec.
BLIP = '../res/sounds-common/pop.wav' #BLIP indicates we just arrived at hotspot (currently not used)

# sounds




class Sounds:
	def __init__(self, object_path, labels, labels_secondary):
		#generate sound files if they don't already exist
		self.object_path = object_path
		self.generate_gtts_labels(object_path, labels, labels_secondary, sound_folder='sounds')

	def generate_gtts_labels(self, object_path, labels, labels_secondary, sound_folder='sounds'):
		if not os.path.exists(self.object_path+sound_folder): #need to generate all TTS labels as .mp3 files:
			os.makedirs(object_path+sound_folder)
			print('Generating sounds, please wait...')
			for item in labels:
				s = labels[item]
				s2 = labels_secondary[item]
				if s2 != None: #len(s2)>0: #does this handle all possible forms of null content in an Excel cell?
					s += '. ' + s2 #concatenate primary and secondary labels
				tts = gTTS(text=s, lang='en')
				try:
					print('saving:',s)
					ret = tts.save(object_path+sound_folder+'/'+str(item)+'.mp3')
					print('ret:',ret)
				except: #sound file is already open
					print('exception')
					pass
			print('Done generating sounds.')

	def play_ambient_invisible(self):
		AMBIENT_INVISIBLE.play()

	def play_ambient_visible(self):
		AMBIENT_VISIBLE.play()

	def play_wav(self, fname):
		Sound(fname).play()

	def play_mp3(self, fname):
		pygame.mixer.music.load(fname)
		pygame.mixer.music.play()

	def play_hotspot(self, hotspot): #play specified hotspot (1, 2, 3, ...)
		#self.play_wav(BLIP) #uncomment to preface TTS announcement with BLIP
		self.play_mp3(self.object_path+'sounds/'+str(hotspot)+'.mp3')

	def halt_TTS(self):
		pygame.mixer.music.stop()

