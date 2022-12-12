import base64
from ast import literal_eval as b
import argparse
a = argparse.ArgumentParser(description="cope encryption suite - encrypt")
a.add_argument("-k", "--key", help="optional key", dest = "d", default="", type=str)
a.add_argument("e")
c = a.parse_args()
n = lambda x: all(x)
o = lambda x: (_ for _ in ()).throw(ValueError("Invalid characters in data\nonly use A-Z, a-z, 0-9, !, ., ?, and space")) if x else None
p = False
q = lambda a,b: [c in a for c in b]
r = lambda x: len(x)
j, k, l = [], '', ''
s = lambda x: j.append(x)
t = True
u = lambda x: hex(x)
x = lambda x: ord(x)
h = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "!", ".", "?", " "]
w = 0
y = r(h)
z = lambda a,b,c: range(a,b,c)
aa = lambda x: chr(x)
ab = lambda x: base64.b85encode(bytes(x, 'utf-8')).decode('ascii')
ac = lambda x: print(x)
ad = 16
ae = 1
af = lambda x: '0x'+x
ag = 0
ah = 2
ai = 4
o(n(q(h, c.e)) == p)
for v in c.d: w += x(v)
w%=y
h[:]=h[w:r(h)]+h[ag:w]
for o in c.e:
    i,n = ag, p
    while n == p:
        if o == h[i]:
            s(i+ad)
            n = t
        i = i + ae
for p in j: k += u(p)[ah:]
q = [af(k[i:i+ai]) for i in z(ag, r(k), ai)]
for r in q: l += aa(b(r))
m = ab(l)
ac(m)