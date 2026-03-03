from collections import Counter


def task18(arr: list[int]) -> list[int]:
    """Для списка построить список номеров элементов, которые повторяются наибольшее число раз."""

    if not arr:
        return []

    freq = Counter(arr)
    max_count = max(freq.values())
    popular = {value for value, count in freq.items() if count == max_count}
    return [i for i, value in enumerate(arr) if value in popular]


print(task18([4, 1, 4, 2, 3, 2, 4, 2]))
