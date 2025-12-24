"""
Бібліотека для конвертації HEX значень з урахуванням порядку байтів.
Реалізація лабораторної роботи №4.
"""


def hex_to_little_endian(hex_string: str, num_bytes: int) -> int:
    """
    Конвертує шістнадцятковий рядок у ціле число у форматі little-endian.

    Args:
        hex_string: Шістнадцятковий рядок (без префікса 0x)
        num_bytes: Кількість байтів, яку має займати число

    Returns:
        Ціле число у форматі little-endian

    Raises:
        ValueError: Якщо hex_string порожній або некоректний
    """
    # Перевірка вхідних даних
    if not hex_string:
        raise ValueError("Hex string cannot be empty")

    # Нормалізація рядка
    hex_string = hex_string.strip().lower()

    # Перевірка, чи є рядок коректним hex
    try:
        int(hex_string, 16)
    except ValueError:
        raise ValueError("Invalid hex string")

    # Визначення очікуваної довжини
    expected_length = num_bytes * 2

    # Доповнення нулями зліва, якщо потрібно
    if len(hex_string) < expected_length:
        hex_string = hex_string.zfill(expected_length)
    # Обрізання, якщо задовгий (беремо останні байти)
    elif len(hex_string) > expected_length:
        hex_string = hex_string[-expected_length:]

    # Розбиття на байти (по 2 символи)
    bytes_list = []
    for i in range(0, len(hex_string), 2):
        byte = hex_string[i:i + 2]
        bytes_list.append(byte)

    # Little-endian: реверсуємо порядок байтів
    bytes_list.reverse()

    # Об'єднання байтів
    little_endian_hex = ''.join(bytes_list)

    # Конвертація у десяткове число
    return int(little_endian_hex, 16)


def hex_to_big_endian(hex_string: str, num_bytes: int) -> int:
    """
    Конвертує шістнадцятковий рядок у ціле число у форматі big-endian.

    Args:
        hex_string: Шістнадцятковий рядок (без префікса 0x)
        num_bytes: Кількість байтів, яку має займати число

    Returns:
        Ціле число у форматі big-endian

    Raises:
        ValueError: Якщо hex_string порожній або некоректний
    """
    # Перевірка вхідних даних
    if not hex_string:
        raise ValueError("Hex string cannot be empty")

    # Нормалізація рядка
    hex_string = hex_string.strip().lower()

    # Перевірка, чи є рядок коректним hex
    try:
        int(hex_string, 16)
    except ValueError:
        raise ValueError("Invalid hex string")

    # Визначення очікуваної довжини
    expected_length = num_bytes * 2

    # Доповнення нулями зліва, якщо потрібно
    if len(hex_string) < expected_length:
        hex_string = hex_string.zfill(expected_length)
    # Обрізання, якщо задовгий (беремо останні байти)
    elif len(hex_string) > expected_length:
        hex_string = hex_string[-expected_length:]

    # Big-endian: просто конвертуємо
    return int(hex_string, 16)


def little_endian_to_hex(value: int, num_bytes: int) -> str:
    """
    Конвертує ціле число у шістнадцятковий рядок у форматі little-endian.

    Args:
        value: Ціле число для конвертації
        num_bytes: Кількість байтів для представлення

    Returns:
        Шістнадцятковий рядок у форматі little-endian

    Raises:
        ValueError: Якщо value від'ємне
    """
    if value < 0:
        raise ValueError("Value must be non-negative")

    # Конвертація числа у hex
    hex_string = hex(value)[2:]  # Видаляємо '0x'

    # Доповнення до потрібної довжини
    expected_length = num_bytes * 2
    hex_string = hex_string.zfill(expected_length)

    # Обрізання, якщо задовгий
    if len(hex_string) > expected_length:
        hex_string = hex_string[-expected_length:]

    # Розбиття на байти
    bytes_list = []
    for i in range(0, len(hex_string), 2):
        byte = hex_string[i:i + 2]
        bytes_list.append(byte)

    # Little-endian: реверсуємо порядок байтів
    bytes_list.reverse()

    # Об'єднання байтів
    return ''.join(bytes_list)


def big_endian_to_hex(value: int, num_bytes: int) -> str:
    """
    Конвертує ціле число у шістнадцятковий рядок у форматі big-endian.

    Args:
        value: Ціле число для конвертації
        num_bytes: Кількість байтів для представлення

    Returns:
        Шістнадцятковий рядок у форматі big-endian

    Raises:
        ValueError: Якщо value від'ємне
    """
    if value < 0:
        raise ValueError("Value must be non-negative")

    # Конвертація числа у hex
    hex_string = hex(value)[2:]  # Видаляємо '0x'

    # Доповнення до потрібної довжини
    expected_length = num_bytes * 2
    hex_string = hex_string.zfill(expected_length)

    # Обрізання, якщо задовгий
    if len(hex_string) > expected_length:
        hex_string = hex_string[-expected_length:]

    return hex_string


def validate_hex_string(hex_string: str) -> bool:
    """
    Перевіряє коректність шістнадцяткового рядка.

    Args:
        hex_string: Рядок для перевірки

    Returns:
        True якщо рядок коректний, інакше False
    """
    if not hex_string:
        return False

    hex_string = hex_string.strip().lower()

    # Допустимі символи в hex
    valid_chars = set('0123456789abcdef')

    # Перевірка кожного символу
    for char in hex_string:
        if char not in valid_chars:
            return False

    return True