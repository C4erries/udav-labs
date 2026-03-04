def solve(parent: dict[str, str | None], queries: list[tuple[str, str]]) -> list[int]:
    def is_ancestor(ancestor: str, node: str) -> bool:
        # ancestor - предок для node ?
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
    """
        Даны два элемента в дереве. Определите, является ли один из них
    потомком другого.
        Во входных данных записано дерево в том же формате, что и в
    предыдущей задаче Далее идет число запросов K
        В каждой из следующих K
    строк, содержатся имена двух элементов дерева.
        Для каждого такого запроса выведите одно из трех чисел: 1, если первый
    элемент является предком второго, 2, если второй является предком первого
    или 0, если ни один из них не является предком другого.

    """
    n = int(input())
    edges = [tuple(input().split()) for _ in range(n - 1)]
    parent = {child: par for child, par in edges}

    k = int(input())
    queries = [tuple(input().split()) for _ in range(k)]

    answers = solve(parent, queries)
    return " ".join(map(str, answers))


print(task2()) # 1 2 0


"""
9
Alexei Peter_I
Anna Peter_I
Elizabeth Peter_I
Peter_II Alexei
Peter_III Anna
Paul_I Peter_III
Alexander_I Paul_I
Nicholaus_I Paul_I
3
Anna Nicholaus_I
Peter_II Peter_I
Alexei Paul_I
"""