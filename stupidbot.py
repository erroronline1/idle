import random
import re

class stupidbot():
	def __init__(self, name):
		self.expects = None
		self.name = name
		self.default = {
			'en': [
				'{0}, i don\'t know how to answer that...', 
				'sorry {0}, i am not sure about that.'],
			'de': [
				'{0}, ich weiß nicht wie ich darauf antworten soll...',
				'da bin ich mir leider nicht sicher {0}.']
		}
		self.generic = [ # first item: mulilanguage trigger pattern, second item: language dict with random responses
			['hello|hallo', {
				'en': [
					'hello {0}!',
					'{0} hi!',
					'{0} wassuuuppp?'],
				'de': [
					'hallo {0}!',
					'{0} hi!',
					'{0} was geht?']}],
			['bored|boring|langweilig|langeweile', {
				'en': [
					'{0} you could tidy up your room...',
					'{0} have you finished your homework?',
					'you have what it takes to exercise coding {0}!',
					'ask me about training mental arithmetic {0}!'],
				'de': [
					'{0} du könntest dein zimmer aufräumen...',
					'{0} hast du deine hausaufgaben schon fertig?',
					'du hast alles was du zum programmieren üben brauchst {0}!',
					'du, {0}, und ich könnten kopfrechnen üben!']}],
			['stupid|dumb|blöd|dumm', {
				'en': [
					'{0} are you sure about that?',
					'that\'s not nice to say about anyone {0}!'],
				'de': [
					'{0} bist du dir da sicher?',
					'das ist aber nicht nett {0}!']}],
			['joke|witz', {
				'en': [
					'Q. Are any Halloween monsters good at math? A. No — unless you Count Dracula!',
					'Q. Why is Peter Pan flying all the time? A. He Neverlands!',
					'Q: What is a skeleton\'s favorite musical instrument? A: A Trombone!',
					'Q: How do you stay warm in an empty room? A: Go stand in the corner — it\'s always 90 degrees.'],
				'de': [
					'Treffen sich 2 Schnecken an der Straße. Will die eine herübergehen. Sagt die andere: "Vorsichtig in einer Stunde kommt der Bus."',
					'Ein Mann rennt völlig außer Atem zum Bootssteg, wirft seinen Koffer auf das drei Meter entfernte Boot, springt hinterher, zieht sich mit letzter Kraft über die Reling und schnauft erleichtert: "Geschafft!" Einer der Seeleute: "Gar nicht so schlecht, aber warum haben Sie eigentlich nicht gewartet, bis wir anlegen?"',
					'Paul zerscheppert in der Wohnung seines Onkels eine große Vase. Der erblasste Onkel stammelt: "Die Vase war aus dem 17. Jahrhundert!" Darauf Paul erleichtert: "Gott sei Dank, ich dachte schon, sie sei neu".',
					'Laufen zwei Zahnstocher den Berg hoch und werden plötzlich von einem Igel überholt. Sagt der eine zum anderen: "Ach – hätte ich gewusst, dass ein Bus fährt, wäre ich mit dem gefahren!"',
					'Fritzchen sitzt am See und angelt. Ein Spaziergänger fragt: "Und, beißen die Fische?" Fritzchen antwortet entnervt: "Nein, Sie können sie, ruhig streicheln."',
					'Junge: "Was ist ein Rotkehlchen?" Schwester: "Ach, irgend so ein verrückter Fisch!" Junge: "Hier steht aber: Hüpft von Ast zu Ast!" Schwester: "Da siehst du, wie verrückt der ist!"',
					'Fragt der Lehrer: "Wer von euch kann mir sechs Tiere nennen, die in Australien leben?" Meldet sich Fritzchen: "Ein Koala und fünf Kängurus.']}],
			['funny|lustig|haha', {
				'en': [
					'i try my very best.'],
				'de': [
					'ich versuche mein bestes!']}],
			['skill|can you|fähigkeit|kannst du', {
				'en': [
					'i\'m glad you asked {0}! currently i can recommend activities in case you are bored, tell a few stupid jokes and help you train mental arithmetics. interact with me by mentioning me with @' + self.name + '.'],
				'de': [
					'schön dass du fragst {0}! derzeit kann ich dir was gegen langeweile empfehlen, ein paar dumme witze erzählen und dir beim kopfrechnen üben helfen. sprich mit mir indem du mich mit @' + self.name + 'erwähnst.']}]
		]

	def parse(self, message, language, user):
		# update with every call for being able to be changed during runtime of chat even after init of class
		# but usable on functions within this class
		self.language = language
		self.user = user
		if '@'+self.name in message:
			answer = False
			# list of skills according to method names.
			skills = ['mentalarithmetic']
			for skill in skills:
				answer = getattr(self, skill)(message)
			# if skills did non respond search generic responses
			if not answer:
				for keywords in self.generic:
					if re.search(keywords[0], message, re.IGNORECASE | re.DOTALL):
						answer = keywords[1][language][random.randint(0, len(keywords[1][language]) - 1)].format('@' + user)
						break
			# default answer if still empty
			if not answer:
				answer = self.default[language][random.randint(0, len(self.default[language]) - 1)].format('@' + user)
			return answer
		return False

	################################################################
	# skill methods
	# 
	# these have to accept message as parameter
	# and have to provide their own trigger patterns (e.g. concatenated in all supported languages)
	# occasionally update the help text and recommendations on being bored while you're hardcoding here anyway
	################################################################

	def mentalarithmetic(self, message):
		if (re.search('calculate|math|mental|rechnen', message, re.IGNORECASE | re.DOTALL) or
			self.expects is not None and self.expects['skill'] == 'mentalarithmetic'):
			def calculation():
				operation = ['+', '-', '*', '/']
				a = ''
				while a == '' or not isinstance(self.expects['value'], int) or self.expects['value'] < 0: # avoid floats and negative numbers
					a = str(random.randint(1, 100)) + operation[random.randint(0, len(operation)-1)] + str(random.randint(1, 10))
					self.expects['value'] = eval(a)
				return a
			if self.expects is None:
				answer={
					'en': [
						'{0} what is the result of {1}?',
						'{0} what does {1} eqal to?',
						'{0} what do you make of {1}?'],
					'de': [
						'{0} was ergibt {1}?',
						'ich möchte von dir das ergebnis von {1} wissen, {0}?',
						'{0} errechne {1}!']
				}
				self.expects = {'skill': 'mentalarithmetic', 'value': None}
				return answer[self.language][random.randint(0,len(answer[self.language])-1)].format('@'+self.user, calculation())
			elif re.search(str(self.expects['value']), message, re.IGNORECASE):
				answer = {
					'en': [
						'yeah, the answer is {0}!',
						'{0} is the correct answer!'],
					'de': [
						'ja, das ergebnis ist {0}!',
						'{0} ist die richtige antwort!']
					}
				value = self.expects['value']
				self.expects = None
				return answer[self.language][random.randint(0,len(answer[self.language])-1)].format(value)
		return False

		
