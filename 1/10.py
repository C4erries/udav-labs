def task10() -> list[str]:
    """Дан список строк с клавиатуры. Упорядочить его по количеству слов в строке."""

    n = int(input())
    lines = [input() for _ in range(n)]
    return sorted(lines, key=lambda line: len(line.split()))


print(task10())
