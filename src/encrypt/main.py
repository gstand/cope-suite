import base64
from ast import literal_eval
import argparse

parser = argparse.ArgumentParser(description="cope encryption suite - encrypt")
parser.add_argument("-k", "--key", help="optional key", dest = "key", default="", type=str)
parser.add_argument("string")
args = parser.parse_args()

chars = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "!", ".", "?", " "]
if all(char in chars for char in args.string) == False:
    raise ValueError("Invalid characters in data\nonly use A-Z, a-z, 0-9, !, ., ?, and space")

key = 0
for char in args.key: 
    key += ord(char)
key %= len(chars)
chars[:]=chars[key:len(chars)]+chars[0:key]

numbers, raw, charred = [], '', ''
for char in args.string:
    i, found = 0, False
    while found == False:
        if char == chars[i]:
            numbers.append(i+16)
            found = True
        i = i + 1

for number in numbers: 
    raw += hex(number)[2:]

points = ['0x'+(raw[i:i+4]) for i in range(0, len(raw), 4)]
for point in points:
    charred += chr(literal_eval(point))
    
final = base64.b85encode(bytes(charred, 'utf-8')).decode('ascii')
print(final)