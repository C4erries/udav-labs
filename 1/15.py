def task15(arr: list[int]) -> list[int]:
    """Дан целочисленный массив. Переставить в обратном порядке элементы между минимальным и максимальным элементами."""

    if len(arr) < 2:
        return arr[:]

    left, right = sorted((arr.index(min(arr)), arr.index(max(arr))))
    result = arr[:]
    result[left + 1:right] = reversed(result[left + 1:right])
    return result


print(task15([7, 2, 9, 4, 6, 1, 5]))
