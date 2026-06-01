import re


def task6(text: str) -> int:
    """Дана строка. Подсчитать количество чисел в строке, значение которых больше 5."""

    numbers = map(int, re.findall(r"-?\d+", text))
    return sum(1 for number in numbers if number > 5)


print(task6("a1 b10 c-3 d7 e5 100"))
