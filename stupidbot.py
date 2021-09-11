import random

class stupidbot():
	def __init__(self, name):
		self.default = {
			'en': ['{0}, i don\'t know how to answer that...', 'sorry {0}, i am not sure about that.'],
			'de': ['{0}, ich weiß nicht wie ich darauf antworten soll...', 'da bin ich mir leider nicht sicher {0}.']
		}
		self.generic = { # keyword list, answer list
			'en': [
				[['hello'],
					['hello {0}!', '{0} hi!', '{0} wassuuuppp?']],
				[['bored', 'boring'],
					['{0} you could tidy up your room...',
					'{0} have you finished your homework?',
					'you have what it takes to exercise coding {0}!']],
				[['stupid', 'dumb'],
					['{0} are you sure about that?',
					'that\'s not nice to say about anyone {0}!']],
				[['joke'],
					['Q. Are any Halloween monsters good at math? A. No — unless you Count Dracula!',
					'Q. Why is Peter Pan flying all the time? A. He Neverlands!',
					'Q: What is a skeleton\'s favorite musical instrument? A: A Trombone!',
					'Q: How do you stay warm in an empty room? A: Go stand in the corner — it\'s always 90 degrees.']],
				[['funny', 'haha'],
					['i try my very best.']],
				[['calculate', 'math', 'mental'],
					['{0} what is the result of {1}?', '{0} what does {1} eqal to?', '{0} what do you make of {1}?']]
			],
			'de': [
				[['hallo'],
					['hallo {0}!', '{0} hi!', '{0} was geht?']],
				[['langweilig', 'langeweile'],
					['{0} du könntest dein zimmer aufräumen...',
					'{0} hast du deine hausaufgaben schon fertig?',
					'du hast alles was du zum programmieren üben brauchst {0}!']],
				[['blöd', 'dumm'],
					['{0} bist du dir da sicher?',
					'das ist aber nicht nett {0}!']],
				[['witz'],
					['Treffen sich 2 Schnecken an der Straße. Will die eine herübergehen. Sagt die andere: "Vorsichtig in einer Stunde kommt der Bus."',
					'Ein Mann rennt völlig außer Atem zum Bootssteg, wirft seinen Koffer auf das drei Meter entfernte Boot, springt hinterher, zieht sich mit letzter Kraft über die Reling und schnauft erleichtert: "Geschafft!" Einer der Seeleute: "Gar nicht so schlecht, aber warum haben Sie eigentlich nicht gewartet, bis wir anlegen?"',
					'Paul zerscheppert in der Wohnung seines Onkels eine große Vase. Der erblasste Onkel stammelt: "Die Vase war aus dem 17. Jahrhundert!" Darauf Paul erleichtert: "Gott sei Dank, ich dachte schon, sie sei neu".',
					'Laufen zwei Zahnstocher den Berg hoch und werden plötzlich von einem Igel überholt. Sagt der eine zum anderen: "Ach – hätte ich gewusst, dass ein Bus fährt, wäre ich mit dem gefahren!"',
					'Fritzchen sitzt am See und angelt. Ein Spaziergänger fragt: "Und, beißen die Fische?" Fritzchen antwortet entnervt: "Nein, Sie können sie, ruhig streicheln."',
					'Junge: "Was ist ein Rotkehlchen?" Schwester: "Ach, irgend so ein verrückter Fisch!" Junge: "Hier steht aber: Hüpft von Ast zu Ast!" Schwester: "Da siehst du, wie verrückt der ist!"',
					'Fragt der Lehrer: "Wer von euch kann mir sechs Tiere nennen, die in Australien leben?" Meldet sich Fritzchen: "Ein Koala und fünf Kängurus.']],
				[['lustig', 'haha'],
					['ich versuche mein bestes!']],
				[['rechnen', 'mathe', 'kopfrechnen'],
					['{0} was ergibt {1}?', 'ich möchte von dir das ergebnis von {1} wissen, {0}?', '{0} errechne {1}!']]
			]
		}
		self.expects = None
		self.name = name

	def parse(self, message, language, user):
		message = message.lower()
		if '@'+self.name in message:
			message=message.split()
			answer = self.default[language][random.randint(0, len(self.default[language]) - 1)].format('@' + user)

			def calculation():
				operation = ['+', '-', '*', '/']
				a = ''
				while a == '' or not isinstance(self.expects, int) or self.expects < 0: # avoid floats and negative numbers
					a = str(random.randint(1, 100)) + operation[random.randint(0, len(operation)-1)] + str(random.randint(1, 10))
					self.expects = eval(a)
				return a

			if self.expects is not None and str(self.expects) in message:
				answer={'en': 'yeah, the answer is {0}!', 'de': 'ja, das ergebnis ist {0}!'}[language].format(self.expects)
				self.expects = None
			else:
				for keywords in self.generic[language]:
					if any(x in message for x in keywords[0]):
						if (any(y in ['calculate','math','rechnen','mathe', 'kopfrechnen'] for y in keywords[0])):
							answer = keywords[1][random.randint(0, len(keywords[1]) - 1)].format('@' + user, calculation())
						else:
							answer = keywords[1][random.randint(0, len(keywords[1]) - 1)].format('@' + user)
						break
			return answer
		return False