''' inspired by https://github.com/Toglefritz/Musical_Marlin
'''
import random

class MakeMusic():
	'''create a g-code file that makes music'''
	STEPS_PER_MM = 80 #steps/min
	A = [27.5, 55, 110, 220, 440, 880, 1760] #440hz for a4
	FREQDIFF = 1.059467
	NOTES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
	SEPARATOR = 10 # milliseconds
	note={}
	def __init__(self):
		# calculate notes relative to A
		realfrequency = 0
		for i, a in enumerate(self.A):
			for n in self.NOTES:
				if n == "A":
					# erase rounding error
					realfrequency = a
				else:
					realfrequency = a * pow(1 / self.FREQDIFF, self.NOTES.index("A") - self.NOTES.index(n))
				self.note[f"{n}{i}"] = int(round(realfrequency * 60 / self.STEPS_PER_MM, 0)) # https://github.com/Toglefritz/Musical_Marlin#note-frequency-to-feedrate

	def play(self, axis, tune):
		axis = axis.upper()
		gcode = '''G90 ; use absolute position
G28 ; home
G0 X50 Y50 Z5 F2000 ; start position with security offset
G91 ; use relative position
'''
		factor = 1
		travelled = 0
		for n in tune["notes"].split():
			# split by note to frequency and length
			tone = n.upper().split("-")
			feedfrequency, duration = self.note.get(tone[0]), float(tone[1])
			if not feedfrequency:
				pause= 60 / tune["bpm"] * duration * 1000
				gcode += f"G4 P{pause} ; pause for {duration}\n"
			else:
	
				if travelled > 10:
					factor = -1
				if travelled<0:
					factor = 1
				distance = factor * round( 1 / tune["bpm"] * duration * feedfrequency, 5)
				travelled += distance
				gcode += f"G0 {axis}{distance} F{feedfrequency} ; {n}\n"
			gcode += f"G4 P{self.SEPARATOR} ; pause for {self.SEPARATOR} milliseconds\n"

		gcode += '''M84; disable motors
M81; power off
'''	
		self.export(gcode)

	def export(self, gcode):
		with open("melodic.gcode", "w", encoding="utf8") as file:
			file.write(gcode)

preset={
	"allemeinentchen": {
		"bpm": 120,
		"notes": '''
			C4-1 D4-1 E4-1 F4-1
			G4-2 G4-2
			A4-1 A4-1 A4-1 A4-1 G4-4
			A4-1 A4-1 A4-1 A4-1
			G4-4
			F4-1 F4-1 F4-1 F4-1
			E4-2 E4-2
			D4-1 D4-1 D4-1 D4-1
			C4-4
		'''
	},
	"happybirthday": {
		"bpm": 120,
		"notes": '''
			G4-.5 G4-.5
			A4-1 G4-1 C5-1
			B4-2 G4-.5 G4-.5
			A4-1 G4-1 D5-1
			C5-2 G4-.5 G4-.5
			G5-1 E5-1 C5-.5 C5-.5
			B4-1 A4-1 F5-.5 F5-.5
			E5-1 C5-1 D5-1
			C5-3
		'''
	},
	"doctorwho": {
		"bpm": 160,
		"notes":'''
			e3-.75 e3-.25 e3-.25 pause-.75
			e3-.75 e3-.25 e3-.25 pause-.75
			e3-.75 e3-.25 e3-.25 pause-.75
			g3-.75 g3-.25 g3-.25 pause-.75

			e3-.75 e3-.25 e3-.25 pause-.75
			e3-.75 e3-.25 e3-.25 pause-.75
			e3-.75 e3-.25 e3-.25 pause-.75
			g3-.75 g3-.25 g3-.25 pause-.75

			e3-.25 e3-.25 e3-.25 e3-.5 pause-.75
			e3-.25 e3-.25 e3-.25 e3-.5 pause-.75
			e3-.25 e3-.25 e3-.25 e3-.5 pause-.75

			E3-1 c5-1 b4-1.5 c5-.5 b4-4
			d5-2 e3-8
			b4-2 g4-1 b3-1 d4-3 c4-1 b3-5

			c5-1 b4-6 g4-1 b4-1
			a4-1.5 g4-.25 f#4-.25 g4-4
			d5-1 e5-1.5 d5-.25 c5-.25 d5-1
			g4-1 e5-1.5 d5-.25 c5-.25 d5-1
			g4-1 b4-.25 a4-2.5 g4-.5 f#4-.5 g4-2
			
			E3-1 c5-1 b4-1.5 c5-.5 b4-4 
			d5-2 e3-8

			#e3-.75 e3-.25 e3-.25 pause-.75 
			#e3-.75 e3-.25 e3-.25 pause-.75 
			#e3-.75 e3-.25 e3-.25 pause-.75 
			#g3-.75 g3-.25 g3-.25 pause-.75

			#e3-.75 e3-.25 e3-.25 pause-.75 
			#e3-.75 e3-.25 e3-.25 pause-.75 
			#e3-.75 e3-.25 e3-.25 pause-.75 
			#g3-.75 g3-.25 g3-.25 pause-.75
		'''
	},
	"startrek": {
		"bpm": 120,
		"notes":'''
			a5-3 e5-3 g5-3 b4-3
			a4-1 d5-.5 g5-2
			f#5-.5 d5-.5 b4-.5 e5-.5 a5-4

			e4-1 d5-3 c#5-1 b4-.5 a4-.5 g#4-.5 g4-4 f4-.5
			e4-1 e5-3 d5-1 c#5-.5 b4-.5 a4-.5 g#4-4 g4-.5
			f#4-3 g#4-1 a4-1 b4-1 c#5-.5 d5-.5 c#5-.5 e5-3 g5-3
			f#5-1 e5-2 f#4-3 b4-2 a4-1 d5-1 g5-1 b5-1 d6-3
		'''
	}
}



song=MakeMusic()
song.play("X", random.choice(list(preset.values())))
#song.play("X", preset["doctorwho"])
