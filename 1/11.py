from collections import Counter


ALPH = set("abcdefghijklmnopqrstuvwxyzабвгдеёжзийклмнопрстуфхцчшщъыьэюя")


def task11(lines: list[str]) -> list[str]:
    """Упорядочить строки по возрастанию разницы между частотой самого частого символа и частотой его появления в алфавите. ????"""

    def score(line: str) -> int:
        letters = [ch.lower() for ch in line if ch.isalpha()]
        if not letters:
            return 0
        symbol, max_freq = Counter(letters).most_common(1)[0]
        alphabet_freq = 1 if symbol in ALPH else 0
        return max_freq - alphabet_freq

    return sorted(lines, key=score)


print(task11(["banana", "abc", "committee", "aabb"]))
