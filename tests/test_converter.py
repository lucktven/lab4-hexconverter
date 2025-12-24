"""
Модульні тести для бібліотеки конвертації.
"""
import pytest
from src.converter import (
    hex_to_little_endian,
    hex_to_big_endian,
    little_endian_to_hex,
    big_endian_to_hex,
    validate_hex_string
)
from src.test_vectors import TEST_VECTORS

class TestHexConversion:
    """Тести для конвертації HEX значень."""

    def test_hex_to_little_endian_vectors(self):
        """Тестування конвертації HEX у little-endian для всіх тестових векторів."""
        for i, vector in enumerate(TEST_VECTORS):
            result = hex_to_little_endian(vector['value'], vector['num_bytes'])
            assert result == vector['little_endian'], \
                f"Вектор {i+1} не пройшов: очікувано {vector['little_endian']}, отримано {result}"

    def test_hex_to_big_endian_vectors(self):
        """Тестування конвертації HEX у big-endian для всіх тестових векторів."""
        for i, vector in enumerate(TEST_VECTORS):
            result = hex_to_big_endian(vector['value'], vector['num_bytes'])
            assert result == vector['big_endian'], \
                f"Вектор {i+1} не пройшов: очікувано {vector['big_endian']}, отримано {result}"

    def test_little_endian_to_hex_round_trip(self):
        """Тестування зворотної конвертації little-endian до HEX."""
        test_cases = [
            ("12345678", 4),
            ("FF", 1),
            ("AABB", 2),
            ("DEADBEEF", 4),
            ("00", 1),
        ]

        for hex_str, num_bytes in test_cases:
            # Конвертація вперед
            le_value = hex_to_little_endian(hex_str, num_bytes)

            # Конвертація назад
            hex_result = little_endian_to_hex(le_value, num_bytes)

            # Порівняння (без ведучих нулів)
            expected = hex_str.lstrip('0').lower() or '0'
            actual = hex_result.lstrip('0').lower() or '0'

            assert actual == expected, \
                f"Round trip failed for {hex_str}: expected {expected}, got {actual}"

    def test_big_endian_to_hex_round_trip(self):
        """Тестування зворотної конвертації big-endian до HEX."""
        test_cases = [
            ("12345678", 4),
            ("FF", 1),
            ("AABB", 2),
            ("DEADBEEF", 4),
            ("00", 1),
        ]

        for hex_str, num_bytes in test_cases:
            # Конвертація вперед
            be_value = hex_to_big_endian(hex_str, num_bytes)

            # Конвертація назад
            hex_result = big_endian_to_hex(be_value, num_bytes)

            # Порівняння (без ведучих нулів)
            expected = hex_str.lstrip('0').lower() or '0'
            actual = hex_result.lstrip('0').lower() or '0'

            assert actual == expected, \
                f"Round trip failed for {hex_str}: expected {expected}, got {actual}"

    def test_validate_hex_string(self):
        """Тестування перевірки коректності HEX рядків."""
        # Коректні значення
        valid_cases = [
            "123456",
            "ABCDEF",
            "abcdef",
            "123",
            "FF",
            "a1b2c3",
            "0000",
        ]

        # Некоректні значення
        invalid_cases = [
            "GG",
            "12G4",
            "XYZ",
            "",
            "   ",
            "12 34",
            "0x123",  # Префікс не підтримується
        ]

        for hex_str in valid_cases:
            assert validate_hex_string(hex_str), f"Should be valid: {hex_str}"

        for hex_str in invalid_cases:
            assert not validate_hex_string(hex_str), f"Should be invalid: {hex_str}"

    def test_edge_cases(self):
        """Тестування граничних випадків."""
        # Порожній рядок
        with pytest.raises(ValueError, match="Hex string cannot be empty"):
            hex_to_little_endian("", 4)

        # Некоректний hex
        with pytest.raises(ValueError, match="Invalid hex string"):
            hex_to_little_endian("GG", 1)

        # Негативне число для зворотної конвертації
        with pytest.raises(ValueError, match="Value must be non-negative"):
            little_endian_to_hex(-1, 4)

        # Завелике значення для заданої кількості байтів
        # Це має працювати (береться останні байти)
        result = hex_to_little_endian("1234567890", 2)
        expected = hex_to_little_endian("5678", 2)
        assert result == expected

    def test_different_byte_sizes(self):
        """Тестування різних розмірів байтів."""
        test_cases = [
            ("FF", 1, 255, 255),
            ("AABB", 2, 43707, 48059),  # Little: 0xBBAA = 48059, Big: 0xAABB = 43707
            ("123456", 3, 4279383, 5635926),  # Little: 0x563412 = 5650450, Big: 0x123456 = 1193046
            ("11223344", 4, 1144201745, 287454020),  # Little: 0x44332211, Big: 0x11223344
        ]

        for hex_str, num_bytes, expected_le, expected_be in test_cases:
            le_result = hex_to_little_endian(hex_str, num_bytes)
            be_result = hex_to_big_endian(hex_str, num_bytes)

            assert le_result == expected_le, \
                f"Little-endian failed for {hex_str}: expected {expected_le}, got {le_result}"
            assert be_result == expected_be, \
                f"Big-endian failed for {hex_str}: expected {expected_be}, got {be_result}"

if __name__ == "__main__":
    pytest.main([__file__, "-v"])