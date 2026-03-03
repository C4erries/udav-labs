def task13(lines: list[str]) -> list[str]:
    """Упорядочить строки по возрастанию квадратичного отклонения между максимальным ASCII-кодом и разностями ASCII-кодов зеркальных пар."""

    def deviation(line: str) -> float:
        if len(line) < 2:
            return 0.0
        max_code = max(map(ord, line))
        diffs = [
            abs(ord(line[i]) - ord(line[-i - 1]))
            for i in range(len(line) // 2)
        ]
        if not diffs:
            return 0.0
        return sum((max_code - diff) ** 2 for diff in diffs) / len(diffs)

    return sorted(lines, key=deviation)


print(task13(["abcd", "abba", "xyz", "aZ9"]))
