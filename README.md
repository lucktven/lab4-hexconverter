# Увімкніть віртуальне середовище (опціонально)
python -m venv venv
# Windows: venv\Scripts\activate
# Linux/Mac: source venv/bin/activate

# Встановіть залежності
pip install -r requirements.txt

# Запустіть демонстрацію
python src/main.py

# Запустіть тести
python -m pytest tests/test_converter.py -v