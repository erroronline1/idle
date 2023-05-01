'''
upload image from webcam to webserver
'''
import os
import sys
from pathlib import Path
import threading
import time
import json
import cv2
import pysftp
import noyb # contains nothing of your business ;)

TERMINALWIDTH = os.get_terminal_size().columns

class Webcam:
	'''initilizes a webcam image, stores to local and uploads the image to a webserver'''
	setup: dict = {
		'cam': 0,
		'rotate': None,
		'refresh': 5,
		'upload': True,
		'homedir': os.path.normpath(Path.home().joinpath('pywebcam.jpg')),
		'remotedir':'/',
		'ftpcredentials': noyb.ftpcredentials, # {'host':'', 'username':'', 'password':'', 'port':22}
	}
	frame = None
	ret = None
	camera = None

	def __init__(self, setup: dict = None):
		if setup:
			self.setup.update(setup)

	def upload(self, credentials: dict, remotedir: str, homedir: str) -> str:
		'''actually upload image to websever via ftp'''
		if self.setup['upload']:
			try:
				with pysftp.Connection(**credentials) as sftp:
					with sftp.cd(remotedir):
						sftp.put(homedir)
				return f"[*] sucessfully uploaded file on {time.ctime(time.time())}"
			except Exception as error:
				return f"[X] could not upload file: {error}"

	def upload_daemon(self) -> None:
		'''save img locally and upload to webserver'''
		while True:
			if self.ret:
				cv2.imwrite(self.setup['homedir'], self.frame)
				self.msg(self.upload(self.setup['ftpcredentials'], self.setup['remotedir'], self.setup['homedir']))
			time.sleep(self.setup['refresh'])

	def goodbye_upload(self) -> None:
		'''uploads last image with offline note on regular exit'''
		goodbye = cv2.imread(self.setup['homedir'])
		goodbye = cv2.putText(goodbye, 'offline', (50,75), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3, cv2.LINE_AA)
		cv2.imwrite(self.setup['homedir'], goodbye)
		self.upload(self.setup['ftpcredentials'], self.setup['remotedir'], self.setup['homedir'])


	def camera_handler(self) -> bool:
		'''displays camera picture or returns loss of camera'''
		while True:
			self.ret, self.frame = self.camera.read()
			if self.ret:
				if self.setup['rotate']:
					self.frame = cv2.rotate(self.frame, self.setup['rotate'])
				cv2.imshow(f'webcam refresh @{self.setup["refresh"]} seconds, press q to quit', self.frame)
			else:
				self.camera.release()
				return False
			if cv2.waitKey(1) & 0xFF == ord('q'):
				break
		return True

	def start(self) -> None:
		'''launch upload daemon, start capturing and reconnect camera on loss'''
		if self.setup['upload']:
			upload = threading.Thread(target=self.upload_daemon)
			upload.daemon = True
			upload.start()

		while True:
			self.camera = cv2.VideoCapture(self.setup['cam'])
			if self.camera.isOpened():
				cam.msg(f"[*] cam {cam.setup['cam']} ready.\n")
				if not self.camera_handler():
					time.sleep(self.setup['refresh'])
					continue
				break
			self.camera.release()
			time.sleep(self.setup['refresh'])
			continue
		self.stop()

	def stop(self) -> None:
		'''release and destroy window'''
		self.camera.release()
		cv2.destroyAllWindows()
		self.goodbye_upload()

	def available_cameras(self) -> None:
		'''list available camera indices'''
		for index in range(-2, 11):
			cap = cv2.VideoCapture(index)
			if cap.read()[0]:
				self.msg(f'[*] camera {index} is available\n')
				cap.release()
				continue
			self.msg(f'[X] camera {index} is not available\n')

	def msg(self, msg) -> None:
		'''status to terminal'''
		clear = (" " * (TERMINALWIDTH - len(msg) - 1)) if msg[-1] != '\n' else ''
		sys.stdout.write( f'\r{msg}{clear}' )
		sys.stdout.flush()

if __name__=="__main__":
	cam: Webcam = Webcam({
		'cam': 1,
   		'rotate':cv2.ROTATE_180, #cv2.ROTATE_90_COUNTERCLOCKWISE, cv2.ROTATE_180
		#'upload': False # false for positioning setup without looking within the code where to disable...
	})

	cam.msg(f"[!] launching cam {cam.setup['cam']}. current settings are:\n{json.dumps(cam.setup, indent=4)}\n")
	cam.start()
