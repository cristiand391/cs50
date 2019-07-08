from cs50 import get_string
from sys import argv
from sys import exit

def main():
    if len(argv) == 2:
        dictionary = argv[1]
    else:
        print("Usage: python bleep.py dictionary")
        exit(1)
        
        
    words = set()
    
    file = open(dictionary, "r")
    for line in file:
        words.add(line.lower().strip())
    file.close()
    
    msg = get_string("What message would you like to censor?\n")
    
    for w in msg.split():
        if w.lower() in words:
            print("*" * len(w) + " ", end="")
        else:
            print(w + " ", end="")

    print("")
if __name__ == "__main__":
main()
