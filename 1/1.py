from math import gcd, isqrt

def Divs(num: int) -> list[int]:
    num = abs(num)
    if num == 0:
        return []
    return sorted({d for k in range(1, isqrt(num) + 1) if num % k == 0 for d in (k, num // k)})

def isCoprime(n1: int, n2: int) -> bool:
    return gcd(n1, n2) == 1

def countDivs(num: int) -> int:
    return sum(1 for d in Divs(num) if d not in (1, abs(num)))

def isPrime(num: int) -> bool:
    if num < 2:
        return False
    return all(num % k != 0 for k in range(2, isqrt(num) + 1))

def func1(num: int) -> int:
    non_prime_divs = [d for d in Divs(num) if d != 1 and not isPrime(d)]
    return 1 + sum(non_prime_divs)

def func2(num: int) -> int:
    return sum(1 for ch in str(abs(num)) if int(ch) < 3)

def func3(num: int):
    s = sum(int(ch) for ch in str(abs(num)) if ch in "2357")
    if s == 0 or abs(num) <= 1:
        return 0

    prime_divs = [d for d in Divs(num) if isPrime(d)]
    return 0 if all(s % p == 0 for p in prime_divs) else float("inf")


for n in [2516, 1514324218]:
    print(func1(n))
