def task3(text: str) -> str:
    """Дана строка с цифрами и буквами. Расположить все цифры в начале строки, а буквы в конце."""

    digits = "".join(ch for ch in text if ch.isdigit())
    letters = "".join(ch for ch in text if ch.isalpha())
    return digits + letters


print(task3("gfjj32hdskf1h3og9394fn3"))
