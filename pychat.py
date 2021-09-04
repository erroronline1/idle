import sqlite3
import threading
import time
import datetime
import shutil
import math
import winsound
from colorama import Fore, Style, init
import psutil
import os

HELLO = '''
             _       _
 ___ _ _ ___| |_ ___| |_
| . | | |  _|   | .'|  _|
|  _|_  |___|_|_|__,|_|
|_| |___|                 built 20210904

by error on line 1 (erroronline.one)
'''

INI={
'database' : '\\\\192.168.178.26\\Public\\pychat.db', # e.g. on some network path
'dblimit' : 25, # sanitize database from all entries where ID < MAX(ID) - DBLIMIT
'update' : 2, # seconds interval to fetch contribution updates
'user' : None, # initiate global user name, changeable
'language' : 'en', # default language, changeable
}

class anarchychat:
	def __init__(self, ini):
		self.database = ini['database']
		self.dblimit = ini['dblimit']
		self.interval = ini['update']
		self.user = ini['user']
		self.language = ini['language']
		self.notify = True
		self.languageChunks = {
			'setname': {
				'en': 'enter your name, [exit] to quit: ',
				'de': 'bitte gib deinen namen ein, [exit] um abzubrechen: '
			}, 'greet': {
				'en': 'hello {0}! welcome to the chat. type [help] for command overview. the chat will start with the latest {1} contributions. press enter to continue...',
				'de': 'hallo {0}! willkommen im chat. gib [help] für eine befehlsübersicht ein. der chat startet mit den letzten {1} beiträgen. drücke enter um fortzufahren...'
			}, 'goodbye': {
				'en': 'goodbye!',
				'de': 'tschüß!'
			}, 'joined': {
				'en': 'joined the chat',
				'de': 'hat den chat betreten'
			}, 'left': {
				'en': 'left the chat',
				'de': 'hat den chat verlassen'
			}, 'clear': {
				'en': 'all contributions being deleted',
				'de': 'alle beiträge gelöscht'
			}, 'lang': {
				'en': 'supported languages are ',
				'de': 'unterstützte sprachen sind '
			}, 'name':{
				'en': 'enter new name: ',
				'de': 'neuen namen eingeben: '
			}, 'sound': {
				'en': 'sound is now {0}',
				'de': 'ton ist nun {0}'
			}, 'on': {
				'en': 'on',
				'de': 'eingeschaltet'
			}, 'off': {
				'en': 'off',
				'de': 'ausgeschaltet'
			}, 'help': {
				'en': '''[exit] to quit
[clear] to truncate database - affects all users!
[lang] to change language
[name] to change your name
[sound] toggle sound on new messages''',
				'de': '''[exit] um zu beenden
[clear] um datenbank zu leeren - betrifft alle nutzer!
[lang] um die sprache zu ändern
[name] um deinen namen zu ändern
[sound] ton bei neuen nachrichten an oder aus'''
			}
		}

		# check if table exists, otherwise create
		self.connection = sqlite3.connect(self.database)
		c = self.connection.cursor()
		c.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='CHAT' ''')
		if not c.fetchone()[0] :
			self.connection.execute('''CREATE TABLE CHAT
				(ID INTEGER PRIMARY KEY AUTOINCREMENT,
				NAME TINYTEXT NOT NULL,
				TIME TINYTEXT NOT NULL,
				MESSAGE TEXT NOT NULL);''')
			self.connection.commit()
		if self.login():
			self.start()

	def login(self):
		# set username
		while not self.user:
			print(self.colorize(self.lang('setname'), Fore.GREEN))
			self.user = str(input('> '))
		if self.user.lower() != '[exit]':
			print(self.colorize(self.lang('greet', self.user, self.dblimit), Fore.GREEN))
			input()
			return True
		self.exit()
	
	def start(self):
		# start new thread for simultaneously retrieving and posting contributions and wait for input
		get_contents = threading.Thread(target = self.fetch)
		get_contents.daemon = True
		get_contents.start()

		self.post(self.colorize(self.lang('joined'), Fore.GREEN))
		while True:
			message = str(input('\r> '))
			if not self.filterinput(message):
				self.exit()

	def exit(self):
		# exit program
		print(self.colorize(self.lang('goodbye'), Fore.GREEN))
		self.connection.close()
		time.sleep(2)
		exit()

	def fetch(self):
		# fetch the latest contributions every so many seconds
		# needs another connection for running in separate thread
		fconnection = sqlite3.connect(self.database)
		latestid = 0
		while True:
			cursor = fconnection.cursor()
			cursor.execute('''SELECT * FROM CHAT WHERE ID > {0}'''.format(latestid))
			results = cursor.fetchall()
			if len(results):
				for result in results:
					print ('\r{0} | {1}: {2}'.format(result[2], (self.colorize(result[1], Fore.YELLOW) if result[1] == self.user else result[1]), result[3]))
					latestid = result[0]
					latestuser = result[1]
				if self.notify and latestuser != self.user:
					winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS)
				print('\r> ', end = '')
			time.sleep(self.interval)

	def post(self, message):
		# insert input and delete all older entries 
		message = message.replace('\'','\'\'')
		self.connection.execute('''INSERT INTO CHAT (ID, NAME, TIME, MESSAGE) VALUES
			(NULL, '{0}', '{1}', '{2}');'''.format(self.user, datetime.datetime.now().strftime('%d.%m.%y %H:%M:%S'), message))
		self.connection.execute('''DELETE FROM CHAT WHERE ID IN (SELECT ID FROM CHAT ORDER BY ID DESC LIMIT (SELECT COUNT(*) FROM CHAT) OFFSET {0});'''.format(self.dblimit))
		self.connection.commit()

	def clearDB(self):
		# truncate table
		self.connection.execute('''DELETE FROM CHAT''')
		self.connection.commit()

	def colorize(self, str, col):
		# occasionally fancy colors for outputs
		# possible colours according to https://pypi.org/project/colorama/
		# this however only works with print, not input in cmd and powershell
		if psutil.Process(os.getpid()).parent().name() in ['py.exe', 'powershell.exe', 'cmd.exe']:
			# powershell is a bit odd on this
			init(convert=True)
		return f'{col}{str}{Style.RESET_ALL}'

	def lang(self, chunk, *args):
		if chunk in self.languageChunks and self.language in self.languageChunks[chunk]:
			return self.languageChunks[chunk][self.language].format(*args)
		else:
			return '*UNDEFINED LANGUAGE FOR {0}*'.format(chunk)
		
	def filterinput(self, message):
		# filter and conditionally execute commands
		if message.lower() == '[exit]':
			self.post(self.colorize(self.lang('left'), Fore.GREEN))
			return False
		elif message.lower() == '[help]':
			print(self.colorize(self.lang('help'), Fore.GREEN))
			return True
		elif message.lower() == '[clear]':
			print(self.colorize(self.lang('clear'), Fore.GREEN))
			self.clearDB()
			return True
		elif message.lower() == '[lang]':
			supported = list(self.languageChunks['lang'].keys())
			print(self.colorize(self.lang('lang') +  ', '.join(supported) + ': ', Fore.GREEN))
			select = str(input('> ')).lower()
			if select in supported:
				self.language = select
			return True
		elif message.lower() == '[name]':
			print(self.colorize(self.lang('name'), Fore.GREEN))
			select = str(input('> '))
			if len(select.strip()):
				self.user = select
			return True
		elif message.lower() == '[sound]':
			self.notify = not self.notify
			print (self.colorize(self.lang('sound', self.lang('on') if self.notify else self.lang('off')), Fore.GREEN))
			return True
		else:
			terminalwidth, terminalheight = shutil.get_terminal_size(0)
			# clear input display - supports multi line inputs
			# may be ugly if console dimensions are changes during use
			for i in range(0, math.ceil(len(message) / terminalwidth)):
				terminalheight = terminalheight + i # sometimes linter can be annoying...
				print('\033[A', ' ' * (terminalwidth - 2), '\033[A')
			if len(message.strip()):
				self.post(message)
			return True

if __name__ == '__main__':
	print(HELLO)
	chat=anarchychat(INI)