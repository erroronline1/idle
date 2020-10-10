import json
import re
import requests
import sys
import os
import threading
import shutil
import itertools
import time
import random
from datetime import date, datetime

print ('''
                         _
 ___ ___ ___ _ _ _ _ ___|_|___ ___
| . |  _| . |_'_| | | . | |   | . |
|  _|_| |___|_,_|_  |  _|_|_|_|_  |
|_|             |___|_|       |___|

    by error on line 1 (erroronline.one)

''')

DEFAULTJSON = {
    "proxylists": [{
        "url": [
            "https://free-proxy-list.net/"
        ],
        "pattern": "([\\d\\.]+):(\\d+)\\n"
    }],
    "useragents": [{
        "url": [
            "https://developers.whatismybrowser.com/useragents/explore/software_type_specific/web-browser/"
        ],
        "pattern": "<td class=\\\"useragent\\\".+?>(.+?)</a>"
    }],
    "fallback": {
        "useragents": ["Mozilla/5.0 CK={} (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko", "Mozilla/5.0 (iPhone; CPU iPhone OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36", "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36", "Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148"]
    },
    "timeout": 10
}

HELPTEXT= '''
[help]

    this program serves to automatically send requests to a given url through different proxies. it is best
    used from the command line to have access to further options. this is not ai, you'll have to analyze the
    probably inhomogeneous sources by yourself beforehand in order to set up. 

    usage: proxyping [ -h | --help ]           this message, priority handling
                     [ -r | --reset ]          writes default setup file if not already exists, priority handling
                     [ -e | --error]           logs connection errors to file
                     [ -l | --limit ] NUMBER   limit attempts irrespective of found proxies
                     URL                       url to ping

    setup is specified in proxyping.json as following:

''' + json.dumps(DEFAULTJSON, indent = 4) + '''

    * set up any proxy sources with optional multiple urls and respective pattern to retrieve ip and port
    * set up any user-agent sources with optional multiple urls and respective pattern to retrieve ip and port
      to trick source servers that don't play well with requests not coming from a browser
    * define some fallback user-agents headers for the same reason
    * define timeout in seconds while not retrieving sourcecode from sites, must not be 0

    every request will be made through another proxies ip with a random user-agent

    extend whole dictionaries/objects if multiple subsites demand different patterns
'''

# set globals
STOPANIMATION = False 				# setter to start/stop working variable
TERMINALWIDTH, terminalheight = shutil.get_terminal_size(0)
terminalheight = 'linter, please ignore unused ' + str(terminalheight)
USERAGENTS = [] 					# initialize as global varibale
LOGFILE = False 					# initialize as global varibale

#                           _   ___             _   _
#   ___ ___ ___ ___ ___ ___| | |  _|_ _ ___ ___| |_|_|___ ___ ___
#  | . | -_|   | -_|  _| .'| | |  _| | |   |  _|  _| | . |   |_ -|
#  |_  |___|_|_|___|_| |__,|_| |_| |___|_|_|___|_| |_|___|_|_|___|
#  |___|
#

# log routine writing to file and terminal
def log(msg):
	if LOGFILE:
		LOGFILE.write( msg + '\n' )

# create sample setup file if necessary and not existing
def reset():
	try:
		with open('proxyping.json', 'x', newline = '', encoding = 'utf8') as file:
			json.dump(DEFAULTJSON, file, ensure_ascii = False, indent = 4)
		fprint('[*]  setting file proxyping.json successfully written. please accommodate to your environment.\n')
	except:
		fprint('[~]  proxyping.json could not be written because it already existed. please contact devops.\n')

# fancy anmiation to show something's going on
def animationbar():
	for c in itertools.cycle(['.   ', '..  ', '... ', '....', ' ...', '  ..', '   .']):
		if not STOPANIMATION:
			sys.stdout.write('\r' + c)
			sys.stdout.flush()
			time.sleep(0.1)
		else:
			time.sleep(1)

# like print but optionally clears loading bar animation beforehand
def fprint(*args, clearanimation = False, newline = True):
	if type(clearanimation) is str:
		sys.stdout.write( '\r' + clearanimation + ' ' * (4 - len(clearanimation) ))
	elif clearanimation:
		sys.stdout.write( '\r    ' )
	msg = ''
	for a in args:
		msg += str( a )
	sys.stdout.write( ('\n' if newline else '') + '\r' + msg  + ' ' * (TERMINALWIDTH - len(msg) - 1) )
	sys.stdout.flush()
	return msg

# create session
def get_session(proxy = False):
	# construct an HTTP session
	session = requests.Session()
	if proxy:
		# set os environment proxies. works for the runtime of the script, has not to be un- or reset
		os.environ['http_proxy'] = proxy[0] + ":" + proxy[1]
		os.environ['https_proxy'] = proxy[0] + ":" + proxy[1]
		# make session to use proxy
		session.proxies = {"http": proxy[0] + ":" + proxy[1], "https": proxy[0] + ":" + proxy[1]}
	return session

# retrieve source code from site
def get_source( link, proxy = False ):
	useragent = False
	if len(USERAGENTS):
		useragent = { "User-Agent": random.choice(USERAGENTS) }
	try:
		session = get_session(proxy)
		returned = session.get( link, headers = useragent, timeout = SETTINGS['timeout'] )
		if returned.status_code == 200:
			return (returned.text)
		else:
			log( '[~]  invalid response received by {0}\n'.format(link))
	except Exception as e:
		log( '[~]  error: {0}\n     used proxy and user agent: {1}\n     {2}\n'.format(e, proxy, useragent))
	return False

#analyze sourcecode and create list according to pattern matches
def analyze(src):
	result = []
	for url in src['url']:
		try:
			ressource = get_source( url )
			matches = re.findall(src['pattern'], ressource, re.IGNORECASE | re.DOTALL)
		except:
			continue
		for match in matches:
			if isinstance(match, tuple):
				#make tuples an array
				match = list(match)
			if match not in result:
				result.append( match )
	return result

#             _       ___             _   _
#   _____ ___|_|___  |  _|_ _ ___ ___| |_|_|___ ___
#  |     | .'| |   | |  _| | |   |  _|  _| | . |   |
#  |_|_|_|__,|_|_|_| |_| |___|_|_|___|_| |_|___|_|_|
#
#
def main(link, limit):
	global STOPANIMATION
	global USERAGENTS
	animation = threading.Thread(target=animationbar)
	animation.daemon = True
	animation.start()

	fprint('[!]  starting analysis of sources to obtain proxies. please stand by.', clearanimation = True)
	for index, proxysite in enumerate(SETTINGS['proxylists']):
		fprint('     analyzing source ' + str(index + 1) + ' of ' + str(len(SETTINGS['proxylists'])), clearanimation = '[!]')
		PROXYLIST = analyze(proxysite)

	fprint('[!]  starting analysis of sources to obtain user agents. please stand by.')
	for index, uasite in enumerate(SETTINGS['useragents']):
		fprint('     analyzing source ' + str(index + 1) + ' of ' + str(len(SETTINGS['useragents'])), clearanimation = '[!]')
		USERAGENTS = analyze(uasite)

	STOPANIMATION=True
	fprint( '[*]  approximately {0} proxies and {1} user agents were found.'.format(len(PROXYLIST), len(USERAGENTS)) )
	if not len(USERAGENTS):
		fprint( '[!]  since no user agents were found, settings fallback options will be used.' )
		USERAGENTS=SETTINGS['fallback']['useragents']

	confirm = input('\n[?]  do you want to ping ' + link + ' now?\n     type "y" to proceed, "h" for help, nothing or any other key to abort: ')
	if confirm == 'y':
		STOPANIMATION = False
		success = 0
		for i, n in enumerate(PROXYLIST):
			if type(limit) == int and i > limit - 1:
				break
			fprint('     ping ' + str(i + 1) + ' of ' + str(limit or len(PROXYLIST)), newline = False)
			if type(get_source( link, list(n) )) == str:
				success += 1
		log(fprint('[*]  {0} successful attempts.'.format(success)))

	elif confirm == 'h':
		print (HELPTEXT)
	STOPANIMATION = True

#   _     _ _   _     _ _
#  |_|___|_| |_|_|___| |_|___ ___
#  | |   | |  _| | .'| | |- _| -_|
#  |_|_|_|_|_| |_|__,|_|_|___|___|
#
#
# #load settings
try:
	with open('proxyping.json', 'r') as jsonfile:
		SETTINGS = json.loads(jsonfile.read().replace('\n', ''))
except:
	fprint('[~] settings could not be loaded, see help for syntax...')
	SETTINGS = False

if __name__ == '__main__':
	#argument handler	
	# omit first argument (scriptname)
	sys.argv.pop(0)
	#options actually ordered by importance
	confirm = False
	limit = False
	options = {	'h':'--help|-h',
				'r':'--reset|-r',
				'e':'--error|-e',
				'l': '((?:--limit|-l)[:\\s]+)([^\\s]+)*',
				}
	params = ' '.join(sys.argv) + ' '
	for opt in options:
		arg = re.findall(options[opt], params, re.IGNORECASE)
		if opt == 'h' and arg:
			confirm = 'h'
			break
		elif opt == 'r' and arg:
			confirm = 'r'
			break
		elif opt == 'e' and arg:
			#init logfile, write session start and parameters for backtracking
			LOGFILE=open('proxyping.log', 'a')
			LOGFILE.write('\n\nsession on ' + datetime.now().strftime('%Y-%m-%d %H:%M') + ' started with >' + ' '.join(sys.argv) + '\n')
			params = params.replace(''.join(arg[0]), '')
		elif opt == 'l' and arg:
			try:
				limit = int(arg[0][1])
				params = params.replace(''.join(arg[0]), '')
			except:
				fprint('     given --limit is not a decimal value! instead of ignoring value is set to zero.')
				limit = 0
		else:
			pass

	#auto help if no source file is found
	if confirm == 'r':
		reset()
	elif not SETTINGS or confirm == 'h':
		print (HELPTEXT)
	else:
		link=params.strip()
		main(link, limit)

	if LOGFILE:
		LOGFILE.write('session properly terminated on ' + datetime.now().strftime('%Y-%m-%d %H:%M'))
		LOGFILE.close()
	input('\n\r[?]  press enter to quit...')
	sys.exit()