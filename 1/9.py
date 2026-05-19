def task9() -> list[str]:
    """Прочитать список строк с клавиатуры и упорядочить его по длине строк."""

    n = int(input())
    lines = [input() for _ in range(n)]
    return sorted(lines, key=len)


print(task9())
