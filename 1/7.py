def task7(text: str) -> int | None:
    """Дана строка. Найти минимальное из имеющихся в ней натуральных чисел."""

    numbers = []
    current = ""

    for ch in text:
        if ch.isdigit():
            current += ch
        elif current:
            value = int(current)
            if value > 0:
                numbers.append(value)
            current = ""

    if current:
        value = int(current)
        if value > 0:
            numbers.append(value)

    return min(numbers) if numbers else None


print(task7("abc 42 qwe7 2 13 2 zz1z"))
