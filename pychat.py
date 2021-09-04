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
# real constants
DATABASE = '\\\\192.168.178.26\\Public\\pychat.db' # e.g. on some network path
DBLIMIT = 25 # sanitize database from all entries where ID < MAX(ID) - DBLIMIT
UPDATE = 2 # seconds interval to fetch contribution updates

# pseudo-constants, but globally used
CONNECTION = None # initiate global connection object
USER = None # initiate global user name, changeable
SOUND = True # play sound on new messages, toggleable

SLANG = 'en' # default language, changeable
LANGUAGE = {
	'setname': {
		'en': 'enter your name, [exit] to quit: ',
		'de': 'bitte gib deinen namen ein, [exit] um abzubrechen: '
	},
	'greet': {
		'en': 'hello {0}! welcome to the chat. type [help] for command overview. the chat will start with the latest {1} contributions. press enter to continue...',
		'de': 'hallo {0}! willkommen im chat. gib [help] für eine befehlsübersicht ein. der chat startet mit den letzten {1} beiträgen. drücke enter um fortzufahren...'
	},
	'goodbye': {
		'en': 'goodbye!',
		'de': 'tschüß!'
	},
	'joined': {
		'en': 'joined the chat',
		'de': 'hat den chat betreten'
	},
	'left': {
		'en': 'left the chat',
		'de': 'hat den chat verlassen'
	},
	'clear': {
		'en': 'all contributions being deleted',
		'de': 'alle beiträge gelöscht'
	},
	'lang': {
		'en': 'supported languages are ',
		'de': 'unterstützte sprachen sind '
	},
	'name':{
		'en': 'enter new name: ',
		'de': 'neuen namen eingeben: '
	},
	'sound': {
		'en': 'sound is now {0}',
		'de': 'ton ist nun {0}'
	},
	'on': {
		'en': 'on',
		'de': 'eingeschaltet'
	},
	'off': {
		'en': 'off',
		'de': 'ausgeschaltet'
	},
	'help': {
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
def lang(chunk, *args):
	if chunk in LANGUAGE and SLANG in LANGUAGE[chunk]:
		return LANGUAGE[chunk][SLANG].format(*args)
	else:
		return '*UNDEFINED LANGUAGE FOR {0}*'.format(chunk)

def open_create(db):
	# check if table exists, otherwise create
	connection = sqlite3.connect(db)
	c = connection.cursor()
	c.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='CHAT' ''')
	if not c.fetchone()[0] :
		connection.execute('''CREATE TABLE CHAT
			(ID INTEGER PRIMARY KEY AUTOINCREMENT,
			NAME TINYTEXT NOT NULL,
			TIME TINYTEXT NOT NULL,
			MESSAGE TEXT NOT NULL);''')
		connection.commit()
	connection.close()

def get_recent(db):
	# fetch the latest contributions every UPDATE seconds
	# needs another connection for running in separate thread
	global UPDATE
	global SOUND
	connection = sqlite3.connect(db)
	latestid = 0
	while True:
		cursor = connection.cursor()
		cursor.execute('''SELECT * FROM CHAT WHERE ID > {0}'''.format(latestid))
		results = cursor.fetchall()
		if len(results):
			for result in results:
				print ('\r{0} | {1}: {2}'.format(result[2], (colorize(result[1], Fore.YELLOW) if result[1] == USER else result[1]), result[3]))
				latestid = result[0]
				latestuser = result[1]
			if SOUND and latestuser != USER:
				winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS)
			print('\r> ', end = '')
		time.sleep(UPDATE)

def put_recent(user, message):
	# insert input and delete all older entries 
	global CONNECTION
	global DBLIMIT
	escape=['\\', '\'', '\"']
	for e in escape:
		message = message.replace(e, '\\' + e)

	CONNECTION.execute('''INSERT INTO CHAT (ID, NAME, TIME, MESSAGE) VALUES
		(NULL, '{0}', '{1}', '{2}');'''.format(user, datetime.datetime.now().strftime('%d.%m.%y %H:%M:%S'), message))
	CONNECTION.execute('''DELETE FROM CHAT WHERE ID IN (SELECT ID FROM CHAT ORDER BY ID DESC LIMIT (SELECT COUNT(*) FROM CHAT) OFFSET {0});'''.format(DBLIMIT))
	CONNECTION.commit()

def clear_recent():
	# truncate table
	global CONNECTION
	CONNECTION.execute('''DELETE FROM CHAT''')
	CONNECTION.commit()

def colorize(str, col):
	# occasionally fancy colors for outputs
	# possible colours according to https://pypi.org/project/colorama/
	# this however only works with print, not input in cmd and powershell
	if psutil.Process(os.getpid()).parent().name() in ['py.exe', 'powershell.exe', 'cmd.exe']:
		# in powershell is a bit odd on this
		init(convert=True)
	return f'{col}{str}{Style.RESET_ALL}'
	
def filterinput(user, message):
	# filter and conditionally execute commands
	global SLANG
	global USER
	global SOUND
	if message.lower() == '[exit]':
		put_recent(user, colorize(lang('left'), Fore.GREEN))
		return False
	elif message.lower() == '[help]':
		print(colorize(lang('help'), Fore.GREEN))
		return True
	elif message.lower() == '[clear]':
		print(colorize(lang('clear'), Fore.GREEN))
		clear_recent()
		return True
	elif message.lower() == '[lang]':
		supported = list(LANGUAGE['lang'].keys())
		print(colorize(lang('lang') +  ', '.join(supported) + ': ', Fore.GREEN))
		select = str(input('> ')).lower()
		if select in supported:
			SLANG = select
		return True
	elif message.lower() == '[name]':
		print(colorize(lang('name'), Fore.GREEN))
		select = str(input('> '))
		if len(select.strip()):
			USER = select
		return True
	elif message.lower() == '[sound]':
		SOUND = not SOUND
		print (colorize(lang('sound', lang('on') if SOUND else lang('off')), Fore.GREEN))
		return True
	else:
		terminalwidth, terminalheight = shutil.get_terminal_size(0)
		# clear input display - supports multi line inputs
		# my be ugly if console dimensions are changes during use
		for i in range(0, math.ceil(len(message) / terminalwidth)):
			terminalheight = terminalheight + i # sometimes linter can be annoying...
			print('\033[A', ' ' * (terminalwidth - 2), '\033[A')
		if len(message.strip()):
			put_recent(user, message)
		return True

if __name__ == '__main__':
	open_create(DATABASE)
	print(colorize(HELLO, Fore.CYAN))
	while not USER:
		print(colorize(lang('setname'), Fore.GREEN))
		USER = str(input('> '))
	if USER.lower() != '[exit]':
		print(colorize(lang('greet', USER, DBLIMIT), Fore.GREEN))
		input()
		# start new thread for simultaneously retrieving and posting contributions
		get_contents = threading.Thread(target = get_recent, kwargs = {'db': DATABASE})
		get_contents.daemon = True
		get_contents.start()

		CONNECTION = sqlite3.connect(DATABASE)
		put_recent(USER, colorize(lang('joined'), Fore.GREEN))
		while True:
			message = str(input('\r> '))
			if not filterinput(USER, message):
				break
	else:
		print(colorize(lang('goodbye'), Fore.GREEN))
	if CONNECTION:
		CONNECTION.close()
	exit()
