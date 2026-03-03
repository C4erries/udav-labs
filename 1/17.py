def task17(arr: list[int]) -> int | None:
    """Дан целочисленный массив. Найти максимальный нечетный элемент."""

    odds = [x for x in arr if x % 2 != 0]
    return max(odds) if odds else None


print(task17([2, 14, 9, 11, 8, 3]))
