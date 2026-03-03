
import random


def task2(text: str) -> str:
    """Дана строка со словами через пробел. Перемешать в каждом слове все символы, кроме первого и последнего."""

    def shuffle_word(word: str) -> str:
        if len(word) <= 3:
            return word
        middle = list(word[1:-1])
        random.shuffle(middle)
        return word[0] + "".join(middle) + word[-1]

    return " ".join(map(shuffle_word, text.split()))


print(task2("text txt abcdef bgdfkb 13451"))
