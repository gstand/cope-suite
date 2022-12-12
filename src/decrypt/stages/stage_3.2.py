import base64
from ast import literal_eval as b
import argparse
a = argparse.ArgumentParser(description="cope encryption suite - decrypt")
a.add_argument("-k", "--key", help="optional key", dest = "d", default = "")
a.add_argument("e")
c = a.parse_args()
x = lambda x: ord(x)
r = lambda x: len(x)
d = lambda x: hex(x)
u = 0
e = 2
h = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "!", ".", "?", " "]
w = 0
f = 16
z = lambda a,b,c: range(a,b,c)
g = lambda x: base64.b85decode(x).decode('utf-8')
y = lambda x: '0x'+x
j = lambda x: int(x)
for v in c.d: w += x(v)
w%=r(h)
h[:]=h[w:r(h)]+h[u:w]
l,m,n= [], '', ''
k = g(c.e)
for o in k: m += d(x(o))[e:] 
l = [j(b(y(m[i:i+e]))) for i in z(u, r(m), e)]
for p in l: n += h[p-f]
print(n)