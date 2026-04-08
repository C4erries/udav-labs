from bisect import bisect_left
from collections import Counter
from pathlib import Path


def count_pairs(freq: Counter[int], limit: int) -> int:
    values = sorted(freq)
    counts = [freq[value] for value in values]
    suffix_counts = [0] * (len(values) + 1)

    for index in range(len(values) - 1, -1, -1):
        suffix_counts[index] = suffix_counts[index + 1] + counts[index]

    total = 0
    for index, value in enumerate(values):
        count = counts[index]
        first_good = bisect_left(values, limit - value, lo=index)

        if first_good == index:
            total += count * (count - 1) // 2
            total += count * suffix_counts[index + 1]
        elif first_good < len(values):
            total += count * suffix_counts[first_good]

    return total


def solve_file(path: Path) -> int:
    with path.open(encoding="utf-8") as file:
        _, limit = map(int, file.readline().split())
        freq = Counter(int(line) for line in file)
    return count_pairs(freq, limit)


def task1() -> str:
    """
    Посчитать количество различных пар кандидатов, у которых сумма рейтингов
    не меньше K.
    """

    base_dir = Path(__file__).resolve().parent.parent / "ЛР4"

    file_a = base_dir / "27-169a.txt"
    if not file_a.exists():
        file_a = base_dir / "27-169bb.txt"

    file_b = base_dir / "27-169.txt"
    if not file_b.exists():
        file_b = base_dir / "27-169b.txt"

    answer_a = solve_file(file_a)
    answer_b = solve_file(file_b)
    return f"{answer_a} {answer_b}"


print(task1())  # 1424027568 1303810249487


"""
5 100
20
50
50
100
200
"""
