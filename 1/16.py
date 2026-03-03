def task16(arr: list[int]) -> tuple[int, int]:
    """Дан целочисленный массив. Найти два наибольших элемента."""

    if len(arr) < 2:
        raise ValueError("Need at least two elements.")
    first, second = sorted(arr, reverse=True)[:2]
    return first, second


print(task16([3, 10, 7, 10, 2, 8]))
