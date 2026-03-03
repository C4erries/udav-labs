def task12(lines: list[str]) -> list[str]:
    """Упорядочить строки по возрастанию медианного значения выборки символов с пересчётом после удаления предыдущей медианы."""

    def iterative_median_value(line: str) -> float:
        sample = sorted(map(ord, line))
        if not sample:
            return 0.0
        medians = []
        while sample:
            mid = (len(sample) - 1) // 2
            medians.append(sample.pop(mid))
        return sum(medians) / len(medians)

    return sorted(lines, key=iterative_median_value)


print(task12(["delta", "abc", "Zzz", "abba"]))
