'''
 _   ___
| |_|_  |___ ___   ___ _ _
|  _|  _| .'| .'|_| . | | |
|_| |___|__,|__,|_|  _|_  |
                  |_| |___|

text to ascii-art
inspired by http://www.patorjk.com/software/taag/

python version with cli options by error on line 1 (erroronline.one)
offline usable with your favourite font

currently lowercase only but with optional linebreak
if you want to add uppercase extend the font-dictionaries and change the
string = string.lower() on line 80something

$ python t2aa.py --help    for overview
'''


availablefonts={
    'rectangle':{ # rectangle font borrowed from http://www.patorjk.com/software/taag/
        'index':    [' ',   'a',      'b',    'c',    'd',    'e',    'f',    'g',    'h',  'i',   'j',     'k',  'l',    'm',     'n',    'o',    'p',    'q',    'r',    's',    't',    'u',    'v',     'w',     'x',    'y',    'z',     'ä',    'ö',    'ü',    'ß',      '1',      '2',    '3',   '4',    '5',    '6',    '7',    '8',    '9',    '0',   ',',  ';',  '.',  ':',   '-',     '_',        '#',    "'",    '+',      '*',      '~',       '^',    '!',   '"',    '$',       '%',       '&',    '/',    '(',    ')',    '=',        '?',    '{',      '[',    ']',    '}',      '\\',    '<',      '>',       '|'],
        'lines':   [['   ','     ','     ','     ','     ','     ','     ','     ','     ','   ','     ','     ','   ','       ','     ','     ','     ','     ','     ','     ','     ','     ','     ', '       ','     ','     ','     ',' _ _ ',' _ _ ',' _ _ ','       ','       ','     ','     ','     ','     ','     ','     ','     ','     ','     ','   ','   ','   ','   ','     ','       ','   _ _   ',' _ ','       ','       ',' _____ ',' _____ ',' __ ',' _ _ ','   _   ','       ','   _   ','     ','   _ ',' _   ','       ',' _____ ','   ___ ',' ___ ',' ___ ',' ___   ','     ',  '   __',  '__   ',  ' _ '],
                    ['   ','     ',' _   ','     ','   _ ','     ',' ___ ','     ',' _   ',' _ ','   _ ',' _   ',' _ ','       ','     ','     ','     ','     ','     ','     ',' _   ','     ','     ', '       ','     ','     ','     ','|_|_|','|_|_|','|_|_|',' _____ ',' ___   ',' ___ ',' ___ ',' ___ ',' ___ ',' ___ ',' ___ ',' ___ ',' ___ ',' ___ ','   ',' _ ','   ',' _ ','     ','       ',' _| | |_ ','| |','   _   ',' _____ ','|   | |','|  _  |','|  |','| | |',' _| |_ ',' __ __ ',' _| |_ ','   _ ',' _|_|','|_|_ ','       ','|___  |','  |  _|','|  _|','|_  |','|_  |  ',' _   ',  '  / /',  '\\ \\  ','| |'],
                    ['   ',' ___ ','| |_ ',' ___ ',' _| |',' ___ ','|  _|',' ___ ','| |_ ','|_|','  |_|','| |_ ','| |',' _____ ',' ___ ',' ___ ',' ___ ',' ___ ',' ___ ',' ___ ','| |_ ',' _ _ ',' _ _ ', ' _ _ _ ',' _ _ ',' _ _ ',' ___ ',' ___ ',' ___ ',' _ _ ','| __  |','|_  |  ','|_  |','|_  |','| | |','|  _|','|  _|','|_  |','| . |','| . |','|   |','   ','|_|','   ','|_|',' ___ ','       ','|_     _|','|_|',' _| |_ ','| | | |','|_|___|','|_| |_|','|  |','|_|_|','|   __|','|__|  |','|   __|','  / |','| |  ','  | |',' _____ ','  |  _|',' _| |  ','| |  ','  | |','  | |_ ','| \\  ', ' / / ',  ' \\ \\ ','| |'],
                    ['   ',"| .'|",'| . |','|  _|','| . |','| -_|','|  _|','| . |','|   |','| |','  | |',"| '_|",'| |','|     |','|   |','| . |','| . |','| . |','|  _|','|_ -|','|  _|','| | |','| | |', '| | | |',"|_'_|",'| | |','|- _|',"| .'|",'| . |','| | |','| __ -|',' _| |_ ','|  _|','|_  |','|_  |','|_  |','| . |','  | |','| . |','|_  |','| | |',' _ ',' _ ',' _ ',' _ ','|___|','       ','|_     _|','   ','|_   _|','|-   -|','       ','       ','|__|','     ','|__   |','|   __|','|   __|',' / / ','| |  ','  | |','|_____|','  |_|  ','|_  |  ','| |  ','  | |','  |  _|',' \\ \\ ','< <  ',  '  > >',  '| |'],
                    ['   ','|__,|','|___|','|___|','|___|','|___|','|_|  ','|_  |','|_|_|','|_|',' _| |','|_,_|','|_|','|_|_|_|','|_|_|','|___|','|  _|','|_  |','|_|  ','|___|','|_|  ','|___|',' \\_/ ','|_____|','|_,_|','|_  |','|___|','|__,|','|___|','|___|','|  ___|','|_____|','|___|','|___|','  |_|','|___|','|___|','  |_|','|___|','|___|','|___|','| |','| |','|_|','|_|','     ',' _____ ','  |_|_|  ','   ','  |_|  ','|_|_|_|','       ','       ','|__|','     ','|_   _|','|__|__|','|_   _|','|_/  ','|_|_ ',' _|_|','|_____|','  |_|  ','  | |_ ','| |_ ',' _| |',' _| |  ','  \\_|', ' \\ \\ ',' / / ',  '| |'],
                    ['   ','     ','     ','     ','     ','     ','     ','|___|','     ','   ','|___|','     ','   ','       ','     ','     ','|_|  ','  |_|','     ','     ','     ','     ','     ', '       ','     ','|___|','     ','     ','     ','     ','|_|    ','       ','     ','     ','     ','     ','     ','     ','     ','     ','     ','|_|','|_|','   ','   ','     ','|_____|','         ','   ','       ','       ','       ','       ','    ','     ','  |_|  ','       ','  |_|  ','     ','  |_|','|_|  ','       ','       ','  |___|','|___|','|___|','|___|  ','     ',  '  \\_\\','/_/  ',  '|_|']]
    },
    'big':{ # big font borrowed from http://www.patorjk.com/software/taag/
        'index':    [' ',     'a',        'b',      'c',       'd',      'e',     'f',     'g',      'h',     'i',   'j',     'k',      'l',       'm',         'n',       'o',     'p',        'q',     'r',      's',     't',      'u',         'v',          'w',         'x',       'y',     'z',     'ä',       'ö',        'ü',      'ß',      '1',    '2',      '3',        '4',      '5',        '6',       '7',       '8',     '9',        '0',     ',',  ';',  '.',  ':',     '-',      '_',        '#',      "'",    '+',        '*',       '~',    '^',    '!',   '"',    '$',       '%',       '&',       '/',     '(',     ')',        '=',      '?',      '{',     '[',    ']',    '}',     '\\',         '<',       '>',   '|'],
        'lines':   [['   ','       ', ' _     ', '      ', '     _ ', '      ', '  __ ','       ', ' _     ', ' _ ','   _ ',' _    ',  ' _ ','           ', '       ', '       ', '       ', '       ', '      ','     ',  ' _   ', '       ', '       ',  '          ',   '      ',  '       ', '     ',' _   _ ', ' _   _ ', ' _   _ ', '  ___  ', ' __ ',' ___  ', ' ____  ', ' _  _   ',' _____ ', '   __  ',' ______ ','  ___  ', '  ___  ', '  ___  ', '   ','   ','   ','   ','        ','        ','   _  _   ',' _ ','       ','    _    ',  ' /\\/|',' /\\ ',' _ ',' _ _ ','  _  ',  ' _   __','        ',  '     __','  __',  '__  ',  '        ',' ___  ', '   __',  ' ___ ',' ___ ','__   ',  '__     ',  '   __',  '__   ',  ' _ '],
                    ['   ','       ', '| |    ', '      ', '    | |', '      ', ' / _|','       ', '| |    ', '(_)','  (_)','| |   ',  '| |','           ', '       ', '       ', '       ', '       ', '      ','     ',  '| |  ', '       ', '       ',  '          ',   '      ',  '       ', '     ','(_) (_)', '(_) (_)', '(_) (_)', ' / _ \\ ','/_ |','|__ \\ ','|___ \\ ','| || |  ','| ____|', '  / /  ','|____  |',' / _ \\ ',' / _ \\ ',' / _ \\ ','   ',' _ ','   ',' _ ','        ','        ',' _| || |_ ','( )','   _   ',' /\\| |/\\ ','|/\\/ ','|/\\|','| |','( | )',' | | ',  '(_) / /','  ___   ',  '    / /',' / /',  '\\ \\ ',' ______ ','|__ \\ ','  / /',  '|  _|','|_  |','\\ \\  ','\\ \\    ','  / /',  '\\ \\  ','| |'],
                    ['   ','  __ _ ', '| |__  ', '  ___ ', '  __| |', '  ___ ', '| |_ ','  __ _ ', '| |__  ', ' _ ','   _ ','| | __',  '| |',' _ __ ___  ', ' _ __  ', '  ___  ', ' _ __  ', '  __ _ ', ' _ __ ',' ___ ',  '| |_ ', ' _   _ ', '__   __',  '__      __',   '__  __',  ' _   _ ', ' ____','  __ _ ', '  ___  ', ' _   _ ', '| | ) |', ' | |','   ) |', '  __) |', '| || |_ ','| |__  ', ' / /_  ','    / / ','| (_) |', '| (_) |', '| | | |', '   ','(_)','   ','(_)',' ______ ','        ','|_  __  _|','|/ ',' _| |_ '," \\ ` ' / ", '     ', '    ', '| |',' V V ','/ __)',  '   / / ',' ( _ )  ',  '   / / ','| | ',  ' | |',  '|______|','   ) |', ' | | ',  '| |  ','  | |',' | | ',  ' \\ \\   ',' / / ',  ' \\ \\ ','| |'],
                    ['   ',' / _` |', "| '_ \\ ",' / __|', ' / _` |', ' / _ \\','|  _|',' / _` |', "| '_ \\ ",'| |','  | |','| |/ /',  '| |',"| '_ ` _ \\ ","| '_ \\ ",' / _ \\ ',"| '_ \\ ",' / _` |', "| '__|",'/ __|',  '| __|', '| | | |', '\\ \\ / /','\\ \\ /\\ / /','\\ \\/ /','| | | |', '|_  /',' / _` |', ' / _ \\ ','| | | |', '| |< < ', ' | |','  / / ', ' |__ < ', '|__   _|','|___ \\ ',"| '_ \\",'   / /  ',' > _ < ', ' \\__, |','| | | |', '   ','   ','   ','   ','|______|','        ',' _| || |_ ','   ','|_   _|','|_     _|',  '     ', '    ', '| |','     ','\\__ \\','  / /  ',' / _ \\/\\','  / /  ','| | ',  ' | |',  ' ______ ','  / / ', '/ /  ',  '| |  ','  | |','  \\ \\','  \\ \\  ','< <  ',  '  > >',  '| |'],
                    ['   ','| (_| |', '| |_) |', '| (__ ', '| (_| |', '|  __/', '| |  ','| (_| |', '| | | |', '| |','  | |','|   < ',  '| |','| | | | | |', '| | | |', '| (_) |', '| |_) |', '| (_| |', '| |   ','\\__ \\','| |_ ', '| |_| |', ' \\ V / ', ' \\ V  V / ',  ' >  < ',  '| |_| |', ' / / ','| (_| |', '| (_) |', '| |_| |', '| | ) |', ' | |',' / /_ ', ' ___) |', '   | |  ',' ___) |', '| (_) |','  / /   ','| (_) |', '   / / ', '| |_| |', ' _ ',' _ ',' _ ',' _ ','        ','        ','|_  __  _|','   ','  |_|  ',' / , . \\ ', '     ', '    ', '|_|','     ','(   /',  ' / / _ ','| (_>  <',  ' / /   ','| | ',  ' | |',  '|______|',' |_|  ', '\\ \\  ','| |  ','  | |','  / /',  '   \\ \\ ',' \\ \\ ',' / / ',  '| |'],
                    ['   ',' \\__,_|','|_.__/ ', ' \\___|',' \\__,_|',' \\___|','|_|  ',' \\__, |','|_| |_|', '|_|','  | |','|_|\\_\\','|_|','|_| |_| |_|', '|_| |_|', ' \\___/ ','| .__/ ', ' \\__, |','|_|   ','|___/',  ' \\__|',' \\__,_|','  \\_/  ', '  \\_/\\_/  ', '/_/\\_\\',' \\__, |','/___|',' \\__,_|',' \\___/ ',' \\__,_|','| ||_/ ', ' |_|','|____|', '|____/ ', '   |_|  ','|____/ ', ' \\___/',' /_/    ',' \\___/ ','  /_/  ', ' \\___/ ','( )','( )','(_)','(_)','        ','        ','  |_||_|  ','   ','       ',' \\/|_|\\/ ','     ', '    ', '(_)','     ',' |_| ',  '/_/ (_)',' \\___/\\/','/_/    ','| | ',  ' | |',  '        ',' (_)  ', ' | | ',  '| |_ ',' _| |',' | | ',  '    \\_\\','  \\_\\','/_/  ',  '| |'],
                    ['   ','       ', '       ', '      ', '       ', '      ', '     ','  __/ |', '       ', '   ',' _/ |','      ',  '   ','           ', '       ', '       ', '| |    ', '    | |', '      ','     ',  '     ', '       ', '       ',  '          ',   '      ',  '  __/ |', '     ','       ', '       ', '       ', '|_|    ', '    ','      ', '       ', '        ','       ', '       ','        ','       ', '       ', '       ', '|/ ','|/ ','   ','   ','        ',' ______ ','          ','   ','       ','         ',  '     ', '    ', '   ','     ','     ',  '       ','        ',  '       ',' \\_\\','/_/ ',  '        ','      ', '  \\_\\','|___|','|___|','/_/  ',  '       ',  '     ',  '     ',  '| |'],
                    ['   ','       ', '       ', '      ', '       ', '      ', '     ',' |___/ ', '       ', '   ','|__/ ','      ',  '   ','           ', '       ', '       ', '|_|    ', '    |_|', '      ','     ',  '     ', '       ', '       ',  '          ',   '      ',  ' |___/ ', '     ','       ', '       ', '       ', '       ', '    ','      ', '       ', '        ','       ', '       ','        ','       ', '       ', '       ', '   ','   ','   ','   ','        ','|______|','          ','   ','       ','         ',  '     ', '    ', '   ','     ','     ',  '       ','        ',  '       ','    ',  '    ',  '        ','      ', '     ',  '     ','     ','     ',  '       ',  '     ',  '     ',  '|_|']]
    }
}

import sys
import re
import shutil

letterspacing=0
font='rectangle'
autolinebreak=False
wordwrap=False
helpAndQuit=False

def helparg():
    global availablefonts
    samples=''
    for font in availablefonts:
        samples += 'fontname: ' + font + '\n'
        samples += 'available characters: ' + ''.join([c for c in availablefonts[font]['index']]) + '\n'
        samples += write(0, font, 'hello world!', True, True)
    print('''
usage: t2aa.py [ -h  | --help ]
               [ -f  | --font ] FONTNAME
               [ -ls | --letterspacing] NUMBER
               [ -lb | --linebreak]
               [ -ww | --wordwrap]

with font going default if FONTNAME not available and
letterspacing can not be less than -1, not readable otherwise
optional linebreak and wordwrap take terminal width into account.

extend available font dictionary as desired. currently available:\n
''' + samples)

def write(ls, font, string, autolinebreak, wordwrap):
    global availablefonts

    terminalwidth, terminalheight = shutil.get_terminal_size(0)
    terminalheight = 'linter, please ignore unused ' + str(terminalheight)

    # set up result from selected font
    output = []
    wrap=0
    string = string.lower()
    # separate words by whitespace
    chunks = re.findall(r'(.+?(?:\s|$))', string)

    for word in chunks:
        # quick assembly of word length to handle word wraps
        expectablelength=0
        for char in word:
            expectablelength += len(availablefonts[font]['lines'][0][availablefonts[font]['index'].index(char)]) + ls
        if wordwrap and len(output):
            if len(output[wrap][-1]) + expectablelength >= terminalwidth:
                wrap += 1
        if wrap+1 >= len(output):
            output.append([''] * len(availablefonts[font]['lines']))
        # add characters to output...
        for char in word:
            # ... linewise
            for lineindex, line in enumerate(availablefonts[font]['lines']):
                # get ascii-letter line
                append=line[availablefonts[font]['index'].index(char)]
                # handle letter spacing
                if len(output[wrap][lineindex]) > 0 and ls < 0:
                    if append[0] != ' ':
                        output[wrap][lineindex] = output[wrap][lineindex][:-1]
                    else:
                        append=append[1:]
                elif len(output[wrap][lineindex]) > 0 and ls > 0:
                        append = ' ' * ls + append
                # manage linebreaks
                if autolinebreak and len(output[wrap][lineindex] + append) >= terminalwidth:
                    wrap += 1
                    output.append([''] * len(availablefonts[font]['lines']))
                # append
                output[wrap][lineindex] += append

    # parse array to output string
    returnstring=''
    for wrap in output:
        returnstring += '\n'.join(wrap) + '\n'
    
    return returnstring

if __name__ == '__main__':
    # argument handler
    # omit first argument (scriptname)
    sys.argv.pop(0)
    # find and assign option arguments, strip arguments, remainder should be string
    options = {
        'h': '--help|-h',
        'ls': '((?:--letterspacing|-ls)[:\\s]+)(-{0,1}\\d+)',
        'f': '((?:--font|-f)[:\\s]+)([^\\s]+[\\w]+)*',
        'lb': '--linebreak|-lb',
        'ww': '--wordwrap|-ww'
        }
    params = ' '.join(sys.argv) + ' '
    for opt in options:
        arg = re.findall(options[opt], params, re.IGNORECASE)
        if opt == 'h' and arg:
            helpAndQuit=True
            break
        elif opt == 'ls' and bool(arg):
            # not less than -1, not readable otherwise
            letterspacing = int(arg[0][1]) if int(arg[0][1]) > -2 else -1
            params=params.replace(''.join(arg[0]), '')
        elif opt == 'f' and bool(arg):
            font = arg[0][1] if arg[0][1] in availablefonts else font
            params=params.replace(''.join(arg[0]), '')
        elif opt == 'lb' and arg:
            autolinebreak=True
            params=params.replace(''.join(arg[0]), '')
        elif opt == 'ww' and arg:
            wordwrap=True
            params=params.replace(''.join(arg[0]), '')

    string=params.strip() if len(params.strip()) else 'hello world!'

    if not helpAndQuit:
        print(write(letterspacing, font, string, autolinebreak, wordwrap))
    else:
        helparg()