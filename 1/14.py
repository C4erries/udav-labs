def task14(lines: list[str]) -> list[str]:
    """Упорядочить строки по возрастанию среднего количества зеркальных троек символов (например, 'ada')."""

    def fn(line: str) -> float:
        if len(line) < 3:
            return 0.0
        triples = sum(1 for i in range(len(line) - 2) if line[i] == line[i + 2])
        return triples / (len(line) - 2)

    return sorted(lines, key=fn)


print(task14(["xyx", "abcde", "ababa", "aaaa"]))
