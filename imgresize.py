from PIL import Image, ExifTags
import os
import sys
import re
from datetime import datetime

# set globals
CURDIR = os.getcwd()
DIRTREE = [CURDIR] # result list of directories
MAXSIZE = 1920 # default value of maximum pixel dimesion 
NESTING = 0 # max level of directory nesting, no subdirectories by default
REPLACE = False
HELP = False

print ('''
 _                       _
|_|_____ ___ ___ ___ ___|_|___ ___
| |     | . |  _| -_|_ -| |- _| -_|
|_|_|_|_|_  |_| |___|___|_|___|___| build 20210305
        |___|

by error on line 1 (erroronline.one)

resizes all jpg and png files in the calling directory and its children (if given) that extend the maximum allowed dimension
you can paste the script in a top level directory and call it like 'py ../../imgresize.py' to process the current nested dir
terminal use for additional options

$ imgresize --help     for overview''')

HELPTEXT= '''
[help]

    this program resizes all jpg and png files in the calling directory and its children (if given) that extend the maximum allowed dimension
    files that are below the given dimension will be kept untouched
    
    usage: imgresize [ -h | --help ]       this message, priority handling
                     [ -m | --max ]        set maximum size in pixel for longer side, {0} by default
                     [ -n | --nesting ]    set maximum nesting for processed subdirectories, {1} by default
                     [ -r | --replace ]    delete original files after processing

    processed files lose all metadata. original modified date will be added to the filename.

'''.format(MAXSIZE, NESTING)

def tree(curdir, nesting):
	dir = os.listdir(curdir)
	nesting -= 1
	for file in dir:
		if nesting > 0:
			if file.find('.') < 1:
				DIRTREE.append(curdir + "\\" + file)
				tree(curdir + "\\" + file, nesting)

def resize(curdir):
	dir = os.listdir(curdir)
	for file in dir:
		if file.find('.') < 1:
			continue
		name = file[0:file.rindex('.')]
		extension = file[file.rindex('.'):].lower()
		mtime = os.path.getmtime(file)

		if extension in ('.jpg', '.png'):
			img = Image.open(file)
			try:
				for orientation in ExifTags.TAGS.keys():
					if ExifTags.TAGS[orientation] == 'Orientation':
						break
				exif = dict(img._getexif().items())

				if exif[orientation] == 3:
					img=img.rotate(180, expand = True)
				elif exif[orientation] == 6:
					img=img.rotate(270, expand = True)
				elif exif[orientation] == 8:
					img=img.rotate(90, expand = True)
			except (AttributeError, KeyError, IndexError):
				# cases: image don't have getexif
				pass

			owidth = img.size[0]
			oheight = img.size[1]
			if owidth > MAXSIZE or oheight > MAXSIZE:
				if owidth >= oheight:
					height = round(MAXSIZE * oheight / owidth)
					width = MAXSIZE
				else:
					width = round(MAXSIZE * owidth / oheight)
					height = MAXSIZE
				img = img.resize((width, height), Image.ANTIALIAS)
				newname = '{0}_{1}x{2}_{3}{4}'.format(name, width, height, datetime.utcfromtimestamp(mtime).strftime('%Y%m%d') , extension)
				img.save(newname)
				if REPLACE:
					os.unlink(file)
				img.close()

#   _     _ _   _     _ _
#  |_|___|_| |_|_|___| |_|___ ___
#  | |   | |  _| | .'| | |- _| -_|
#  |_|_|_|_|_| |_|__,|_|_|___|___|
#

if __name__ == '__main__':
	# argument handler
	# omit first argument (scriptname)
	sys.argv.pop(0)
	# find and assign option arguments
	options = {
		'h': '--help|-h',
		'm': '((?:--max|-m)[:\\s]+)(\\d+)',
		'n': '((?:--nesting|-n)[:\\s]+)(\\d+)',
		'r': '--replace|-r'
		}
	params = ' '.join(sys.argv) + ' '
	for opt in options:
		arg = re.findall(options[opt], params, re.IGNORECASE)
		if opt == 'h' and arg:
			HELP=True
			break
		elif opt == 'm' and bool(arg):
			# not less than 1, default otherwise
			MAXSIZE = int(arg[0][1]) if int(arg[0][1]) > 0 else MAXSIZE
			params = params.replace(''.join(arg[0]), '')
		elif opt == 'n' and bool(arg):
			# not less than 1, default otherwise
			NESTING = int(arg[0][1]) if int(arg[0][1]) > 0 else NESTING
			params = params.replace(''.join(arg[0]), '')
		elif opt == 'r' and arg:
			REPLACE = True
			params = params.replace(''.join(arg[0]), '')

	if HELP:
		print (HELPTEXT)
	else: 
		confirmation=str(input('\n\nall images in directory "' + CURDIR + '"' + (' and its {0}.-level nested subdirectories'.format(NESTING) if NESTING else '') + ' will be resized to ' + str(MAXSIZE) + 'px maximum width or height! [ y / n ]: ')).lower()
		if confirmation == 'y':
			tree(CURDIR, NESTING + 1)
			for dir in DIRTREE:
				resize(dir)

	sys.exit()