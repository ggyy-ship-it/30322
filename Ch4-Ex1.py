def gcd(x, y):
    if x % y == 0:
        return y
    else:
        return gcd(y, x % y)

x, y = map(int, input().split())
L = gcd(x, y)
N = (x * y) // (L * L)
print(L)
print(N)
