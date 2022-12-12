import argparse
import platform
import pathlib
import sys
sys.path.append(str(pathlib.Path(__file__).parent.resolve())[0:len(str(pathlib.Path(__file__).parent.resolve()))-5])
import lib.cope2

if platform.system() == 'Linux' or platform.system() == 'Darwin': # color initalization for linux/macos, wont work on windows
    red,bold,dim,reset,errorBG,debugBG='\033[00;31m', '\033[01m', '\033[02m', '\033[0m', '\033[41;30;01m', '\033[47;30;02m'
else:
    red,green,bold,dim,reset,errorBG,debugBG=''

def printError(text):
    print(errorBG + "[ERROR]" + reset + " " + text)
    
def printVerbose(text):
    print(debugBG + "[DEBUG]" + reset + dim + " " + text + reset) if args.verbose else None

parser = argparse.ArgumentParser(description='Encode a string using COPE².')
parser.add_argument('input', type=str)
parser.add_argument('-o', '--output', type=str, help='Output file to write to. If not specified, output will be written to stdout. File will be appended to if it already exists.', metavar = 'out')
parser.add_argument('-c', '--compile', action='store_true', help='Compile a provided Python file.')
parser.add_argument('-O', '--offset', type=int, default=128, help='Offset for decoding engine. Universal default is 128. You probably don\'t need to change this.', metavar = '128')
parser.add_argument('-p', '--pagesize', type=int, default=2, help='Page size for decoding engine. Universal default is 2. You probably don\'t need to change this.', metavar = '8')
parser.add_argument('-V', '--verbose', action='store_true', help='Print verbose output.')
parser.add_argument('-v', '--version', action='version', version='Written by Garret Stand on 10 December 2022 :)')

print('🔐 \033[32;01mCOPE²\033[00;32m Encoder\033[0m')
args = parser.parse_args()

if args.compile:
    try:
        with open(args.input, 'r') as f:
            toencode = f.read()
    except (FileNotFoundError, IOError, OSError, UnicodeDecodeError) as e:
        printError('Input file does not exist, is not a text file, or is otherwise corrupted/broken. Check your path. Exiting...')
        exit()
else:
    toenecode = args.input

encoded_structure = lib.cope2.encode(toencode, args.offset, args.pagesize)
encoded = encoded_structure[0] if not args.compile else lib.cope2.compile(toencode, encoded_structure[1], encoded_structure[2])

if encoded_structure[3] == True:
    printError('Your provided offset/pagesize was determined to be unsafe. The maximum possible offset (%i) and the lowest possible page size (%i) were used instead.' % (encoded_structure[1], encoded_structure[2]))

if args.output:
    try:
        with open(args.output, 'w') as f:
            f.write(encoded)
    except FileNotFoundError:
        try:
            with open(args.output, 'w+') as f:
                f.write(encoded)
        except (IOError, OSError) as e:
            printError('Input was encoded, but cannot output to declared file. Check your path.')
            printError('Do you want to print the encoded string to stdout? (y/N)')
            if input().lower() == 'y':
                print(encoded)        
            exit()
    print(bold + "Success!" + reset + " Encoded string written to " + args.output)
else:
    print(bold + "Success!" + reset + " Encoded string:\n\n" + encoded)