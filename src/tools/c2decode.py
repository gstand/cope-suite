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

parser = argparse.ArgumentParser(description='Decode a COPE² encoded string.', epilog='It is assumed that any input is a valid COPE² encoded string. If you are passing a file to decompile, please use the -d/--decompile flag.')
parser.add_argument('input', type=str)
parser.add_argument('-d', '--decompile', action='store_true', help='Decompile a COPE² compiled Python file. This only works for files that have been compiled with the COPE Toolchain.')
parser.add_argument('-o', '--output', type=str, help='Output file to write to. If not specified, output will be written to stdout. File will be appended to if it already exists.', metavar = 'out')
parser.add_argument('-O', '--offset', type=int, default=128, help='Offset for decoding engine. Universal default is 128. You probably don\'t need to change this.', metavar = '128')
parser.add_argument('-p', '--pagesize', type=int, default=2, help='Page size for decoding engine. Universal default is 2. You probably don\'t need to change this.', metavar = '2')
parser.add_argument('-V', '--verbose', action='store_true', help='Print verbose output.')
parser.add_argument('-v', '--version', action='version', version='Written by Garret Stand on 10 December 2022 :)')

print('🔐 \033[32;01mCOPE²\033[00;32m Decoder\033[0m')
args = parser.parse_args()

if args.decompile:
    try:
        with open(args.input, 'r') as f:
            dataline = f.readline().strip('\n')
            try:
                exec(dataline)
                todecode = z1
            except:
                printError("Something went wrong fetching the hexstring. Ensure the input is a valid and unmodified COPE² compiled Python file.")
                exit(1)
    except (FileNotFoundError, IOError, OSError, UnicodeDecodeError) as e:
        printError('Input file does not exist, is not a text file, or is otherwise corrupted/broken. Check your path. Exiting...')
        exit(1)
else:
    todecode = args.input

printVerbose("data to decode: " + todecode)

try:
    int(todecode, 16)
except ValueError:
    printError('Input is not a valid COPE² encoded string. Exiting...') if not args.decompile else printError('Input is not a valid COPE² compiled Python file. Check the documentation for more information. Exiting...')
    exit(1)

decoded = lib.cope2.decode(todecode, args.offset, args.pagesize)

if args.output:
    try:
        with open(args.output, 'a') as f:
            f.write('\n' + decoded)
    except FileNotFoundError:
        try:
            with open(args.output, 'w+') as f:
                f.write(decoded)
        except (IOError, OSError) as e:
            printError('Input was decoded, but cannot output to declared file. Check your path.')
            printError('Do you want to print the decoded string to stdout? (y/N)')
            if input().lower() == 'y':
                print(decoded)        
            exit(2)
    print(bold + "Success!" + reset + " Decoded string written to " + args.output)
else:
    print(bold + "Success!" + reset + " Decoded string:\n\n" + decoded)
