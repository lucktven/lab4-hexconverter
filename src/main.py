"""
Головний файл для демонстрації роботи бібліотеки.
Демонструє всі 4 функції на тестових векторах.
"""
import sys
import os

# Додаємо теку src до шляху пошуку модулів
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.converter import (
    hex_to_little_endian,
    hex_to_big_endian,
    little_endian_to_hex,
    big_endian_to_hex,
    validate_hex_string
)
from src.test_vectors import TEST_VECTORS, get_test_vector


def print_separator():
    """Друкує роздільник."""
    print("\n" + "=" * 70)


def print_vector_info(vector: dict, index: int):
    """Друкує інформацію про тестовий вектор."""
    print_separator()
    print(f"ТЕСТОВИЙ ВЕКТОР {index + 1}")
    print("=" * 70)

    # Скорочений вивід значення
    value = vector["value"]
    if len(value) > 64:
        display_value = value[:32] + "..." + value[-32:]
    else:
        display_value = value

    print(f"HEX значення: {display_value}")
    print(f"Кількість байтів: {vector['num_bytes']}")
    print(f"Очікуваний little-endian: {vector['little_endian']}")

    # Скорочений вивід великого числа
    big_endian_str = str(vector['big_endian'])
    if len(big_endian_str) > 50:
        big_endian_str = big_endian_str[:25] + "..." + big_endian_str[-25:]
    print(f"Очікуваний big-endian: {big_endian_str}")


def test_vector_conversion(vector: dict, index: int) -> bool:
    """
    Тестує конвертацію для одного вектора.

    Args:
        vector: Тестовий вектор
        index: Індекс вектора

    Returns:
        True якщо всі тести пройшли, False якщо є помилки
    """
    all_passed = True

    print_vector_info(vector, index)

    # 1. Перевірка коректності hex
    is_valid = validate_hex_string(vector["value"])
    print(f"\n1. Перевірка коректності HEX: {'✓ ПАС' if is_valid else '✗ НЕ ПАС'}")
    if not is_valid:
        all_passed = False

    # 2. Конвертація у little-endian
    try:
        le_result = hex_to_little_endian(vector["value"], vector["num_bytes"])
        le_passed = le_result == vector["little_endian"]
        print(f"2. HEX → Little-endian: {'✓ ПАС' if le_passed else '✗ НЕ ПАС'}")
        if not le_passed:
            print(f"   Отримано: {le_result}")
            all_passed = False
    except Exception as e:
        print(f"2. HEX → Little-endian: ✗ ПОМИЛКА: {e}")
        all_passed = False

    # 3. Конвертація у big-endian
    try:
        be_result = hex_to_big_endian(vector["value"], vector["num_bytes"])
        be_passed = be_result == vector["big_endian"]
        print(f"3. HEX → Big-endian: {'✓ ПАС' if be_passed else '✗ НЕ ПАС'}")
        if not be_passed:
            # Скорочений вивід для великих чисел
            be_str = str(be_result)
            if len(be_str) > 50:
                be_str = be_str[:25] + "..." + be_str[-25:]
            print(f"   Отримано: {be_str}")
            all_passed = False
    except Exception as e:
        print(f"3. HEX → Big-endian: ✗ ПОМИЛКА: {e}")
        all_passed = False

    # 4. Зворотня конвертація (лише для невеликих значень)
    if vector["num_bytes"] <= 8:
        try:
            # Little-endian → HEX
            le_hex = little_endian_to_hex(vector["little_endian"], vector["num_bytes"])
            # Порівнюємо з оригіналом (без ведучих нулів)
            original_hex = vector["value"].lstrip('0').lower() or '0'
            le_hex_clean = le_hex.lstrip('0').lower() or '0'
            le_reverse_passed = le_hex_clean == original_hex

            print(f"4. Little-endian → HEX: {'✓ ПАС' if le_reverse_passed else '✗ НЕ ПАС'}")
            if not le_reverse_passed:
                print(f"   Оригінал: {original_hex}")
                print(f"   Отримано: {le_hex_clean}")
                all_passed = False
        except Exception as e:
            print(f"4. Little-endian → HEX: ✗ ПОМИЛКА: {e}")
            all_passed = False

    return all_passed


def demonstrate_simple_examples():
    """Демонструє прості приклади використання."""
    print_separator()
    print("ПРОСТІ ПРИКЛАДИ ВИКОРИСТАННЯ")
    print("=" * 70)

    examples = [
        ("12345678", 4, "4-байтне значення"),
        ("FF", 1, "1-байтне значення"),
        ("AABB", 2, "2-байтне значення"),
        ("DEADBEEF", 4, "4-байтне значення"),
    ]

    for hex_str, num_bytes, description in examples:
        print(f"\n{description}: {hex_str} ({num_bytes} байти)")

        # Конвертація вперед
        le = hex_to_little_endian(hex_str, num_bytes)
        be = hex_to_big_endian(hex_str, num_bytes)

        print(f"  Little-endian: {le}")
        print(f"  Big-endian:    {be}")

        # Конвертація назад
        le_hex = little_endian_to_hex(le, num_bytes)
        be_hex = big_endian_to_hex(be, num_bytes)

        print(f"  Little → HEX: {le_hex}")
        print(f"  Big → HEX:    {be_hex}")


def main():
    """Головна функція демонстрації."""
    print("ЛАБОРАТОРНА РОБОТА №4")
    print("Конвертація HEX значень з урахуванням порядку байтів")
    print("\n" + "=" * 70)

    # Загальна статистика
    total_vectors = len(TEST_VECTORS)
    passed_vectors = 0

    # Тестування всіх векторів
    for i in range(total_vectors):
        vector = get_test_vector(i)
        if test_vector_conversion(vector, i):
            passed_vectors += 1

    # Вивід результатів
    print_separator()
    print("РЕЗУЛЬТАТИ ТЕСТУВАННЯ")
    print("=" * 70)
    print(f"Усього тестових векторів: {total_vectors}")
    print(f"Успішно пройдено: {passed_vectors}")
    print(f"Не пройдено: {total_vectors - passed_vectors}")

    if passed_vectors == total_vectors:
        print("\n✓ Всі тести пройдені успішно!")
    else:
        print(f"\n✗ Знайдено помилки в {total_vectors - passed_vectors} тестах")

    # Демонстрація простих прикладів
    demonstrate_simple_examples()

    print_separator()
    print("Демонстрація завершена!")
    print("\nДля детальних тестів запустіть:")
    print("python -m pytest tests/test_converter.py -v")


if __name__ == "__main__":
    main()