from pathlib import Path


ALPHABET_LOWER = "абвгдежзийклмнопрстуфхцчшщъыьэюя"
ALPHABET_UPPER = ALPHABET_LOWER.upper()

ENCRYPTED_LOWER = ALPHABET_LOWER[1:] + ALPHABET_LOWER[0]
ENCRYPTED_UPPER = ALPHABET_UPPER[1:] + ALPHABET_UPPER[0]

DECRYPT_TABLE = str.maketrans(
    ENCRYPTED_LOWER + ENCRYPTED_UPPER,
    ALPHABET_LOWER + ALPHABET_UPPER,
)


def decrypt_text(text: str) -> str:
    """Расшифровать текст, в котором каждая русская буква заменена на следующую."""

    return text.translate(DECRYPT_TABLE)


def task2(source_path: str | Path, target_path: str | Path) -> str:
    """
    Считать зашифрованный русский текст из файла и записать расшифровку
    в новый файл.
    """

    source = Path(source_path)
    target = Path(target_path)

    encrypted_text = source.read_text(encoding="utf-8")
    decrypted_text = decrypt_text(encrypted_text)

    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(decrypted_text, encoding="utf-8")
    return decrypted_text


"""
task2("encrypted.txt", "decrypted.txt")
"""
