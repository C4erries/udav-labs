from collections import Counter


def task19(arr: list[int]) -> list[int]:
    """Дан список. Построить массив из элементов, делящихся на свой номер и встречающихся в исходном массиве один раз."""

    freq = Counter(arr)
    return [
        value
        for index, value in enumerate(arr, start=1)
        if value % index == 0 and freq[value] == 1
    ]


print(task19([3, 4, 9, 8, 10, 6, 21]))
