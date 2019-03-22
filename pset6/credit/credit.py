from cs50 import get_int

while True:
    cc_number = get_int("credit card number: ")
    if (cc_number):
        break
string_number = str(cc_number)
digit_number = len(string_number) # how many digits there are in number
digit1 = int(string_number[0])
digit2 = int(string_number[1])

# magic formula
sum = 0
m = 1
for i in range(digit_number):
    if (m % 2 == 0):
        z = int(string_number[-m])*2
        sum += z % 10
        if (z >= 10):
            sum += int(str(z)[0])
    elif (m % 2 != 0):
        y = int(string_number[-m])
        sum += y
    m += 1
    if (m > digit_number):
        break

x = sum % 10

#check card's validity
if (((digit1 == 3 and digit2 == 4 or digit2 == 7) and x == 0 and digit_number == 15)):
    print("AMEX")
elif ((digit1 == 5 and digit2 == 1 or digit2 == 2 or digit2 == 3 or digit2 == 4 or digit2 == 5) and x == 0 and digit_number == 16):
    print("MASTERCARD")
elif (digit1 == 4 and x == 0 and digit_number == 13 or digit_number == 16):
    print("VISA")
else:
    print("INVALID")