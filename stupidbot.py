import random
import re
import requests

class xinarow: 
	def __init__(self, x, y):
		self.board=[[' ']*x for n in range(y)] 
	def draw(self, x, y, player):
		x,y=x-1,y-1 
		if self.board[y][x] == ' ': 
			self.board[y][x]=player 
			return True 
		else: 
			return False 
	def free(self): 
		f=[] 
		for i in range(len(self.board)):
			for j in range(len(self.board[i])):
				if self.board[i][j]==' ': 
					f.append([i,j])
		return f


class stupidbot():
	expects = None
	language = None
	user = None
	def __init__(self, name):
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
					'hello {0}! ask "@' + self.name + ' help" for info about me.',
					'hi {0}! ask "@' + self.name + ' help" for info about me.',
					'{0} wassuuuppp? ask "@' + self.name + ' help" for info about me.',],
				'de': [
					'hallo {0}! frag "@' + self.name + ' hilfe" für infos über mich.',
					'hi {0}! frag "@' + self.name + ' hilfe" für infos über mich.',
					'{0} was geht? frag "@' + self.name + ' hilfe" für infos über mich.']}],
			['bored|boring|langweilig|langeweile', {
				'en': [
					'{0} you could tidy up your room...',
					'{0} have you finished your homework?',
					'you have what it takes to exercise coding {0}!',
					'ask me about training mental arithmetic {0}!',
					'go outside if the weather is appropriate. ask me about that :)'],
				'de': [
					'{0} du könntest dein zimmer aufräumen...',
					'{0} hast du deine hausaufgaben schon fertig?',
					'du hast alles was du zum programmieren üben brauchst {0}!',
					'du, {0}, und ich könnten kopfrechnen üben!',
					'du könntest rausgehen, wenn es das wetter zulässt. frag mich danach :)']}],
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
					'Q: How do you stay warm in an empty room? A: Go stand in the corner — it\'s always 90 degrees.',
					'Q. Why did the bicycle fall over? A: It was two tired.',
					'Q: What did one wall say to the other wall? A:  I\'ll meet you at the corner!'],
				'de': [
					'Treffen sich 2 Schnecken an der Straße. Will die eine herübergehen. Sagt die andere: "Vorsichtig in einer Stunde kommt der Bus."',
					'Ein Mann rennt völlig außer Atem zum Bootssteg, wirft seinen Koffer auf das drei Meter entfernte Boot, springt hinterher, zieht sich mit letzter Kraft über die Reling und schnauft erleichtert: "Geschafft!" Einer der Seeleute: "Gar nicht so schlecht, aber warum haben Sie eigentlich nicht gewartet, bis wir anlegen?"',
					'Paul zerscheppert in der Wohnung seines Onkels eine große Vase. Der erblasste Onkel stammelt: "Die Vase war aus dem 17. Jahrhundert!" Darauf Paul erleichtert: "Gott sei Dank, ich dachte schon, sie sei neu".',
					'Laufen zwei Zahnstocher den Berg hoch und werden plötzlich von einem Igel überholt. Sagt der eine zum anderen: "Ach – hätte ich gewusst, dass ein Bus fährt, wäre ich mit dem gefahren!"',
					'Fritzchen sitzt am See und angelt. Ein Spaziergänger fragt: "Und, beißen die Fische?" Fritzchen antwortet entnervt: "Nein, Sie können sie, ruhig streicheln."',
					'Junge: "Was ist ein Rotkehlchen?" Schwester: "Ach, irgend so ein verrückter Fisch!" Junge: "Hier steht aber: Hüpft von Ast zu Ast!" Schwester: "Da siehst du, wie verrückt der ist!"',
					'Fragt der Lehrer: "Wer von euch kann mir sechs Tiere nennen, die in Australien leben?" Meldet sich Fritzchen: "Ein Koala und fünf Kängurus.']}],
			['funny|thank|good bot|lustig|danke|guter bot|haha', {
				'en': [
					'i try my very best.',
					'you\'re welcome {0}!'],
				'de': [
					'ich versuche mein bestes!',
					'immer gern {0}!']}],
			['skill|can you|help|fähigkeit|kannst du|hilfe', {
				'en': [
					'i\'m glad you asked {0}! currently i can recommend activities in case you are bored, tell a few stupid jokes, some stupid riddles and help you train mental arithmetics. i recently learned mastermind, rock-paper-scissors and tic-tac-toe. i am not good at the latter...'
					+ ' i can also tell you the weather, help with decisions and tell about things on wikipedia. interact with me by mentioning me with @' + self.name + '.'],
				'de': [
					'schön dass du fragst {0}! derzeit kann ich dir was gegen langeweile empfehlen, ein paar dumme witze erzählen, scherzfragen stellen und dir beim kopfrechnen üben helfen. kürzlich habe ich mastermind, schnick-schnack-schnuck und drei-gewinnt gelernt. im letzten bin ich nicht gut...'
					+ ' ich kann dir auch das wetter sagen, bei entscheidungen helfen  und bei wikipedia nachschauen was etwas ist. sprich mit mir indem du mich mit @' + self.name + ' erwähnst.']}]
		]

	def parse(self, message, language, user):
		# update with every call for being able to be changed during runtime of chat even after init of class
		# but usable on functions within this class
		self.language = language
		self.user = user
		if '@'+self.name in message:
			answer = False
			# list of skills according to method names.
			skills = ['mentalarithmetic', 'googleweather', 'wikipedia', 'conundrum', 'mastermind', 'tictactoe', 'rockpaperscissors', 'decide']
			for skill in skills:
				answer = getattr(self, skill)(message)
				if answer:
					break
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

	def sourcecode(self, link, timeout = 5):
		try:
			r = requests.get( link, headers =
				{"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0",
				"Referer": "https://ecosia.org"}, timeout = timeout )
			if r.status_code == 200:
				return r.text
		except:
			pass
		return False

	################################################################
	# skill methods
	# these have to accept message as parameter
	# and have to provide their own trigger patterns (e.g. concatenated in all supported languages)
	# occasionally update the help text and recommendations on being bored while you're hardcoding here anyway
	################################################################

	def mentalarithmetic(self, message):
		if (re.search('calculate|math|mental|rechnen', message, re.IGNORECASE | re.DOTALL) or
			self.expects is not None and self.expects['skill'] == 'mentalarithmetic'):
			def calculation():
				operation = [[100, '+', 100], [100, '-', 99], [100, '*', 20], [150, '/', 12]]
				a = ''
				while a == '' or not isinstance(self.expects['value'], int) or self.expects['value'] < 0: # avoid floats and negative numbers
					op = operation[random.randint(0, len(operation)-1)]
					a = str(random.randint(1, op[0])) + op[1] + str(random.randint(1, op[2]))
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
			if re.search(str(self.expects['value']), message, re.IGNORECASE):
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
			answer = {
				'en': [
					'{0} the answer is {1}!'],
				'de': [
					'{0} das ergebnis ist {1}!']
				}
			value = self.expects['value']
			self.expects = None
			return answer[self.language][random.randint(0,len(answer[self.language])-1)].format('@'+self.user, value)
		return False

	def googleweather(self, message):
		if (re.search('weather|rain|temperature|wetter|regen|regnet|warm|temperatur', message, re.IGNORECASE | re.DOTALL) or
			self.expects is not None and self.expects['skill'] == 'googleweather'):
			if self.expects is None:
				self.expects = {'skill': 'googleweather'}
				answer = {
					'en': [
						'{0} where should i check for the weather?'],
					'de': [
						'{0} für welchen ort soll ich das wetter nachfragen?']
					}
				return answer[self.language][0].format('@'+self.user)
			else:
				self.expects = None
				gcode = self.sourcecode('https://www.google.com/search?q=weather+' + message.replace('@'+self.name, '').replace(' ', '+'))
				if gcode:
					data = re.findall(r'class="BBwThe">(.+?)<.*?id="wob_tm".+?>(\d+).+?id="wob_pp".*?>(.+?)<.*?id="wob_dc">(.+?)<', gcode, re.IGNORECASE | re.DOTALL)
					if len(data):
						answer = {
							'en': [
								'the weather for {2} is reportedly {1} with {3}°c and rainfall probability of {0}.'],
							'de': [
								'das wetter für {2} wird als {1} gemeldet, bei {3}°c und einer niederschlagswahrscheinlichkeit von {0}.']
							}
						return answer[self.language][0].format(data[0][2], data[0][3], data[0][0], data[0][1]).lower()
				else:
					answer = {
						'en': [
							'sorry, i kindly asked but did not get a response too.'],
						'de': [
							'verzeihung, ich habe wirklich höflich gefragt aber auch keine antwort bekommen.']
						}
					return answer[self.language][random.randint(0,len(answer[self.language])-1)]
		return False

	def wikipedia(self, message):
		if re.search('what is|tell me about|was ist|sag mir was zu', message, re.IGNORECASE | re.DOTALL):
			topic = re.search(r'(?:what is|tell me about|was ist|sag mir was zu).+?(?:a|an|the|ein|eine|der|die|das)*([\w\s\(\)]{1,})', message, re.IGNORECASE | re.DOTALL)
			topic = topic[1].replace('@'+self.name, '').replace(' ', '+')
			wcode = self.sourcecode('https://' + self.language + '.wikipedia.org/w/index.php?search=' + topic)
			data = None
			if wcode:
				data = re.search(r'<p>(.*?)</p>.*?(?:<ul>|<p>)(.*?)(?:</p>|<ul>)', wcode, re.IGNORECASE | re.DOTALL)
				if data is not None:
					answer = {
						'en': [
							'wikipedia says: {0}\nis not necessarily correct and most probably incomplete.'],
						'de': [
							'wikipedia sagt: {0}\nist nicht notwendigerweise richtig und wahrscheinlich unvollständig.']
						}
					result = re.sub('<.*?>|&#.+?;', '', re.sub('<li.*?>', '* ', data[0]))
					return answer[self.language][0].format(result).lower()
			if not wcode or data is None:
				answer = {
					'en': [
						'sorry, i kindly asked but did not get a response too.'],
					'de': [
						'verzeihung, ich habe wirklich höflich gefragt aber auch keine antwort bekommen.']
					}
				return answer[self.language][random.randint(0,len(answer[self.language])-1)]
		return False

	def conundrum(self, message):
		riddles={
			'en':[
				['what is a skeleton\'s favorite musical instrument?', 'a trombone!', 'trombone'],
				['what has four wheels and flies?', 'a garbage truck', 'garbage.*truck'],
				['I make you frown and scratch your head, to find my solution will leave you mumbling. Many love me, many hate me and my nature\'s humbling. Fabled creatures sometimes use me, of confusion some accuse me. What am I?', 'a riddle!', 'riddle|enigma|puzzle|mystery|conundrum'],
				['what is round, hard, and sticks so far out of a man\'s pajamas that you can hang a hat on it?', 'a hat!', 'hat|cap'],
				['Maggie was born in 1757. She just had his 20th birth day today how did that happen?', '1757 is a room number!', 'hotel|motel|room.*number']
			],
			'de':[
				['Peters Mutter hat drei Kinder: Tick, Trick und ?', 'Peter!', 'peter'],
				['noch heute wird in vielen Regionen der Welt eine uralte Erfindung angewandt, die es dem Menschen ermöglicht, durch Wände zu schauen. Wie heißt diese Erfindung?', 'das Fenster!', 'fenster'],
				['welches Schimpfwort ergibt sich, wenn sich ein Uhu im Sand versteckt?', 'ein Sauhund!', 'sauhund'],
				['wie oft konnte Noah angeln?', 'zweimal, er hatte nur zwei Würmer!', 'zwei|2'],
				['welcher Berg war vor der Entdeckung des Mount Everest der höchste?', 'der Mount Everest war auch vor der Entdeckung der höchste!', 'mount|everest|selbst|selbe|gleiche'],
				['was kommt einmal in jeder Minute, zweimal in jedem Moment aber nie in tausend Jahren vor?', 'das M!', 'm'],
				['Helmut Kohl hat einen Kurzen, Arnold Schwarzenegger einen Langen, Ehepaare benutzen ihn oft gemeinsam, ein Junggeselle hat ihn für sich allein, Madonna hat keinen, und der Papst benutzt ihn nie. Was ist gmeint?', 'ein Nachname!', 'nach.*name'],
				['du machst bei einem Marathonlauf mit und überholst kurz vor dem Ziel den Zweiten. Wievielter bist du dann?', 'der zweite!', '2|zweite'],
				['ws hat keine Farbe, trotzdem kann man es sehen. Es wiegt nichts, aber jeder Gegenstand wird damit leichter. Was ist das?', 'ein Loch!', 'loch'],
				['was will jeder werden, aber keiner sein?', 'alt!', 'alt'],
				['wenn man es braucht, wirft man es weg! wenn man es nicht braucht, holt man es wieder zurück! Was ist das?', 'ein Anker!', 'anker'],
				['ein Gemüsehändler ist 1.85 m groß und 35 Jahre alt. Was wiegt er?', 'Gemüse!', 'gemüse'],
				['mit was beginnt Tag und was endet in Nacht?', 'einem T!', 't'],
				['ein Einbrecher war in einem Gebäude. Obwohl dieses gut bewacht war, gelang es ihm hinein zu kommen ohne Alarm auszulösen. Er hielt sich lange in dem Gebäude auf und ging dann wieder. Auch dabei wurde kein Alarm ausgelöst. Wäre er aber nicht so lange geblieben, so wäre er beim Verlassen des Gebäudes gescheitert. Was war das für ein Gebäude?', 'im Gefängnis!', 'gefängnis|knast'],
				['ein Mann verlässt sein Haus, steigt in sein Auto und fährt 120 km Richtung Süden. Dort angekommen kauft er einen neuen Pelzmantel für seine Frau. Danach fährt er 120 km Richtung Westen. Er erreicht einen Fachhandel für Messtechnik und informiert sich über technologische Neuerungen. Nun fährt er 120 km Richtung Norden und erreicht wieder sein Haus. Er sieht einen Bären der in der Abfalltonne wühlt. Welche Farbe hat der Bär?', 'das Haus des Mannes muß auf dem Nordpol stehen um mit der beschriebenen Route sein Haus wieder zu erreichen. Und in der Arktis gibt es nur weiße Eisbären!', 'eis.*bär|polar.*bär']
			]
		}
		guessed={
			'en':['Exactly,', 'Yes,', 'Very good,'],
			'de':['Exakt,', 'Ja,', 'Genau,', 'Sehr gut,']
		}
		reveal={
			'en':['It\'s', 'Well,'],
			'de':['Also', 'Naja,']
		}
		if (re.search('conundrum|riddle|scherzfrage|rätsel', message, re.IGNORECASE | re.DOTALL) or
			self.expects is not None and self.expects['skill'] == 'conundrum'):
			if self.expects is None:
				selected_set=random.randint(0, len(riddles[self.language])-1)
				self.expects = {'skill': 'conundrum', 'value': riddles[self.language][selected_set][2], 'set': selected_set}
				return '@'+self.user +', ' + riddles[self.language][selected_set][0]
			expected_value, selected_set = self.expects['value'], self.expects['set']
			self.expects = None
			if re.search(str(expected_value), message, re.IGNORECASE):
				return guessed[self.language][random.randint(0, len(guessed[self.language])-1)] + ' ' + riddles[self.language][selected_set][1]
			return reveal[self.language][random.randint(0, len(reveal[self.language])-1)] + ' ' + riddles[self.language][selected_set][1]
		return False

	def mastermind(self, message):
		greet={
			'en':['type in four different numbers between 0 and 9, i will tell you if any is correct and/or on the right position: '],
			'de':['rate vier zahlen zwischen 0 und 9. ich sage dir ob welche richtig und/oder an der richtigen stelle stehen: ']
		}
		error={
			'en':['nah, this is not the amount of numbers to guess.'],
			'de':['nö, die anzahl an ratezahlen ist nicht richtig.']
		}
		positionstr={
			'en':['number(s) at right position.'],
			'de':['zahl(en) an der richtigen stelle.']
		}
		numberstr={
			'en':['number(s) guessed but not their position.'],
			'de':['zahl(en) erraten aber nicht ihre position.']
		}
		again={
			'en':['again!'],
			'de':['nochmal!']
		}
		done={
			'en':['congratulations! number of guesses:'],
			'de':['glückwunsch! benötigte versuche:']
		}

		if (re.search('mastermind|cows and bulls|superhirn|logiktrainer', message, re.IGNORECASE | re.DOTALL) or
			self.expects is not None and self.expects['skill'] == 'mastermind'):
			if self.expects is None:
				solution=random.sample(range(0,9),4)
				self.expects = {'skill': 'mastermind', 'solution': [str(x) for x in solution], 'guesses': 0}
				return '@'+self.user +', ' + greet[self.language][0]

			answer=''
			guess=re.findall(r'\d', message)
			print (guess, self.expects['solution'])
			if len(guess) != 4:
				return '@'+self.user +', ' + error[self.language][0]
			self.expects['guesses'] += 1
			if guess != self.expects['solution']:
				number=0 
				position=0 
				for x in self.expects['solution']: 
					if x in guess: 
						if guess.index(x)==self.expects['solution'].index(x):
							position+=1
						else: 
							number+=1
				if position: 
					answer = f'@{self.user}, {answer} {position} {positionstr[self.language][0]}'
				if number: 
					answer = f'@{self.user}, {answer} {number} {numberstr[self.language][0]}'
				return f'@{self.user}, {answer} {again[self.language][0]}'
			else: 
				return f"@{self.user}, {done[self.language][0]} {self.expects['guesses']}"
		return False
	
	def tictactoefield(self, board_x=[]):
		x,y=len(board_x[0]),len(board_x)
		board=''
		for i in range(y*2+1): 
			for j in range(x): 
				if i%2: 
					board += '| '
					board += board_x[i//2][j] if board_x else ' '
					board += ' '
				else: 
					board += ' ---' 
			board += ('|' if i%2 else '') + '\n'
		return board

	def tictactoewinner(self, board_x):
		# scalable to every size dependable of board_x list BUT winner can only be determined on square board at the moment
		lines=len(board_x) 
		columns=len(board_x[0])
		# rearrange entries to vertical
		board_y=[] # vertical 
		for y in range(0,columns):
			for x in range(0,lines):
				try: 
					board_y[y]
				except: 
					board_y.append([])
				board_y[y].append(board_x[x][y]) 
		# rearrange entries to diagonal
		board_ul=[] # from upper left 
		board_ur=[] # from upper right 
		readxy=[[0]*lines] 
		readxy.append([]) 
		for i in range(columns):
			if i>0: 
				readxy[0].append(i)
			readxy[1].append(i)
		readxy[1].extend([columns-1]*(lines-1)) 
		#print('start coordinates: ',readxy)
		maxlen=lines if lines<=columns else columns
		for y in range(0,lines+columns-1): 
			for x in range(0,maxlen):
				try: 
					board_ul[y]
				except: 
					board_ul.append([])
					board_ur.append([])
				uly=readxy[1][y]-x 
				ulx=readxy[0][y]+x 
				if uly<0: 
					continue 
				elif ulx>maxlen-1: 
					continue 
				else: 
					board_ul[y].append(board_x[uly][ulx]) 

				ury=readxy[0][y]+x 
				urx=readxy[0][-1-y]+x 
				if ury<0: 
					continue 
				elif urx>maxlen-1: 
					continue 
				else: 
					board_ur[y].append(board_x[ury][urx])         

		win1=['X']*maxlen 
		win2=['O']*maxlen 
		if win1 in board_x+board_y+board_ul+board_ur and win2 in board_x+board_y+board_ul+board_ur:
			return ('draw') 
		elif win1 in board_x+board_y+board_ul+board_ur:
			return('X')
		elif win2 in board_x+board_y+board_ul+board_ur:
			return('O')
		else: 
			return False 

	def tictactoe(self, message):
		draw={
			'en':['please type in x-y coordinats for your draw:'],
			'de':['bitte gib die x-y kordinaten für deinen zug an:']
		}
		forbidden={
			'en':['field already set.'],
			'de':['feld bereits belegt.']
		}
		forbidden2={
			'en':['field out of bounds.'],
			'de':['feld außerhalb des spielfelds.']
		}
		end={
			'en':{'X': 'congratulations, you won!', 'O': 'i won!','draw': 'every one is a winner!'},
			'de':{'X': 'glückwunsch, du hast gewonnen!', 'O': 'ich habe gewonnen!', 'draw': "jeder ist ein gewinner!"}
		}

		if (re.search('tictactoe|tix tac toe|tic-tac-toe|drei gewinnt|drei-gewinnt|3 gewinnt', message, re.IGNORECASE | re.DOTALL) or
			self.expects is not None and self.expects['skill'] == 'tictactoe'):
			if self.expects is None:
				self.expects={'skill': 'tictactoe', 'game': xinarow(3,3)}
				return f'@{self.user}, {draw[self.language][0]}' + '\n' + self.tictactoefield(self.expects['game'].board)
			else:
				coords=re.findall(r'\d', message)
				coords=[int(x) for x in coords]
				if coords[0] > len(self.expects['game'].board) or coords[1] > len(self.expects['game'].board[0]):
					return f'@{self.user}, {forbidden2[self.language][0]} {draw[self.language][0]}'
				if not self.expects['game'].draw(coords[0],coords[1],'X'):
					return f'@{self.user}, {forbidden[self.language][0]} {draw[self.language][0]}'
				if len(self.expects['game'].free()):
					field=random.sample(self.expects['game'].free(),1)
					self.expects['game'].draw(int(field[0][1])+1,int(field[0][0])+1,'O')
				
				# evaluate winner 
				winner=self.tictactoewinner(self.expects['game'].board)
				if winner:
					winboard=self.expects['game'].board
					self.expects = None
					return f'@{self.user}, {end[self.language][winner]}' + '\n' + self.tictactoefield(winboard)
				return f'@{self.user}, {draw[self.language][0]}' + '\n' + self.tictactoefield(self.expects['game'].board)
	
	def rockpaperscissors(self, message):
		draw={
			'en':['please type rock, paper or scissors.'],
			'de':['bitte gib stein, papier oder schere für deinen zug an.']
		}
		end={
			'en':{'X': 'congratulations, you won!', 'O': 'i won!','draw': 'every one is a winner!'},
			'de':{'X': 'glückwunsch, du hast gewonnen!', 'O': 'ich habe gewonnen!', 'draw': "jeder ist ein gewinner!"}
		}
		beats={
			'en':['beats'],
			'de':['schlägt']
		}
		game={
			'en':[['rock','paper','scissors'],['paper','scissors','rock'],['scissors','rock','paper']],
			'de':[['stein','papier','schere'],['papier','schere','stein'],['scissors','schere','papier']]
		}
		if (re.search('rockpaperscissors|rock paper scissors|rock-paper-scissors|rps|steinpapierschere|stein papier schere|schnickschnackschnuck|schnick schnack schnuck|schnick-schnack-schnuck', message, re.IGNORECASE | re.DOTALL) or
			self.expects is not None and self.expects['skill'] == 'rockpaperscissors'):
			if self.expects is None:
				self.expects={'skill': 'rockpaperscissors'}
				return f'@{self.user}, {draw[self.language][0]}'
			else:
				bot=game[self.language][random.randint(0,2)]
				user=re.split(r'\W+', message)[-1]
				if not user in bot:
					return f'@{self.user}, {draw[self.language][0]}'					
				self.expects=None
				user=bot.index(user)
				if user < 1:
					return f'{bot[1]} {beats[self.language][0]} {bot[user]}. @{self.user}, {end[self.language]["O"]}'
				elif user > 1:
					return f'{bot[user]} {beats[self.language][0]} {bot[1]}. @{self.user}, {end[self.language]["X"]}'
				else:
					return f'{bot[user]} {end[self.language]["draw"]}'
	
	def decide(self, message):
		filterwords={
			'en':['and', 'or', 'between','decide','rule','clinch','determine'],
			'de':['und', 'oder', 'zwischen','entscheide','entscheiden','bestimme']
		}
		if (re.search('decide|rule|clinch|determine|entscheide|entscheiden|bestimme', message, re.IGNORECASE | re.DOTALL) or
			self.expects is not None and self.expects['skill'] == 'decide'):

			options=re.split(r'\W+', message)[2:]
			options=[x for x in options if x not in filterwords[self.language]]
			if self.expects is None and not options:
				self.expects = {'skill': 'decide'}
				answer = {
					'en': ['from which options should i decide for you?'],
					'de': ['aus welchen optionen soll ich für dich entscheiden?']
					}
				return f'@{self.user}, {answer[self.language][0]}'
			else:
				return f'@{self.user}, {random.choice(options)}'
		self.expects=None
