def solve(parent: dict[str, str | None], queries: list[tuple[str, str]]) -> list[int]:
    """Bruteforce ancestor checks by climbing parent links."""

    def is_ancestor(ancestor: str, node: str) -> bool:
        while node is not None:
            if node == ancestor:
                return True
            node = parent.get(node)
        return False

    result = []
    for first, second in queries:
        if is_ancestor(first, second):
            result.append(1)
        elif is_ancestor(second, first):
            result.append(2)
        else:
            result.append(0)
    return result


def task2() -> str:
    """For each query output 1 if first is ancestor, 2 if second is ancestor, else 0."""

    n = int(input())
    edges = [tuple(input().split()) for _ in range(n - 1)]
    parent = {child: par for child, par in edges}

    k = int(input())
    queries = [tuple(input().split()) for _ in range(k)]

    answers = solve(parent, queries)
    return " ".join(map(str, answers))


print(task2())
