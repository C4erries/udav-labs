def solve(durations: list[int], post_count: int) -> list[int] | None:
    total_duration = sum(durations)
    if total_duration % post_count != 0:
        return None

    target = total_duration // post_count
    current_sum = 0
    current_size = 0
    result = []

    for duration in durations:
        current_sum += duration
        current_size += 1

        if current_sum > target:
            return None
        if current_sum == target:
            result.append(current_size)
            current_sum = 0
            current_size = 0

    if current_sum != 0 or len(result) != post_count:
        return None
    return result


def task3() -> str:
    """
    Разбить видео на k подряд идущих постов так, чтобы сумма длительностей
    в каждом посте была одинаковой.
    """


    n, k = map(int, input().split())
    durations = list(map(int, input().split()))

    answer = solve(durations, k)
    if answer is None:
        return "Нет"
    return "Да\n" + " ".join(map(str, answer))


print(task3())


"""
6 3
3 3 1 4 1 6
"""
