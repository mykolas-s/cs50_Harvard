from cs50 import get_int

while True:
    n = get_int("Specify pyramid height (lower than 23): ")
    if (n >= 0 and n <= 23):
        break
a = 2
for i in range(n):
    print(" " * (n - a + 1), end="")
    print("#" * a, end="")
    print()
    a += 1