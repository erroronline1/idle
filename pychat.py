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
from win10toast import ToastNotifier

HELLO = '''
                     _           _       _
 ___ ___ ___ ___ ___| |_ _ _ ___| |_ ___| |_
| .'|   | .'|  _|  _|   | | |  _|   | .'|  _|
|__,|_|_|__,|_| |___|_|_|_  |___|_|_|__,|_|
                        |___|                 built 20210904

by error on line 1 (erroronline.one)
'''

INI = {
	'database' : '\\\\192.168.178.26\\Public\\anarchychat.db', # e.g. on some network path
	'dblimit' : 25, # sanitize database from all entries where ID < MAX(ID) - DBLIMIT
	'update' : 3, # seconds interval to fetch contribution updates, likely slightly limits read/write traffic on the drive
	'active' : 30, # seconds to expire before a user is considered logged off. must be more than update interval
	'user' : None, # initiate global user name, changeable
	'language' : 'en', # default language, changeable
	'title': 'AnarchyChat' # app title to display e.g. in notification
}

class anarchychat:
	def __init__(self, ini):
		self.database = ini['database']
		self.dblimit = ini['dblimit']
		self.interval = ini['update']
		self.active = ini['active']
		self.user = ini['user']
		self.language = ini['language']
		self.title = ini['title']
		self.notify = True
		self.languageChunks = {
			'setname': {
				'en': 'enter your name, [exit] to quit: ',
				'de': 'bitte gib deinen namen ein, [exit] um abzubrechen: '
			}, 'greet': {
				'en': 'hello {0}! welcome to the chat. type [help] for command overview.\nthe chat will start with the latest {1} contributions. current users are {2}.\nstarting any moment...',
				'de': 'hallo {0}! willkommen im chat. gib [help] für eine befehlsübersicht ein.\nder chat startet mit den letzten {1} beiträgen. aktuelle nutzer sind {2}.\ngleich geht es los...'
			}, 'goodbye': {
				'en': 'goodbye!',
				'de': 'tschüß!'
			}, 'joined': {
				'en': 'joined the chat',
				'de': 'hat den chat betreten'
			}, 'left': {
				'en': 'left the chat',
				'de': 'hat den chat verlassen'
			}, 'timeout': {
				'en': ' because of timeout',
				'de': ' weil die zeit ablief'
			}, 'clear': {
				'en': 'all contributions being deleted',
				'de': 'alle beiträge gelöscht'
			}, 'lang': {
				'en': 'supported languages are ',
				'de': 'unterstützte sprachen sind '
			}, 'name':{
				'en': 'enter new name: ',
				'de': 'neuen namen eingeben: '
			}, 'nametaken':{
				'en': 'name already taken',
				'de': 'name bereits belegt'
			}, 'notify': {
				'en': 'notifications are now {0}',
				'de': 'benachrichtigungen sind nun {0}'
			}, 'on': {
				'en': 'turned on',
				'de': 'eingeschaltet'
			}, 'off': {
				'en': 'turned off',
				'de': 'ausgeschaltet'
			}, 'help': {
				'en': '''[clear] to truncate database - affects all users!
[exit] to quit
[lang] to change language
[name] to change your name
[notify] to toggle notification on new messages
[users] to show list of currently active users''',
				'de': '''[clear] um datenbank zu leeren - betrifft alle nutzer!
[exit] um zu beenden
[lang] um die sprache zu ändern
[name] um deinen namen zu ändern
[notify] um benachrichtigung bei neuen nachrichten an- oder ausschalten
[users] um eine liste der aktiven nutzer anzuzeigen'''
			}
		}

		# check if table exists, otherwise create
		self.connection = sqlite3.connect(self.database)
		c = self.connection.cursor()
		c.execute('''SELECT count(name) FROM sqlite_master WHERE type='table' AND name='CHAT';''')
		if not c.fetchone()[0] :
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
		if self.login():
			self.start()

	def login(self):
		# set username
		while not self.user:
			print(self.colorize(self.lang('setname'), Fore.GREEN))
			select = str(input('> ')).strip()
			if select in self.ping(self.connection, 'get'):
				print(self.colorize(self.lang('nametaken'), Fore.GREEN))
			elif len(select):
				self.user = select
		if self.user.lower() != '[exit]':
			print(self.colorize(self.lang('greet', self.user, self.dblimit, ', '.join(self.ping(self.connection, 'get'))), Fore.GREEN))
			time.sleep(3)
			return True
		self.exit()
	
	def start(self):
		# start new thread for simultaneously retrieving and posting contributions and wait for input
		get_contents = threading.Thread(target = self.fetch)
		get_contents.daemon = True
		get_contents.start()

		self.post(self.colorize(self.lang('joined'), Fore.GREEN))
		while True:
			try:
				message = str(input('\r> '))
				if not self.filterinput(message):
					self.exit()
			except KeyboardInterrupt:
				self.exit()

	def exit(self):
		# delete user from active table, close database connection and exit program
		self.ping(self.connection, 'delete', {'NAME': self.user})
		print(self.colorize(self.lang('goodbye'), Fore.GREEN))
		self.connection.close()
		time.sleep(2)
		exit()

	def fetch(self):
		# fetch the latest contributions every so many seconds, notify about new messages and tell about being still active 
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
					latestmsg = {'title': result[1], 'msg': result[3]}
				if latestuser != self.user:
					self.notification(latestmsg)
				print('\r> ', end = '')
			# ping your name to the active list
			self.ping(fconnection, 'put')
			time.sleep(self.interval)

	def post(self, message, user = None):
		# insert message and delete older entries 
		message = message.replace('\'','\'\'')
		self.connection.executescript('''
			INSERT INTO CHAT (ID, NAME, TIME, MESSAGE) VALUES (NULL, '{0}', '{1}', '{2}');
			DELETE FROM CHAT WHERE ID IN (SELECT ID FROM CHAT ORDER BY ID DESC LIMIT (SELECT COUNT(*) FROM CHAT) OFFSET {3});
			'''.format(
				user if user else self.user,
				datetime.datetime.now().strftime('%d.%m.%y %H:%M:%S'),
				message,
				self.dblimit))
		self.connection.commit()

	def clearDB(self):
		# truncate table
		self.connection.executescript('''DELETE FROM CHAT; VACUUM;''')
		self.connection.commit()

	def ping(self, conn, method, fields=None):
		if method == 'put':
			conn.execute('''INSERT OR REPLACE INTO PING (NAME, TOUCH) VALUES ('{0}', strftime('%s', 'now'));'''.format(self.user))
			conn.commit()
		elif method == 'get':
			self.ping(conn, 'delete')
			cursor = conn.cursor()
			cursor.execute('''SELECT * FROM PING''')
			results = cursor.fetchall()
			out=[]
			if len(results):
				for result in results:
					out.append(result[0])
			return out
		elif method == 'delete':
			if not fields:
				cursor = conn.cursor()
				cursor.execute('''SELECT NAME FROM PING WHERE (strftime('%s', 'now') - TOUCH) > {0};'''.format(self.active))
				results = cursor.fetchall()
				if len(results):
					for result in results:
						if result[0] != self.user:
							self.post(self.colorize(self.lang('left') + self.lang('timeout'), Fore.GREEN), result[0])
				conn.execute('''DELETE FROM PING WHERE (strftime('%s', 'now') - TOUCH) > {0};'''.format(self.active))
			else:
				conn.execute('''DELETE FROM PING WHERE {0}='{1}';'''.format(list(fields.keys())[0], fields[list(fields.keys())[0]]))
			conn.commit()

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
		if message.lower() == '[clear]':
			print(self.colorize(self.lang('clear'), Fore.GREEN))
			self.clearDB()
			return True
		elif message.lower() == '[exit]':
			self.post(self.colorize(self.lang('left'), Fore.GREEN))
			return False
		elif message.lower() == '[help]':
			print(self.colorize(self.lang('help'), Fore.GREEN))
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
			select = str(input('> ')).strip()
			if select in self.ping(self.connection, 'get'):
				print(self.colorize(self.lang('nametaken'), Fore.GREEN))
			elif len(select):
				self.ping(self.connection, 'delete', {'NAME': self.user})
				self.user = select
			return True
		elif message.lower() == '[notify]':
			self.notify = not self.notify
			print(self.colorize(self.lang('notify', self.lang('on') if self.notify else self.lang('off')), Fore.GREEN))
			return True
		elif message.lower() == '[users]':
			print(self.colorize(','.join(self.ping(self.connection, 'get')), Fore.GREEN))
			return True
		else:
			terminalwidth, terminalheight = shutil.get_terminal_size(0)
			# clear input display - supports multi line inputs
			# may be ugly if console dimensions are changes during use
			for i in range(0, math.ceil(len(message) / terminalwidth)):
				terminalheight = terminalheight + i # sometimes linter can be annoying...
				print('\033[A' + (' ' * (terminalwidth - 2)) + '\033[A')
			if len(message.strip()):
				self.post(message)
			return True

	def notification(self, msg):
		# notification handling as an easily adaptable method for your convenience 
		if self.notify:
			if not hasattr(self, 'toast'):
				self.toast = ToastNotifier()
			# winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS)
			self.toast.show_toast(self.title + ' | ' + msg['title'], msg['msg'], threaded = True, icon_path = None, duration = 3)

if __name__ == '__main__':
	print(HELLO)
	chat = anarchychat(INI)