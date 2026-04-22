import re


OCTET_PATTERN = r"(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)"
"""
250-255
200-249
100-199
0-99
"""
IPV4_PATTERN = re.compile(rf"^(?:{OCTET_PATTERN}\.){{3}}{OCTET_PATTERN}$")


class InvalidIPv4Error(ValueError):
    """Некорректный IPv4-адрес."""


def is_ipv4(value: str) -> bool:
    """Проверить, является ли строка корректным IPv4-адресом."""

    return IPV4_PATTERN.fullmatch(value) is not None


def parse_ipv4(value: str) -> str:
    """
    Вернуть IPv4-адрес или выбросить исключение, если аргумент некорректен.
    """

    if not isinstance(value, str):
        raise InvalidIPv4Error("IPv4-адрес должен быть строкой.")
    if not is_ipv4(value):
        raise InvalidIPv4Error(
            "Передана строка, не являющаяся корректным IPv4-адресом."
        )
    return value


def task1() -> bool:
    """
    Проверить, является ли введенная строка IP-адресом версии IPv4.
    """

    return is_ipv4(input())

print(task1())


"""
192.168.0.1
"""
