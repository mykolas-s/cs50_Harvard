from cs50 import get_string
import sys

if (sys.argv[1] == None):
    print("Error")

p = get_string("plaintext: ")
print("ciphertext: ", end="")

k = int(sys.argv[1])

for i in p:
    if i.isupper():
        o = (ord(i) - 65 + k) % 26 + 65
        print(chr(o), end="")
    elif i.islower():
        o = (ord(i) - 97 + k) % 26 + 97
        print(chr(o), end="")
    else:
        print(i, end="")
print()