"""
Тестові вектори для лабораторної роботи №4.
Містить приклади з методичних вказівок.
"""

# Тестовий вектор 1
VECTOR_1 = {
    "value": "ff00000000000000000000000000000000000000000000000000000000000000",
    "num_bytes": 32,
    "little_endian": 255,
    "big_endian": 115339776388732929035197660848497720713218148788040405586178452820382218977280
}

# Тестовий вектор 2
VECTOR_2 = {
    "value": "aaaa000000000000000000000000000000000000000000000000000000000000",
    "num_bytes": 32,
    "little_endian": 43690,
    "big_endian": 77193548260167611359494267807458109956502771454495792280332974934474558013440
}

# Тестовий вектор 3
VECTOR_3 = {
    "value": "FFFFFFFF",
    "num_bytes": 4,
    "little_endian": 4294967295,
    "big_endian": 4294967295
}

# Тестовий вектор 4 (спрощений варіант)
# Оригінальне значення дуже довге (512 байт), тому використовуємо скорочений варіант
VECTOR_4 = {
    "value": "F0" + "0" * 1022,  # 512 байт = 1024 символи hex
    "num_bytes": 512,
    "little_endian": 240,
    "big_endian": int("F0" + "0" * 1022, 16)
}

# Список усіх векторів
TEST_VECTORS = [VECTOR_1, VECTOR_2, VECTOR_3, VECTOR_4]

def get_test_vector(index: int) -> dict:
    """
    Отримати тестовий вектор за індексом.

    Args:
        index: Індекс вектора (0-3)

    Returns:
        Словник з даними тестового вектора

    Raises:
        IndexError: Якщо індекс некоректний
    """
    if 0 <= index < len(TEST_VECTORS):
        return TEST_VECTORS[index]
    raise IndexError(f"Test vector index must be between 0 and {len(TEST_VECTORS)-1}")