################################################################################
# simplified translation from latin characters to circular gallifreyan
# by error on line 1 (erroronline.one)
#
# gallifreyan is based on television series doctor who by bbc
# translation is based on loren shermans alphabet of circular gallifreyan
# http://shermansplanet.com/gallifreyan/guide.pdf
#
# conversion of phonetic c for english only
#
# this only gives impressions of character composing
# python version inspired by mightyfrong
# https://github.com/Mightyfrong/gallifreyan-translation-helper
################################################################################

print('''
                _         _
 ___  ___  ___ | |_  ___ | | ___  ___  ___
|_ -||  _|| . ||   || -_|| || . || -_||  _|
|___||___||_  ||_|_||___||_||  _||___||_|
          |___|             |_|

$ python circular_gallifreyan.py --help     for more information
bypass to sample value by just pressing enter

''')

import re
from PIL import Image, ImageDraw
import math
import sys

preset = {
#sample presets
	"sample": "coward, any day!",
	"radius": 128,
	"bg": (255, 255, 255),
	"fg": (0, 0, 0)
}

helptext = '''
translate latin characters and punctuation to shermans circular gallifreyan. no numbers currently.
the artistic implementation is up to you anyway!

use from the console with
$ python circular_gallifreyan.py [ -h | --help ]              this view
                                 [ -r | --radius ] INTEGER    character circles radius in pixel
                                 [ -s | --save ]              saves output to file
                                 [ -l | --literal ]           allows literal c
                                 [ -p | --plain ]             no grouping of vowels to consonants

everthing else typed will be translated. double quotes can not be called from console.
punctuation if string is quoted. without provided text you will be promped to enter something, quotes enabled.

default grouping of consonants and vowels has my personal flavour (no a with t-stem). grouping of consonants is not supported.

supported/allowed characters:
'''

signs=[
#valid phonemes
	#vowels
	"a", "e", "i", "o", "u",
	#b-stem
	"b", "ch", "d", "g", "h", "f",
	#j-stem
	"j", "ph", "k", "l", "n", "p", "m",
	#t-stem
	"t", "wh", "sh", "r", "v", "w", "s",
	#th-stem
	"th", "gh", "y", "z", "qu", "x", "ng",
	#punctuation
	".", "?", "!", '"', "'", "-", "," ,";" ,":",
	#literal
	"c","q"
]

class character_draw():
	def __init__(self, r):
		self.r = r #radius
		self.x = 0 #current x-position
		self.y = 0 #current y-position
		self.n = self.r * 1.2 #next characters spacing
		self.carc = [self.x + self.r * 1.2 / 2, self.x + self.r * 1.2] #current center of consonant, word circle alignment
		self.linewidth = math.ceil(self.r / 100)
		self.vowelreset()
	def vowelreset(self):
		self.veiu = [self.x + self.n / 2, self.n] #vowel center for grouping x, y
		self.vo = [self.x + self.n / 2, self.y + self.n - self.r / 6] #vowel center for grouping x, y
		self.va = [self.x + self.n / 2, self.y + self.n + self.r / 6] #vowel center for grouping x, y
		self.vr = self.r / 8 #vowel radius factor for grouping
	def nextchar(self):
		self.x += self.n
		self.carc[0] += self.n
		self.veiu[0] = self.va[0] = self.vo[0] = self.carc[0]
	def space(self):
		self.x += self.n
		self.carc[0] += self.n
		self.veiu[0] = self.va[0] = self.vo[0] = self.carc[0]

	def bstem(self):
		draw.line((self.x, self.carc[1], self.carc[0] + (self.r / 2 * math.cos(math.radians(115))), self.carc[1]), fill = preset['fg'], width = self.linewidth)
		draw.line((self.carc[0] + (self.r / 2 * math.cos(math.radians(65))), self.carc[1], self.x + self.n, self.carc[1]), fill = preset['fg'], width = self.linewidth)
		draw.arc((self.carc[0] - self.r / 2, self.carc[1] / 2 - (self.r / 2 * math.cos(math.radians(45))), self.carc[0] + self.r / 2, self.carc[1] / 2 - (self.r / 2 * math.cos(math.radians(45))) + self.r), 115, 65, fill = preset['fg'], width = self.linewidth)
		self.vo = [self.carc[0] + self.r / 2 * math.cos(math.radians(45)), self.carc[1] / 2 - (self.r / 2 * math.cos(math.radians(45))) + self.r / 2 * math.cos(math.radians(60))] #adjust center for vowel grouping
		self.veiu = [self.carc[0], self.carc[1] / 2 - (self.r / 2 * math.cos(math.radians(45))) + self.r / 2] #adjust center for vowel grouping
	def jstem(self):
		draw.line((self.x, self.carc[1], self.x + self.n, self.carc[1]), fill = preset['fg'], width = self.linewidth)
		draw.ellipse((self.carc[0] - self.r / 2, self.carc[1] / 2 - self.r / 2, self.carc[0] + self.r / 2, self.carc[1] / 2 + self.r / 2), outline = preset['fg'], width = self.linewidth)
		self.vo = [self.carc[0] + self.r / 2 * math.cos(math.radians(45)), self.carc[1] / 2 - self.r / 2 + self.r / 2 * math.cos(math.radians(60))] #adjust center for vowel grouping
		self.veiu = [self.carc[0], self.carc[1] / 2 - self.r / 2 + self.r / 2] #adjust center for vowel grouping
	def tstem(self):
		draw.line((self.x, self.carc[1], self.carc[0] + (self.r / 2 * math.cos(math.radians(180))), self.carc[1]), fill = preset['fg'], width = self.linewidth)
		draw.line((self.carc[0] + (self.r / 2 * math.cos(math.radians(0))), self.carc[1], self.x + self.n, self.carc[1]), fill = preset['fg'], width = self.linewidth)
		draw.arc((self.carc[0] - self.r / 2, self.carc[1] - self.r / 2, self.carc[0] + self.r / 2, self.carc[1] - self.r / 2 + self.r), 180, 360, fill = preset['fg'], width = self.linewidth)
		self.vo = [self.carc[0] + self.r / 2 * math.cos(math.radians(45)), self.carc[1] - self.r / 2 + self.r / 2 * math.cos(math.radians(60))] #adjust center for vowel grouping
		self.veiu = [self.carc[0], self.carc[1]] #adjust center for vowel grouping
	def thstem(self):
		draw.line((self.x, self.carc[1], self.x + self.n, self.carc[1]), fill = preset['fg'], width = self.linewidth)
		draw.ellipse((self.carc[0] - self.r / 2, self.carc[1] - self.r / 2, self.carc[0] + self.r / 2, self.carc[1] + self.r / 2), outline = preset['fg'], width = self.linewidth)
		self.vo = [self.carc[0] + self.r / 2 * math.cos(math.radians(45)), self.carc[1] - self.r / 2 + self.r / 2 * math.cos(math.radians(60))] #adjust center for vowel grouping
		self.veiu = [self.carc[0], self.carc[1]] #adjust center for vowel grouping
	def dot1(self):
		draw.ellipse((self.carc[0] - self.r / 10 / 2, self.carc[1] - self.r / 10 / 2 - self.r / 4, self.carc[0] - self.r / 10 / 2 + self.r / 10, self.carc[1] - self.r / 10 / 2 + self.r / 10 - self.r / 4), fill=preset['fg'])
	def dot2(self):
		draw.ellipse((self.carc[0] - self.r / 10 / 2 - self.r / 10, self.carc[1] - self.r / 10 / 2 - self.r / 4, self.carc[0] - self.r / 10 / 2 + self.r / 10 - self.r / 10, self.carc[1] - self.r / 10 / 2 + self.r / 10 - self.r / 4), fill=preset['fg'])
		draw.ellipse((self.carc[0] - self.r / 10 / 2 + self.r / 10, self.carc[1] - self.r / 10 / 2 - self.r / 4, self.carc[0] - self.r / 10 / 2 + self.r / 10 + self.r / 10, self.carc[1] - self.r / 10 / 2 + self.r / 10 - self.r / 4), fill=preset['fg'])
	def dot3(self):
		draw.ellipse((self.carc[0] - self.r / 10 / 2 - self.r / 5, self.carc[1] - self.r / 10 / 2 - self.r / 4, self.carc[0] - self.r / 10 / 2 + self.r / 10 - self.r / 5, self.carc[1] - self.r / 10 / 2 + self.r / 10 - self.r / 4), fill=preset['fg'])
		draw.ellipse((self.carc[0] - self.r / 10 / 2, self.carc[1] - self.r / 10 / 2 - self.r / 4, self.carc[0] - self.r / 10 / 2 + self.r / 10, self.carc[1] - self.r / 10 / 2 + self.r / 10 - self.r / 4), fill=preset['fg'])
		draw.ellipse((self.carc[0] - self.r / 10 / 2 + self.r / 5, self.carc[1] - self.r / 10 / 2 - self.r / 4, self.carc[0] - self.r / 10 / 2 + self.r / 10 + self.r / 5, self.carc[1] - self.r / 10 / 2 + self.r / 10 - self.r / 4), fill=preset['fg'])
	def dot4(self):
		draw.ellipse((self.carc[0] - self.r / 10 / 2 - self.r / 3.5, self.carc[1] - self.r / 10 / 2 - self.r / 4, self.carc[0] + self.r / 10 / 2 - self.r / 3.5, self.carc[1] - self.r / 10 / 2 + self.r / 10 - self.r / 4), fill=preset['fg'])
		draw.ellipse((self.carc[0] - self.r / 10 / 2 - self.r / 10, self.carc[1] - self.r / 10 / 2 - self.r / 4, self.carc[0] + self.r / 10 / 2 - self.r / 10, self.carc[1] - self.r / 10 / 2 + self.r / 10 - self.r / 4), fill=preset['fg'])
		draw.ellipse((self.carc[0] - self.r / 10 / 2 + self.r / 10, self.carc[1] - self.r / 10 / 2 - self.r / 4, self.carc[0] + self.r / 10 / 2 + self.r / 10, self.carc[1] - self.r / 10 / 2 + self.r / 10 - self.r / 4), fill=preset['fg'])
		draw.ellipse((self.carc[0] - self.r / 10 / 2 + self.r / 3.5, self.carc[1] - self.r / 10 / 2 - self.r / 4, self.carc[0] + self.r / 10 / 2 + self.r / 3.5, self.carc[1] - self.r / 10 / 2 + self.r / 10 - self.r / 4), fill=preset['fg'])
	def line1(self):
		draw.line((self.veiu[0] + (self.r / 2 * math.cos(math.radians(135))), self.veiu[1] - (self.r / 2 * math.sin(math.radians(135))), self.veiu[0] + (self.r / 2 * 1.3 * math.cos(math.radians(135))), self.veiu[1] - (self.r / 2 * 1.3 * math.sin(math.radians(135)))), fill = preset['fg'], width = self.linewidth)
	def line2(self):
		draw.line((self.veiu[0] + (self.r / 2 * math.cos(math.radians(130))), self.veiu[1] - (self.r / 2 * math.sin(math.radians(130))), self.veiu[0] + (self.r / 2 * 1.3 * math.cos(math.radians(130))), self.veiu[1] - (self.r / 2 * 1.3 * math.sin(math.radians(130)))), fill = preset['fg'], width = self.linewidth)
		draw.line((self.veiu[0] + (self.r / 2 * math.cos(math.radians(140))), self.veiu[1] - (self.r / 2 * math.sin(math.radians(140))), self.veiu[0] + (self.r / 2 * 1.3 * math.cos(math.radians(140))), self.veiu[1] - (self.r / 2 * 1.3 * math.sin(math.radians(140)))), fill = preset['fg'], width = self.linewidth)
	def line3(self):
		draw.line((self.veiu[0] + (self.r / 2 * math.cos(math.radians(125))), self.veiu[1] - (self.r / 2 * math.sin(math.radians(125))), self.veiu[0] + (self.r / 2 * 1.3 * math.cos(math.radians(125))), self.veiu[1] - (self.r / 2 * 1.3 * math.sin(math.radians(125)))), fill = preset['fg'], width = self.linewidth)
		draw.line((self.veiu[0] + (self.r / 2 * math.cos(math.radians(135))), self.veiu[1] - (self.r / 2 * math.sin(math.radians(135))), self.veiu[0] + (self.r / 2 * 1.3 * math.cos(math.radians(135))), self.veiu[1] - (self.r / 2 * 1.3 * math.sin(math.radians(135)))), fill = preset['fg'], width = self.linewidth)
		draw.line((self.veiu[0] + (self.r / 2 * math.cos(math.radians(145))), self.veiu[1] - (self.r / 2 * math.sin(math.radians(145))), self.veiu[0] + (self.r / 2 * 1.3 * math.cos(math.radians(145))), self.veiu[1] - (self.r / 2 * 1.3 * math.sin(math.radians(145)))), fill = preset['fg'], width = self.linewidth)
	def a(self):
		draw.ellipse((self.va[0] - self.vr, self.va[1] - self.vr + self.vr / 2, self.va[0] + self.vr, self.va[1] + self.vr +  self.vr / 2), outline = preset['fg'], width = self.linewidth)
		self.vr *= 1.3 #enlarge for next grouped vowel
		self.va[1] -= (self.vr - self.vr / 1.3) / 2 #adjusting center
	def e(self):
		draw.ellipse((self.veiu[0] - self.vr, self.veiu[1] - self.vr, self.veiu[0] + self.vr, self.veiu[1] + self.vr), outline = preset['fg'], width = self.linewidth)
		self.vr *= 1.3 #enlarge for next grouped vowel
	def i(self):
		draw.ellipse((self.veiu[0] - self.vr, self.veiu[1] - self.vr, self.veiu[0] + self.vr, self.veiu[1] + self.vr), outline = preset['fg'], width = self.linewidth)
		draw.line((self.veiu[0], self.veiu[1] - self.vr, self.veiu[0], self.veiu[1] - self.vr - self.vr), fill = preset['fg'], width = self.linewidth)
		self.vr *= 1.3 #enlarge for next grouped vowel
	def o(self):
		draw.ellipse((self.vo[0] - self.vr, self.vo[1] - self.vr - self.vr / 2 , self.vo[0] + self.vr, self.vo[1] + self.vr - self.vr / 2), outline = preset['fg'], width = self.linewidth)
		self.vr *= 1.3 #enlarge for next grouped vowel
		self.vo[1] += (self.vr - self.vr / 1.3) / 2 #adjusting center
	def u(self):
		draw.ellipse((self.veiu[0] - self.vr, self.veiu[1] - self.vr, self.veiu[0] + self.vr, self.veiu[1] + self.vr), outline = preset['fg'], width = self.linewidth)
		draw.line((self.veiu[0], self.veiu[1] + self.vr, self.veiu[0], self.veiu[1] + self.vr + self.vr), fill = preset['fg'], width = self.linewidth)
		self.vr *= 1.3 #enlarge for next grouped vowel
	def dot(self):
		draw.line((self.x, self.carc[1] * 1.3, self.x + self.n, self.carc[1] * 1.3), fill = preset['fg'], width = self.linewidth)
		draw.ellipse((self.carc[0] - self.r / 8, self.carc[1] * 1.3 - self.r / 8, self.carc[0] + self.r / 8, self.carc[1] * 1.3 + self.r / 8), outline = preset['fg'], width = self.linewidth)
	def question(self):
		draw.line((self.x, self.carc[1] * 1.3, self.x + self.n, self.carc[1] * 1.3), fill = preset['fg'], width = self.linewidth)
		draw.ellipse((self.carc[0] - self.r / 10 / 2 - self.r / 10, self.carc[1] * 1.15, self.carc[0] - self.r / 10 / 2 + self.r / 10 - self.r / 10, self.carc[1] * 1.15 + self.r / 10), fill=preset['fg'])
		draw.ellipse((self.carc[0] - self.r / 10 / 2 + self.r / 10, self.carc[1] * 1.15, self.carc[0] - self.r / 10 / 2 + self.r / 10 + self.r / 10, self.carc[1] * 1.15 + self.r / 10), fill=preset['fg'])
	def exclamation(self):
		draw.line((self.x, self.carc[1] * 1.3, self.x + self.n, self.carc[1] * 1.3), fill = preset['fg'], width = self.linewidth)
		draw.ellipse((self.carc[0] - self.r / 10 / 2 - self.r / 5, self.carc[1] * 1.15, self.carc[0] - self.r / 10 / 2 + self.r / 10 - self.r / 5, self.carc[1] * 1.15 + self.r / 10), fill=preset['fg'])
		draw.ellipse((self.carc[0] - self.r / 10 / 2, self.carc[1] * 1.15, self.carc[0] - self.r / 10 / 2 + self.r / 10, self.carc[1] * 1.15 + self.r / 10), fill=preset['fg'])
		draw.ellipse((self.carc[0] - self.r / 10 / 2 + self.r / 5, self.carc[1] * 1.15, self.carc[0] - self.r / 10 / 2 + self.r / 10 + self.r / 5, self.carc[1] * 1.15 + self.r / 10), fill=preset['fg'])
	def doublequote(self):
		draw.line((self.x, self.carc[1] * 1.3, self.x + self.n, self.carc[1] * 1.3), fill = preset['fg'], width = self.linewidth)
		draw.line((self.carc[0], self.carc[1] * 1.3, self.carc[0], self.carc[1] ), fill = preset['fg'], width = self.linewidth)
	def singlequote(self):
		draw.line((self.x, self.carc[1] * 1.3, self.x + self.n, self.carc[1] * 1.3), fill = preset['fg'], width = self.linewidth)
		draw.line((self.carc[0] - self.r / 10, self.carc[1] *1.3, self.carc[0] - self.r / 10, self.carc[1]), fill = preset['fg'], width = self.linewidth)
		draw.line((self.carc[0] + self.r / 10, self.carc[1] *1.3, self.carc[0] + self.r / 10, self.carc[1] ), fill = preset['fg'], width = self.linewidth)
	def dash(self):
		draw.line((self.x, self.carc[1] * 1.3, self.x + self.n, self.carc[1] * 1.3), fill = preset['fg'], width = self.linewidth)
		draw.line((self.carc[0] - self.r / 5, self.carc[1] *1.3, self.carc[0] - self.r / 5, self.carc[1]), fill = preset['fg'], width = self.linewidth)
		draw.line((self.carc[0], self.carc[1] * 1.3, self.carc[0], self.carc[1]), fill = preset['fg'], width = self.linewidth)
		draw.line((self.carc[0] + self.r / 5, self.carc[1] *1.3, self.carc[0] + self.r / 5, self.carc[1]), fill = preset['fg'], width = self.linewidth)
	def comma(self):
		draw.line((self.x, self.carc[1] * 1.3, self.x + self.n, self.carc[1] * 1.3), fill = preset['fg'], width = self.linewidth)
		draw.ellipse((self.carc[0] - self.r / 8, self.carc[1] * 1.3 - self.r / 8, self.carc[0] + self.r / 8, self.carc[1] * 1.3 + self.r / 8), fill=preset['fg'])
	def semicolon(self):
		draw.line((self.x, self.carc[1] * 1.3, self.x + self.n, self.carc[1] * 1.3), fill = preset['fg'], width = self.linewidth)
		draw.ellipse((self.carc[0] - self.r / 10 / 2, self.carc[1] * 1.15, self.carc[0] - self.r / 10 / 2 + self.r / 10, self.carc[1] * 1.15 + self.r / 10), fill=preset['fg'])
	def colon(self):
		draw.line((self.x, self.carc[1] * 1.3, self.x + self.n, self.carc[1] * 1.3), fill = preset['fg'], width = self.linewidth)
		draw.ellipse((self.carc[0] - self.r / 6, self.carc[1] * 1.3 - self.r / 6, self.carc[0] + self.r / 6, self.carc[1] * 1.3 + self.r / 6), outline = preset['fg'], width = self.linewidth)
		draw.ellipse((self.carc[0] - self.r / 8, self.carc[1] * 1.3 - self.r / 8, self.carc[0] + self.r / 8, self.carc[1] * 1.3 + self.r / 8), outline = preset['fg'], width = self.linewidth)
	def wordline(self):
		draw.line((self.x, self.carc[1], self.x + self.n, self.carc[1]), fill = preset['fg'], width = self.linewidth)

def sign(char):
#circular gallifreyan signs
	#vowels
	if char == "a":
		write.a()
	elif char == "e":
		write.e()
	elif char == "i":
		write.i()
	elif char == "o":
		write.o()
	elif char == "u":
		write.u()
	#b-stem
	elif char == "b":
		write.bstem()
	elif char == "ch":
		write.bstem()
		write.dot2()
	elif char == "d":
		write.bstem()
		write.dot3()
	elif char == "g":
		write.bstem()
		write.line1()
	elif char == "h":
		write.bstem()
		write.line2()
	elif char == "f":
		write.bstem()
		write.line3()
	#j-stem
	elif char == "j":
		write.jstem()
	elif char == "ph":
		write.jstem()
		write.dot1()
	elif char == "k":
		write.jstem()
		write.dot2()
	elif char == "l":
		write.jstem()
		write.dot3()
	elif char == "c":
		write.jstem()
		write.dot4()
	elif char == "n":
		write.jstem()
		write.line1()
	elif char == "p":
		write.jstem()
		write.line2()
	elif char == "m":
		write.jstem()
		write.line3()
	#t-stem
	elif char == "t":
		write.tstem()
	elif char == "wh":
		write.tstem()
		write.dot1()
	elif char == "sh":
		write.tstem()
		write.dot2()
	elif char == "r":
		write.tstem()
		write.dot3()
	elif char == "v":
		write.tstem()
		write.line1()
	elif char == "w":
		write.tstem()
		write.line2()
	elif char == "s":
		write.tstem()
		write.line3()
	#th-stem
	elif char == "th":
		write.thstem()
	elif char == "gh":
		write.thstem()
		write.dot1()
	elif char == "y":
		write.thstem()
		write.dot2()
	elif char == "z":
		write.thstem()
		write.dot3()
	elif char == "q":
		write.thstem()
		write.dot4()
	elif char == "qu":
		write.thstem()
		write.line1()
	elif char == "x":
		write.thstem()
		write.line2()
	elif char == "ng":
		write.thstem()
		write.line3()
	#punctuation
	elif char == ".":
		write.dot()
	elif char == "?":
		write.question()
	elif char == "!":
		write.exclamation()
	elif char == '"':
		write.doublequote()
	elif char == "'":
		write.singlequote()
	elif char == "-":
		write.dash()
	elif char == ",":
		write.comma()
	elif char == ";":
		write.semicolon()
	elif char == ":":
		write.colon()

	else:
		return False

def characters(sentence):
	# set up array of gallifreyan character groups
	# phonetical correction of c and q according to best practice
	words = sentence.split()
	out = []
	for word in words:
		out.append([])
		pointer = 0
		while pointer < len(word):
			two = word[pointer:pointer+2]
			one = word[pointer:pointer+1]
			if two in signs:
				# phonetic correction of c at the end
				if pointer == len(word)-1 and two == "c":
					two = "k"
				out[-1].append(two)
				pointer += 2
			elif one in signs:
				# phonetic correction of c within words
				if not literal and one in ["e","i","y"] and pointer>0 and out[-1][-1] == "c":
					out[-1][-1] = "s"
				elif not literal and pointer>0 and out[-1][-1] == "c":
					out[-1][-1] = "k"
				out[-1].append(one)
				pointer += 1
			else:
				raise ValueError('character {0} not processable, translation aborted.'.format(one or two))
		out[-1] = group(out[-1])
	return out

def group(word):
	# group vowels and multiple consonants if suitable 
	place = []
	for i in range(len(word)):
		if ((i>0 and not (word[i] == "a" and word[i-1] in ["t","wh","sh","r","v","w","s"]) and #no "a" grouped to these consonants simply because i do not like that personally
			not (word[i] in ["a","e","i","o","u"] and word[i-1] in ["a","e","i","o","u"] and  word[i] != word[i-1]) and #no grouped different vowels
			(word[i] in ["a","e","i","o","u"] or word[i] == word[i-1]))):
			place[-1].append(word[i])
		else:
			place.append([word[i]])
	return place

if __name__ == "__main__":
	radius = False
	save = False
	literal = False
	plain = False

	# argument handler
	# omit first argument (scriptname)
	sys.argv.pop(0)
	# find and assign option arguments, strip arguments, remainder should be string
	options = {
		'h': '--help|-h',
		'r': '((?:--radius|-r)[:\\s]+)(\\d+)',
		's': '--save|-s',
		'l': '--literal|-l',
		'p': '--plain|-p'
		}
	params = ' '.join(sys.argv) + ' '
	for opt in options:
		arg = re.findall(options[opt], params, re.IGNORECASE)
		if opt == 'h' and arg:
			print(helptext, signs)
			exit()
		elif opt == 'r' and bool(arg):
			radius = int(arg[0][1])
			params = params.replace(''.join(arg[0]), '')
		elif opt == 's' and bool(arg):
			save = True
			params = params.replace(''.join(arg[0]), '')
		elif opt == 'l' and bool(arg):
			literal = True
			params = params.replace(''.join(arg[0]), '')
		elif opt == 'p' and bool(arg):
			plain = True
			params = params.replace(''.join(arg[0]), '')

	string = params.strip() if len(params.strip()) else False
	if not string:
		string = input("type single sentence: ")
	if not radius:
		radius = input("type circle radius (px): ")
	if string == "":
		string = preset["sample"]
	if radius =="":
		radius = preset['radius']

	print("possible grouping of characters: ")
	for word in characters(string):
		print (word)
	if "c" in string or "q" in string and not literal:
		print("c has been replaced. if they have to be used literal in names exchange them with a j-stem (c) or th-stem (q) with four dots. add flag --literal from command line to show the difference")

	write = character_draw(int(radius))
	sentence = characters(string)
	if plain:
		imgwidth = len(string)
	else:
		imgwidth = len(sentence) - 1
		for word in sentence:
			for group in word:
				imgwidth += 1

	img = Image.new("RGB", (int(write.n * imgwidth), int(write.n * 1.5)), preset['bg'])
	draw = ImageDraw.Draw(img)

	for word in sentence:
		for index, group in enumerate(word):
			for letter in group:
				sign(letter)
				if letter in ["'", '"', '-'] and index <= len(word):
					write.wordline()
				if plain:
					if letter in ["a", "e", "i", "o", "u"]:
						write.wordline()
					write.nextchar()
					write.vowelreset()
				elif letter == group[0] and letter in ["a", "e", "i", "o", "u"]:
					write.wordline()

			if not plain:
				write.nextchar()
			write.vowelreset()
		write.space()
	del draw 

	try:
		if save:
			img.save("cg.png")
			print("cg.png has been saved in scripts folder.")
		img.show() 
	except: print('error processing image')