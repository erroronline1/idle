# idle

these are some of my quite useful scripts (to me) to actually automate recurring tasks.
some of them come from first doodles with the language but evolved to decent tools.

## anarchychat
a stupid little chat where one script handles everything without the necessity of a server script - hence the name. basically you only need to define a shared location for the sqlite-database-file (yeah, i was quite optimistic about that in the beginning). if you store this within a network-folder, e.g. an nas-drive, everyone within the local network is able to participate in the chat. the script itself can be stored in the same place for everyone to access via shortcut for easier maintaining, or be used decentralized. this originated from restricting online-access for the kids rendering messenger services useless after the timeout. using this network-chat it might still be possible to reach out. sure - i could just go upstairs and talk to them though, but like any proper programmer i'd rather spend several days on developing a cumbersome solution to save a few minutes...

all entries above the dblimit will be deleted. some commands might affect every user. notifications on new messages from other users are implemented windows-specific. there is a stupid little bot helping with mental calculation...

### issues:
* it was a wild ride experiencing and trying to handle troubles using sqlite via network until i found [ressources about that topic](https://www.sqlite.org/useovernet.html). after all it is stated, that sqlite may not be suitable for this kind of usecase without a server handling the in- and output. there might/will be errors due to competing database insertions and locked database on connection issues.
* using fritz.nas is a major problem for slow fritz letting the application freeze, having to delete the db-file and still having to wait several minutes to start over again. however on a wd-mycloud-nas it works more reliable even on connection loss and doesn't seem to have the necessity to delete the database. can still remain unlocked for some minutes though.
* once in a while the toast-messages go rogue. it might be necessary to reboot...

works quite reasonably in vsc-console and cmd as a py-script on a stable connection. not quite in idle and powershell though.

well, just because you could doesn't mean you should, but it was fun. at least i learned a bit about sqlite, threading and exceptions while handling the deficiencies. absolute win.

## backup
i had a medium inconvenience trying to backup. the flashdrive died and of course i hadn't saved everything as i should have. since i am not aware of clever backup options on windows i considered writing something that is hopefully a bit more efficient by only copying non existant files and overwriting only files with a newer timestamp.
configure the local and the remote directory and occasionally define directories to exclude (like .git, __pycache__, etc.).

## circular_gallifreyan_unicode
simplified translation from latin characters to unicode representation of circular gallifreyan

gallifreyan is based on television series doctor who by bbc, translation is based on [loren shermans alphabet of circular gallifreyan](http://shermansplanet.com/gallifreyan/guide.pdf)

conversion of phonetic c for english only. platform related unicode inconsistencies though.

## circular_gallifreyan
same as above but with graphical output. favoured grouping of characters still in console. inspired by, redone and extended in javascript for [mightyfrongs gallifreyan translation helper](https://github.com/Mightyfrong/gallifreyan-translation-helper) with a bit of participation by myself.

## g_code_music
the other day i reinvented the wheel. figured out pretty fast others had before. was still fun to write something that generates a g-code to play music with non silent stepper motors on a 3d-printer.
the extruder moves to x50 y50 z5 after homing on start so it has a security offset. also the head moves about 20mm maximum (depending on the notes length) to x or y so it should work on almost any fdm-printer, given no silent stepper are built in.

## imgresize
automated resizing of images within the calling directory, optional including its subdirectiories to given nesting. useful for preparing blog content or releasing storage space retrospectively after everyone forgot to set the cameras to NOT maximum resolution. recently with optional terminal parameters.

## leech
serves to automatically download files according to linked ressources on websites. it is best used from the command line to have access to further options. this is not ai, you'll have to analyze the inhomogeneous sources by yourself beforehand in order to set up. see help for setup syntax.

leech does support the use of a proxy. urllib does have issues if the proxy-configuration is the same for http and https though. but who does this beside my company anyway? handling custom or root certificates is still on my maybe-later-list. 

## proxyping
this proof-of-concept retrieves lists of proxies and user-agents by pattern matching given websites. then it calls the specified url using the list of proxies and random user-agents. the proxies from the samples are not very reliable on connection or might need longer timeouts resulting in elongated runtime of the script. but it is quite dynamic.

## rename
rename all files in specified folder. choose if you want to rename all the same (as in file(0).mp3, file(1).mp3, ...), strip parts of filenames (as in file_1_security_copy.mp3, file_2_security_copy.mp3, ...), add something before overwriting while copying into folder (as in file_1_a.mp3, file_2_a.mp3, file_3_a.mp3)

## ruler
creates a background image with scale, spirals and areas according to the devices resolution

## stupidbot
serves as an addition to the anarchychat. split codebase for easier maintaining.
easy-to-implement and expendable skills beside generic responses. language according to passed current language from the chat itself.

## t2aa
text-2-ascii-art can be used from the command line. found it to be useful for structuring and commenting code.

## webcam
captures a webcam image, stores and uploads to webserver at a configurable interval. low traffic but still possible to watch your printer running out of filament. i don't have money for a raspberry pi...