import base64

def encrypt(data: str, keystr: str = "") -> str:
    chars = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "!", ".", "?", " "]
    if all(char in chars for char in data) == False:
        raise ValueError("Invalid characters in data\nonly use A-Z, a-z, 0-9, !, ., ?, and space")

    key = 0
    for char in keystr: 
        key += ord(char)
    key %= len(chars)
    chars[:]=chars[key:len(chars)]+chars[0:key]

    numbers, raw, charred = [], '', ''
    for char in data:
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
    return final

def decrypt(data: str, keystr: str = "") -> str:
    chars = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "!", ".", "?", " "]
    points, raw, final= [], '', ''
    key = 0

    for char in keystr: 
        key += ord(char)
    key %= len(chars)
    chars[:]=chars[key:len(chars)]+chars[0:key]

    charred = base64.b85decode(data).decode('utf-8')
    for char in charred:
        raw += hex(ord(char))[2:] 

    points = [int(literal_eval('0x'+(raw[i:i+2]))) for i in range(0, len(raw), 2)]

    for point in points: 
        final += chars[point-16]

    print(final)
