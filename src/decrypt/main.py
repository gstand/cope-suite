import base64
from ast import literal_eval
import argparse

parser = argparse.ArgumentParser(description="cope encryption suite - decrypt")
parser.add_argument("-k", "--key", help="optional key", dest = "key", default = "")
parser.add_argument("string")
args = parser.parse_args()

chars = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "!", ".", "?", " "]
points, raw, final= [], '', ''
key = 0

for char in args.key: 
    key += ord(char)
key %= len(chars)
chars[:]=chars[key:len(chars)]+chars[0:key]

charred = base64.b85decode(args.string).decode('utf-8')
for char in charred:
    raw += hex(ord(char))[2:] 

points = [int(literal_eval('0x'+(raw[i:i+2]))) for i in range(0, len(raw), 2)]

for point in points: 
    final += chars[point-16]

print(final)