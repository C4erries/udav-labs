from math import sqrt
import numpy as np

def Divs(num: int) -> list[int]:
    divs = []
    for d in range(1, int(sqrt(num))): 
        if num % d == 0:
            divs.append(d)
            divs.append(num // d)
    if num == int(sqrt(num))**2:
        divs.append(int(sqrt(num)))
    return divs

def isCoprime(n1: int, n2: int) -> bool:
    mn = min(n1, n2)
    for d in range(2, mn + 1):
        if n1 % d == 0 and n2 % d == 0:
            return False
    return True

def countDivs(num: int) -> int:
    count = 0
    for k in range(2, int(sqrt(num))): 
        if num % k == 0:
            count += 2
    if num == int(sqrt(num))**2:
        count += 1
    return count

def isPrime(num: int) -> bool:
    if num < 2:
        return False
    for k in range(2, int(sqrt(num)+1)):  
        if num % k == 0:
            return False
    return True

def func1(num: int) -> int:
    acc = 1
    non_prime_divs = [v for v in range(4, num // 2 + 1) if num % v == 0 and not isPrime(v)]
    if not isPrime(num):
        non_prime_divs.append(num)
    acc += sum(non_prime_divs)
    return acc

def func2(num: int) -> int:
    acc = 0
    for k in str(num):
        if int(k) < 3:
            acc += 1
    return acc

def func3(num: int):
    s = sum([int(v) for v in str(num) if v in "2357"])
    if s == 0 or abs(num) <= 1:
        return 0


    prime_divs = set(v for v in range(2, num // 2 + 1) if num % v == 0 and isPrime(v))
    if isPrime(num):
        prime_divs.add(num)

    for p in prime_divs:
        if s % p != 0:
            return np.inf

    return 0 


for n in [2516, 1514324218]:
    print(func1(n))