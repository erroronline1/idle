import sqlite3
import threading
import time
import datetime
import shutil
import math
import json
from pathlib import Path
import os
import sys

from colorama import Fore, Style, init
# possible console colors according to https://pypi.org/project/colorama/
# this however only works with print, not input in cmd and powershell, hence a strict separation from output and input

# windows-specific fancyness
try:
	from win11toast import toast
	import psutil
	if '.exe' in psutil.Process(os.getpid()).parent().name():
		# powershell is a bit odd on this
		init(convert=True)
except:
	def toast(*ignore):
		pass

HELLO = '''
                     _           _       _
 ___ ___ ___ ___ ___| |_ _ _ ___| |_ ___| |_
| .'|   | .'|  _|  _|   | | |  _|   | .'|  _|
|__,|_|_|__,|_| |___|_|_|_  |___|_|_|__,|_|
                        |___|                 built 20231226

by error on line 1 (erroronline.one)
'''
DEFAULT = { # default settings
	# relative paths do not work!
	# 'database': '\\\\fritz.box\\FRITZ.NAS\\anarchychat.db',
	'database': '\\\\192.168.178.26\\Public\\anarchychat.db', # e.g. on some network path
	'dblimit': 25, # sanitize database from all entries where ID < MAX(ID) - DBLIMIT
	'interval': 3, # seconds interval to fetch contribution updates, likely slightly limits read/write traffic on the drive
	'active': 30, # seconds to expire before a user is considered logged off. must be more than update interval
	'user': None, # default user name
	'language': 'en', # default language
	'title': 'AnarchyChat' # app title to display e.g. in notification
}

class anarchychat:
	fetchProcessRun = False
	fetchProcess = None
	fconnection = None
	bot = None
	notify = True
	latestid = 0
	errorcounter = {'start': int(time.time()), 'count': 0}

	def __init__(self, ini):
		self.database = self.dblimit = self.interval = self.active = self.user = self.language = self.title = None # i like you too, linter

		self.defaultini = ini
		# set attributes according to config file or default ini
		self.ini('get')
		# these are the available language chunks that can be extended as required
		# make sure the commands are registered appropriate in the command-method
		self.languageChunks = {
			'clear': {
				'en': 'all contributions being deleted',
				'de': 'alle beiträge gelöscht'
			}, 'databaseerror': {
				'en': 'sorry, that failed due to some database or connection error. please try again.\n{0} errors since starting {1} ago, restart if necessary (close window or type [exit]).\nif the problem persists the application will close by itself.',
				'de': 'das hat leider wegen eines datenbank- oder -verbindungsfehlers nicht funktioniert. bitte versuche es nochmal.\n{0} fehler seit dem start vor {1}, starte gegebenenfalls neu (fenster schließen oder [beenden] eingeben).\nwenn das problem weiterhin besteht, wird sich die anwendung selbst schließen.'
			}, 'goodbye': {
				'en': 'goodbye {0}!',
				'de': 'tschüß {0}!'
			}, 'greet': {
				'en': 'hello {0}! welcome to the chat. type [help] (with brackets) for command overview.\nthe chat will start with the latest {1} contributions if available. current users are {2}.\nstarting any moment...',
				'de': 'hallo {0}! willkommen im chat. gib [hilfe] (mit klammern) für eine befehlsübersicht ein.\nder chat startet mit den letzten {1} beiträgen falls vorhanden. aktuelle nutzer sind {2}.\ngleich geht es los...'
			}, 'help': {
				'en': '''available commands have to be typed with brackets:

[clear]    to clear database - affects all users!
[exit]     to quit
[interval] to change refresh interval
[language] to change the applications language
[name]     to change your name
[notify]   to toggle notification on new messages
[reset]    to delete config file and use default settings
[save]     to save current settings for next start
[users]    to show list of currently active users

@user      highlights the mention for the respective user 
''',
				'de': '''verfügbare befehle müssen mit klammern eingegeben werden:

[aktualisierung]   um die aktualisierungsrate zu ändern
[beenden]          um zu beenden
[benachrichtigung] um benachrichtigung bei neuen nachrichten an- oder ausschalten
[löschen]          um datenbank zu leeren - betrifft alle nutzer!
[name]             um deinen namen zu ändern
[nutzer]           um eine liste der aktiven nutzer anzuzeigen
[speichern]        um aktuelle einstellungen für den nächsten programmstart zu speichern
[sprache]          um die sprache des programms zu ändern
[zurücksetzen]     um konfigurationsdatei zu löschen und standardeinstellungen zu verwenden

@nutzer            hebt den entsprechenden benutzernamen farblich für diesen nutzer hervor
'''
			}, 'interval': {
				'en': 'enter seconds to refresh (1-10):',
				'de': 'gib sekunden zur aktualisierung ein (1-10):'
			}, 'joined': {
				'en': 'joined the chat',
				'de': 'hat den chat betreten'
			}, 'lang': {
				'en': 'supported languages are ',
				'de': 'unterstützte sprachen sind '
			}, 'left': {
				'en': 'left the chat',
				'de': 'hat den chat verlassen'
			}, 'name':{
				'en': 'enter new name:',
				'de': 'neuen namen eingeben:'
			}, 'nametaken':{
				'en': 'name already taken. you may wait about {0} seconds if this is your name though.',
				'de': 'name bereits belegt. du kannst auch etwa {0} sekunden warten, wenn es doch deiner ist.'
			}, 'notify': {
				'en': 'notifications are now {0}',
				'de': 'benachrichtigungen sind nun {0}'
			}, 'off': {
				'en': 'turned off',
				'de': 'ausgeschaltet'
			}, 'on': {
				'en': 'turned on',
				'de': 'eingeschaltet'
			}, 'reset': {
				'en': 'settings restored to default',
				'de': 'einstellungen auf standard zurückgesetzt'
			}, 'save': {
				'en': 'settings saved',
				'de': 'einstellungen gespeichert'
			}, 'setname': {
				'en': 'enter your name, [exit] (with brackets) to quit:',
				'de': 'bitte gib deinen namen ein, [exit] (mit klammern) um abzubrechen:'
			}, 'timeout': {
				'en': ' because of timeout',
				'de': ' weil die zeit ablief'
			}
		}

		# check if table exists, otherwise create
		try:
			self.connection = sqlite3.connect(self.database)
			c = self.connection.cursor()
			c.execute('''SELECT count(name) FROM sqlite_master WHERE type='table' AND name='CHAT';''')
			if not c.fetchone()[0]:
				self.connection.executescript('''
				CREATE TABLE CHAT
				(ID INTEGER PRIMARY KEY AUTOINCREMENT,
				NAME TINYTEXT NOT NULL,
				TIME TINYTEXT NOT NULL,
				MESSAGE TEXT NOT NULL);

				CREATE TABLE PING
				(NAME TINYTEXT UNIQUE,
				TOUCH TINYTEXT);''')
				self.connection.commit()
		except Exception as error:
			self.errorhandler(error, False)

	def ini(self, action):
		home = str(Path.home())
		if action == 'put':
			with open(home + '/anarchychat.json', 'w', newline = '', encoding = 'utf8') as file:
				# export properties according to default ini keys
				ini = {}
				for key in self.defaultini:
					ini[key] = getattr(self, key)
				json.dump(ini, file, ensure_ascii = False, indent = 4)
		elif action == 'get':
			try:
				with open(home + '/anarchychat.json', 'r') as jsonfile:
					ini = json.loads(jsonfile.read().replace('\n', ''))
			except:
				ini = self.defaultini
			# set attributes according to config file or default ini, except current user name 
			for key in ini:
				if ini == self.defaultini and key == 'user':
					continue
				setattr(self, key, ini[key])
		elif action == 'delete':
			if os.path.exists(home + '/anarchychat.json'):
				os.remove(home + '/anarchychat.json')

	def login(self):
		''' set username if none or already in use, or exit '''
		while not self.user or self.user in self.ping(self.connection, 'get'):
			self.fprint(self.lang('setname'), color = Fore.CYAN)
			select = str(input('> ')).strip()
			if select in self.ping(self.connection, 'get'):
				self.fprint(self.lang('nametaken', self.active), color = Fore.CYAN)
			elif len(select):
				self.user = select
		if self.user.lower() != '[exit]':
			currentusers=self.ping(self.connection, 'get')
			self.fprint(self.lang('greet', self.user, self.dblimit, ', '.join(currentusers) if len(currentusers) else self.lang('nousers')), color = Fore.CYAN)
			time.sleep(3)
			self.post(self.fprint(self.lang('joined'), justcolorize = Fore.CYAN))
			if self.bot is not None:
				self.post(self.bot.parse('@bot hello hallo', self.language, self.user), self.bot.name)
			self.start()
		else:
			self.exit()

	def start(self):
		''' start new thread for simultaneously retrieving and posting contributions and wait for input '''
		self.fetchProcessRun = True
		self.fetchProcess = threading.Thread(target = self.fetch, daemon = True)
		self.fetchProcess.start()
		while True:
			try:
				message = str(input('\r> ')).strip()
				if not self.command(message):
					self.exit()
			except KeyboardInterrupt:
				self.exit()

	def exit(self):
		''' delete user from active table, close database connection and exit program '''
		self.fetchProcessRun = False
		if hasattr(self, 'connection'):
			self.ping(self.connection, 'delete', {'NAME': self.user})
			self.connection.close()
		self.fprint(self.lang('goodbye', self.user if self.user.lower() != '[exit]' else ''), color = Fore.CYAN)
		time.sleep(2)
		sys.exit()

	def errorhandler(self, error, resume = None):
		self.errorcounter['count'] += 1
		runtime = int(time.time()) - self.errorcounter['start']
		runtime = datetime.timedelta(seconds = runtime)
		emsg=str(error.message if hasattr(error, 'message') else error)
		self.fprint(self.lang('databaseerror', self.errorcounter['count'], runtime) + ' ' + emsg + '\n', color = Fore.RED)

		if resume :
			self.fetchProcessRun = False
			if hasattr(self, 'fetchProcess'):
				self.fetchProcess.join()
			del self.connection
			try:
				self.connection = sqlite3.connect(self.database)
			except Exception as e:
				self.errorhandler(e, False)
			self.start()
		elif not resume and resume is not None:
			self.exit()
		else:
			return False

	def fetch(self):
		''' fetch the latest contributions every so many seconds, notify about new messages and tell about being still active
			needs another connection for running in separate thread '''
		self.fconnection = None
		try:
			self.fconnection = sqlite3.connect(self.database)
			while self.fetchProcessRun:
				cursor = self.fconnection.cursor()
				cursor.execute(f'SELECT * FROM CHAT WHERE ID > {self.latestid}')
				results = cursor.fetchall()
				if len(results):
					for result in results:
						self.fprint (f'\r{result[2]} | {(self.fprint(result[1], justcolorize = Fore.YELLOW) if result[1] == self.user else result[1])}: {self.mention(result[3])}')
						self.latestid = result[0]
						latestuser = result[1]
					if latestuser != self.user and self.notify:
						toast(self.title + ' | ' + result[1], result[3], on_dismissed=self.doNothing)
					self.fprint('\r> ', newline = False)
				# ping your name to the active list
				self.ping(self.fconnection, 'put')
				time.sleep(self.interval)
			self.fconnection.close()
		except Exception as e:
			del self.fconnection
			self.errorhandler(e)
			#raise Exception(e) from None
			# 'from none' to avoid messing up the error output with:
			# During handling of the above exception, another exception occurred:
			# see https://www.python.org/dev/peps/pep-0409/

	def post(self, message, user = None):
		''' insert message and delete older entries '''
		message = message.replace('\'','\'\'')
		try:
			self.connection.executescript(f"""
				INSERT INTO CHAT (ID, NAME, TIME, MESSAGE) VALUES (NULL, '{user if user else self.user}', '{datetime.datetime.now().strftime("%d.%m.%y %H:%M:%S")}', '{message}');
				DELETE FROM CHAT WHERE ID IN (SELECT ID FROM CHAT ORDER BY ID DESC LIMIT (SELECT COUNT(*) FROM CHAT) OFFSET {self.dblimit});
				""")
			self.connection.commit()
		except Exception as e:
			self.errorhandler(e, True)

	def clearDB(self):
		''' truncate table '''
		try:
			self.connection.executescript('''DELETE FROM CHAT; VACUUM;''')
			self.connection.commit()
		except Exception as e:
			self.errorhandler(e, True)

	def ping(self, conn, method, fields = None):
		''' connection must be passed to be usable from different threads '''
		if method == 'put':
			try:
				conn.execute(f"INSERT OR REPLACE INTO PING (NAME, TOUCH) VALUES ('{self.user}', strftime('%s', 'now'));")
				conn.commit()
			except Exception as e:
				self.errorhandler(e, True)
		elif method == 'get':
			self.ping(conn, 'delete')
			cursor = conn.cursor()
			cursor.execute('''SELECT * FROM PING''')
			results = cursor.fetchall()
			out = [] if self.bot is None else [self.bot.name]
			if len(results):
				for result in results:
					out.append(result[0])
			return out
		elif method == 'delete':
			try:
				if fields is None:
					cursor = conn.cursor()
					cursor.execute(f"SELECT NAME FROM PING WHERE (strftime('%s', 'now') - TOUCH) > {self.active};")
					results = cursor.fetchall()
					if len(results):
						for result in results:
							if result[0] != self.user:
								self.post(self.fprint(self.lang('left') + self.lang('timeout'), justcolorize = Fore.CYAN), result[0])
					conn.execute(f"DELETE FROM PING WHERE (strftime('%s', 'now') - TOUCH) > {self.active};")
				else:
					conn.execute(f"DELETE FROM PING WHERE {list(fields.keys())[0]}='{fields[list(fields.keys())[0]]}';")
				conn.commit()
			except Exception as e:
				self.errorhandler(e, True)

	def fprint(self, string, color = None, newline = True, justcolorize = None):
		''' more universal use and output cleansing compared to plain print() '''
		if color is not None:
			string = f'{color}{string}{Style.RESET_ALL}'
		elif justcolorize is not None:
			string = f'{justcolorize}{string}{Style.RESET_ALL}'
		if justcolorize is None:
			terminalwidth = shutil.get_terminal_size(0)[0]
			string = '\r' + string
			if newline:
				string = string + ' ' * (terminalwidth- len(string)) + '\n'
			sys.stdout.write(string)
			sys.stdout.flush()
			return
		return string

	def mention(self, message):
		usertag = '@' + self.user
		if usertag in message:
			message = message.replace(usertag, self.fprint(usertag, justcolorize = Fore.YELLOW))
		return message

	def lang(self, chunk, *args):
		if chunk in self.languageChunks and self.language in self.languageChunks[chunk]:
			return self.languageChunks[chunk][self.language].format(*args)
		return f"*UNDEFINED LANGUAGE FOR {chunk}*"

	def command(self, message):
		''' filter and conditionally execute commands '''
		if message.lower() in ('[clear]', '[löschen]'):
			self.fprint(self.lang('clear'), color = Fore.CYAN)
			self.clearDB()
			return True
		if message.lower() in ('[exit]', '[beenden]'):
			self.post(self.fprint(self.lang('left'), justcolorize = Fore.CYAN))
			return False
		if message.lower() in ('[help]', '[hilfe]'):
			self.fprint(self.lang('help'), color = Fore.CYAN)
			return True
		if message.lower() in ('[interval]', '[aktualisierung]'):
			self.fprint(self.lang('interval'), color = Fore.CYAN)
			select=int(input('> '))
			if 0 < select < 11:
				self.interval = select
			return True
		if message.lower() in ('[language]', '[sprache]'):
			supported = list(self.languageChunks['lang'].keys())
			self.fprint(self.lang('lang') +  ', '.join(supported) + ': ', color = Fore.CYAN)
			select = str(input('> ')).lower()
			if select in supported:
				self.language = select
			return True
		if message.lower() in ('[name]', '[name]'):
			self.fprint(self.lang('name'), color = Fore.CYAN)
			select = str(input('> ')).strip()
			if select in self.ping(self.connection, 'get'):
				self.fprint(self.lang('nametaken', self.active), color = Fore.CYAN)
			elif len(select):
				self.ping(self.connection, 'delete', {'NAME': self.user})
				self.user = select
			return True
		if message.lower() in ('[notify]', '[benachrichtigung]'):
			self.notify = not self.notify
			self.fprint(self.lang('notify', self.lang('on') if self.notify else self.lang('off')), color = Fore.CYAN)
			return True
		if message.lower() in ('[reset]', '[zurücksetzen]'):
			self.ini('delete')
			self.ini('get')
			self.fprint(self.lang('reset'), color = Fore.CYAN)
			return True
		if message.lower() in ('[save]', '[speichern]'):
			self.ini('put')
			self.fprint(self.lang('save'), color = Fore.CYAN)
			return True
		if message.lower() in ('[users]', '[nutzer]'):
			self.fprint(', '.join(self.ping(self.connection, 'get')), color = Fore.CYAN)
			return True
		terminalwidth = shutil.get_terminal_size(0)[0]
		# clear input display - supports multi line inputs
		# may be ugly if console dimensions are changed during use
		linter=0 # highlighting unused i distracts me...
		for i in range(0, math.ceil(len(message) / terminalwidth)):
			linter += i
			self.fprint('\033[A' + (' ' * (terminalwidth)) + '\033[A')
		if len(message):
			self.post(message)
			if self.bot is not None:
				botmsg = self.bot.parse(message, self.language, self.user)
				if botmsg:
					self.post(botmsg, self.bot.name)
		return True

	def doNothing(self, *args):
		pass

if __name__ == '__main__':
	# anarchychat is supposed to work without the stupidbot as well
	# however as siblings the anarchychat is rooting the user name and message according to stupidbots methods
	# implementation is meant to be kept as little as possible though
	from stupidbot import stupidbot
	chat = anarchychat(DEFAULT)
	chat.fprint(HELLO, color = Fore.CYAN)
	chat.bot = stupidbot('bot') # final decision whether bot is available or not
	chat.login()
