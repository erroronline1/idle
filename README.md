# idle

these are some of my quite useful scripts (to me) to actually automate recurring tasks.
some of them come from first doodles with the language but evolved to decent tools.

### anarchychat
a stupid little chat where one script handles everything without the necessity of a server script - hence the name. basically you only need to define a shared location for the sqlite-database-file. if you store this within a network-folder, e.g. an nas-drive, everyone within the local network is able to participate in the chat. this originated from restricting online-access for the kids rendering messenger services useless after the timeout. using this chat-script it might still be possible to reach out. sure - i could just go upstairs and talk to them though, but like any proper programmer i'd rather spend several days on developing a cumbersome solution to save a few minutes...

this is by no means a bulletproof thing - yet. all entries above the DBLIMIT-count will be deleted. some commands might affect every user. notifications on new messages from other users are implemented windows-specific.

works quite well in vsc-console and cmd as a py-script. not quite in idle and powershell though. sometimes lines slip a bit.

### circular_gallifreyan_unicode
simplified translation from latin characters to unicode representation of circular gallifreyan

gallifreyan is based on television series doctor who by bbc, translation is based on [loren shermans alphabet of circular gallifreyan](http://shermansplanet.com/gallifreyan/guide.pdf)

conversion of phonetic c for english only. platform related unicode inconsistencies though.

### circular_gallifreyan
same as above but with graphical output. favoured grouping of characters still in console. inspired by, redone and extended in javascript for [mightyfrongs gallifreyan translation helper](https://github.com/Mightyfrong/gallifreyan-translation-helper) with a bit of participation by myself.

### imgresize
automated resizing of images within the calling directory, optional including its subdirectiories to given nesting. useful for preparing blog content or releasing storage space retrospectively after everyone forgot to set the cameras to NOT maximum resolution. recently with optional terminal parameters.

### leech
serves to automatically download files according to linked ressources on websites. it is best used from the command line to have access to further options. this is not ai, you'll have to analyze the inhomogeneous sources by yourself beforehand in order to set up. see help for setup syntax.

### proxyping
this proof-of-concept retrieves lists of proxies and user-agents by pattern matching given websites. then it calls the specified url using the list of proxies and random user-agents. the proxies from the samples are not very reliable on connection or might need longer timeouts resulting in elongated runtime of the script. but it is quite dynamic.

### rename
rename all files in specified folder. choose if you want to rename all the same (as in file(0).mp3, file(1).mp3, ...), strip parts of filenames (as in file_1_security_copy.mp3, file_2_security_copy.mp3, ...), add something before overwriting while copying into folder (as in file_1_a.mp3, file_2_a.mp3, file_3_a.mp3)

### ruler
creates a background image with scale, spirals and areas according to the devices resolution

### t2aa
text-2-ascii-art can be used from the command line. found it to be useful for structuring and commenting code.