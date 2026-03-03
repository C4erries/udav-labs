import re


def task7(text: str) -> int | None:
    """Дана строка. Найти минимальное из имеющихся в ней натуральных чисел."""

    numbers = [int(n) for n in re.findall(r"\b\d+\b", text) if int(n) > 0]
    return min(numbers) if numbers else None


print(task7("abc 42 qwe 7 0 13 2 zzz"))
