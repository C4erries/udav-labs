from collections import defaultdict

#To do dfs Euler tour
def solve(
    parent: dict[str, str | None], queries: list[tuple[str, str]]
) -> list[int]:

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
    """Даны два элемента в дереве. Для каждого запроса определить: 1/2/0 в зависимости от отношения предок-потомок."""

    n = int(input())
    edges = [tuple(input().split()) for _ in range(n - 1)]

    k = int(input())
    queries = [tuple(input().split()) for _ in range(k)]

    answers = solve(edges, queries)
    return " ".join(map(str, answers))


print(task2())
