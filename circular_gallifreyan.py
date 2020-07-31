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

import re
from PIL import Image, ImageDraw
import math

preset={
#sample presets
	"sample": "coward any day",
	"radius": 128
}

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
	#special
	"c","q"
]

class character_draw():
	def __init__(self, r):
		self.r = r #radius
		self.x = 0 #current position
		self.y = 0 #surrent position
		self.n =self.r * 1.2 #next characters spacing
	def bstem(self):
		draw.line((self.x, self.y + self.n, self.x + self.n / 2 - (self.r / 2 * math.cos(math.radians(60))), self.y + self.n), fill=(0,0,0))
		draw.line((self.x + self.n / 2 + (self.r / 2 * math.cos(math.radians(60))), self.y + self.n, self.x + self.n, self.y + self.n), fill=(0,0,0))
		draw.arc((self.x + self.n / 2 - self.r / 2, self.y + self.n / 2 - (self.r / 2 * math.cos(math.radians(45))), self.x + self.n / 2 + self.r / 2, self.y + self.n / 2 - (self.r / 2 * math.cos(math.radians(45))) + self.r), 120, 62, fill=(0,0,0))
	def jstem(self):
		draw.line((self.x, self.y + self.n, self.x + self.n, self.y + self.n), fill=(0,0,0))
		draw.ellipse((self.x + self.n / 2 - self.r / 2, self.y + self.n / 2 - self.r / 2, self.x + self.n / 2 + self.r / 2, self.y + self.n / 2 + self.r / 2), outline=(0,0,0))
	def tstem(self):
		draw.line((self.x, self.y + self.n, self.x + self.n / 2 - (self.r / 2 * math.sin(math.radians(75))), self.y + self.n), fill=(0,0,0))
		draw.line((self.x + self.n / 2 + (self.r / 2 * math.sin(math.radians(75))), self.y + self.n, self.x + self.n, self.y + self.n), fill=(0,0,0))
		draw.arc((self.x + self.n / 2 - self.r / 2, self.y + self.n - (self.r * (1 - math.sin(math.radians(35)))), self.x + self.n / 2 + self.r / 2, self.y + self.n - (self.r * (1 - math.sin(math.radians(35)))) + self.r), 190, 350, fill=(0,0,0))
	def thstem(self):
		draw.line((self.x, self.y + self.n, self.x + self.n, self.y + self.n), fill=(0,0,0))
		draw.ellipse((self.x + self.n / 2 - self.r / 2, self.y + self.n - self.r / 2, self.x + self.n / 2 + self.r / 2, self.y + self.n + self.r / 2), outline=(0,0,0))
	def dot1(self):
		draw.ellipse((self.x + self.n / 2 - self.r / 10 / 2, self.y + self.n - self.r / 10 / 2 - self.r / 4, self.x + self.n / 2 - self.r / 10 / 2 + self.r / 10, self.y + self.n - self.r / 10 / 2 + self.r / 10 - self.r / 4), fill=(0,0,0))
	def dot2(self):
		draw.ellipse((self.x + self.n / 2 - self.r / 10 / 2 - self.r / 10, self.y + self.n - self.r / 10 / 2 - self.r / 4, self.x + self.n / 2 - self.r / 10 / 2 + self.r / 10 - self.r / 10, self.y + self.n - self.r / 10 / 2 + self.r / 10 - self.r / 4), fill=(0,0,0))
		draw.ellipse((self.x + self.n / 2 - self.r / 10 / 2 + self.r / 10, self.y + self.n - self.r / 10 / 2 - self.r / 4, self.x + self.n / 2 - self.r / 10 / 2 + self.r / 10 + self.r / 10, self.y + self.n - self.r / 10 / 2 + self.r / 10 - self.r / 4), fill=(0,0,0))
	def dot3(self):
		draw.ellipse((self.x + self.n / 2 - self.r / 10 / 2 - self.r / 5, self.y + self.n - self.r / 10 / 2 - self.r / 4, self.x + self.n / 2 - self.r / 10 / 2 + self.r / 10 - self.r / 5, self.y + self.n - self.r / 10 / 2 + self.r / 10 - self.r / 4), fill=(0,0,0))
		draw.ellipse((self.x + self.n / 2 - self.r / 10 / 2, self.y + self.n - self.r / 10 / 2 - self.r / 4, self.x + self.n / 2 - self.r / 10 / 2 + self.r / 10, self.y + self.n - self.r / 10 / 2 + self.r / 10 - self.r / 4), fill=(0,0,0))
		draw.ellipse((self.x + self.n / 2 - self.r / 10 / 2 + self.r / 5, self.y + self.n - self.r / 10 / 2 - self.r / 4, self.x + self.n / 2 - self.r / 10 / 2 + self.r / 10 + self.r / 5, self.y + self.n - self.r / 10 / 2 + self.r / 10 - self.r / 4), fill=(0,0,0))
	def line1(self):
		draw.line((self.x + self.n / 2, self.y + self.n /2 - self.r / 2, self.x + self.n / 2, self.y + self.n - (self.r * (1 - math.sin(math.radians(35))))), fill=(0,0,0))
	def line2(self):
		draw.line((self.x + self.n / 2 - self.r / 5, self.y + self.n /2 - self.r / 2, self.x + self.n / 2 - self.r / 10, self.y + self.n - (self.r * (1 - math.sin(math.radians(35))))), fill=(0,0,0))
		draw.line((self.x + self.n / 2 + self.r / 5, self.y + self.n /2 - self.r / 2, self.x + self.n / 2 + self.r / 10, self.y + self.n - (self.r * (1 - math.sin(math.radians(35))))), fill=(0,0,0))
	def line3(self):
		draw.line((self.x + self.n / 2 - self.r / 5, self.y + self.n /2 - self.r / 2, self.x + self.n / 2 - self.r / 10, self.y + self.n - (self.r * (1 - math.sin(math.radians(35))))), fill=(0,0,0))
		draw.line((self.x + self.n / 2, self.y + self.n /2 - self.r / 2, self.x + self.n / 2, self.y + self.n - (self.r * (1 - math.sin(math.radians(35))))), fill=(0,0,0))
		draw.line((self.x + self.n / 2 + self.r / 5, self.y + self.n /2 - self.r / 2, self.x + self.n / 2 + self.r / 10, self.y + self.n - (self.r * (1 - math.sin(math.radians(35))))), fill=(0,0,0))
	def a(self):
		draw.line((self.x, self.y + self.n, self.x + self.n, self.y + self.n), fill=(0,0,0))
		draw.ellipse((self.x + self.n / 2 - self.r / 8, self.y + self.n + self.r / 10, self.x + self.n / 2 + self.r / 8, self.y + self.n + self.r / 10 + self.r / 4), outline=(0,0,0))
	def e(self):
		draw.line((self.x, self.y + self.n, self.x + self.n, self.y + self.n), fill=(0,0,0))
		draw.ellipse((self.x + self.n / 2 - self.r / 8, self.y + self.n - self.r / 8, self.x + self.n / 2 + self.r / 8, self.y + self.n + self.r / 8), outline=(0,0,0))
	def i(self):
		draw.line((self.x, self.y + self.n, self.x + self.n, self.y + self.n), fill=(0,0,0))
		draw.ellipse((self.x + self.n / 2 - self.r / 8, self.y + self.n - self.r / 8, self.x + self.n / 2 + self.r / 8, self.y + self.n + self.r / 8), outline=(0,0,0))
		draw.line((self.x + self.n / 2, self.y + self.n - self.r / 8, self.x + self.n / 2, self.y + self.n - self.r / 8 - self.r / 4), fill=(0,0,0))
	def o(self):
		draw.line((self.x, self.y + self.n, self.x + self.n, self.y + self.n), fill=(0,0,0))
		draw.ellipse((self.x + self.n / 2 - self.r / 8, self.y + self.n - self.r / 10 - self.r / 4, self.x + self.n / 2 + self.r / 8, self.y + self.n - self.r / 10), outline=(0,0,0))
	def u(self):
		draw.line((self.x, self.y + self.n, self.x + self.n, self.y + self.n), fill=(0,0,0))
		draw.ellipse((self.x + self.n / 2 - self.r / 8, self.y + self.n - self.r / 8, self.x + self.n / 2 + self.r / 8, self.y + self.n + self.r / 8), outline=(0,0,0))
		draw.line((self.x + self.n / 2, self.y + self.n + self.r / 8, self.x + self.n / 2, self.y + self.n +  + self.r / 8 + self.r / 4), fill=(0,0,0))

	def nextchar(self):
		self.x += self.n
	def space(self):
		self.x += self.n
	def nextline(self):
		self.y += self.n * 1.5

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
	elif char == "qu":
		write.thstem()
		write.line1()
	elif char == "x":
		write.thstem()
		write.line2()
	elif char == "ng":
		write.thstem()
		write.line3()

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
				if one in ["e","i","y"] and pointer>0 and out[-1][-1] == "c":
					out[-1][-1] = "s"
				elif pointer>0 and out[-1][-1] == "c":
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

if __name__=="__main__":
	print("circular gallifreyan translator\nfor latin characters only and without digits and punctuation.\ngiving you hints on how to combine and draw the letters.\nbypass to sample value by just pressing enter.")
	text = "" #input("type single sentence: ")
	radius = "" #input("type circle radius (px): ")

	if text == "":
		text = preset["sample"]
	if radius =="":
		radius = preset['radius']

	print("favoured grouping of characters: ")
	for word in characters(text):
		print (word)

	write = character_draw(int(radius))

	img = Image.new("RGB", (int(write.n * len(text)), int(write.n * 1.5)), (255, 255, 255))
	draw = ImageDraw.Draw(img)


	for word in characters(text):
		print (word)
		for group in word:
			for letter in group:
				sign(letter)
				write.nextchar()
		write.space()

	del draw 
	try:
		img.save("cg.png")
		img.show() 
	except: print('nope')