from cs50 import get_float

while True:
    f = get_float("Change owed: ")
    if f > 0:
        break

# float to integer
i = round(f * 100)
count = 0

while i >= 25:
    i = i - 25
    count += 1
while i >= 10:
    i = i - 10
    count += 1
while i >= 5:
    i = i - 5
    count += 1
while i >= 1:
    i = i - 1
    count += 1
print(f"You will need {count} coins to give back {f} change")