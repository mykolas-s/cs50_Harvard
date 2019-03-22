from cs50 import get_string
import sys

def main():
    if (sys.argv[1] == None or len(sys.argv) > 2):
       print("Error")
       sys.exit(1)

    k = sys.argv[1]
    k_lenght = len(k)

    for i in range(k_lenght):
        if (k[i].isalpha() == False):
            print("Error")
            sys.exit(1)

    p = get_string("plaintext: ")
    print("ciphertext: ", end="")
    count = 0

    for i in range(len(p)): #for every character in plaintext
        j = (i - count) % k_lenght
        if (p[i].isalpha()):
            if (p[i].isupper() == True):
                sum = ord(p[i]) + ord(k[j].upper())
                c = ((sum % 65) % 26) + 65
            elif (p[i].islower() == True):
                sum =  ord(p[i]) + ord(k[j].lower())
                c = ((sum % 97) % 26) + 97
            print(chr(c), end="")
        else:
            print(p[i], end="")
            count += 1
    print()

if __name__ == "__main__":
	main()