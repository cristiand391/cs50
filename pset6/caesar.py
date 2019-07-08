from cs50 import get_string
from sys import argv
from sys import exit

if len(argv) == 2:
    k = int(argv[1])
else:
    print("Usage: python caesar.py k")
    exit(1)
    
msg = get_string("plaintext: ")

print("ciphertext: ", end="")

for c in msg:
    if c.isalpha():
        if c.islower():
            print(chr(((ord(c) + k - 97) % 26) + 97), end="")
        elif c.isupper():
            print(chr(((ord(c) + k - 65) % 26) + 65), end="")
    else:
        print(c, end="")
print("")
