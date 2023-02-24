'''
backup script copies all subfolders and files but excluded if not existant or newer
'''
import os
import shutil

src = {
	"startDir": "C:/Users/dev/Documents",
	"excludeDir": [".git", "__pycache__", 'build', 'dist', "Eigene Videos", "Eigene Musik", "Dell"]
	}
dst = {
	"startDir": "//192.168.178.26/Public/doc/dev",
	"excludeDir": ["ancient"]
	}

def _tree(curdir, exclude):
	curdir = os.path.normpath(curdir)
	result={curdir:{}}
	try:
		directory = os.scandir(curdir)
		for file in directory:
			if not file.name in exclude and file.is_dir():
				nextdir = os.path.normpath(os.path.join(curdir, file.name))
				result.update(_tree(nextdir, exclude))
			elif file.is_file():
				result[curdir][file.name] = file.stat().st_mtime
	except Exception as access_denied:
		print (access_denied)
	return result

def _copy(origin, backup):
	for originfolder in origin:
		backupfolder = originfolder.replace(list(origin)[0], list(backup)[0])
		for file in origin[originfolder]:
			if not backupfolder in backup:
				os.makedirs(backupfolder, exist_ok=True)
			if not backupfolder in backup or not file in backup[backupfolder] or origin[originfolder][file] > backup[backupfolder][file]: # touchwise
				print('[*] copying', os.path.join(originfolder, file))
				shutil.copy2(os.path.join(originfolder, file), os.path.join(backupfolder, file))

if __name__ == '__main__':
	local = _tree(src['startDir'], src['excludeDir'])
	remote = _tree(dst['startDir'], dst['excludeDir'])
	_copy(local, remote)
