def task1() -> int:
    """Даны два списка чисел. Посчитать, сколько чисел содержится одновременно в первом и во втором списке."""

    first = list(map(int, input().split()))
    second = list(map(int, input().split()))
    return len(set(first) & set(second))


print(task1())
