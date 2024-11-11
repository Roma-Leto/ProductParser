# Product Parser

**Product Parser** — это асинхронный парсер для извлечения данных о продуктах с различных сайтов продуктовых магазинов. Проект использует асинхронное программирование с помощью библиотеки `asyncio` и выполняет параллельные HTTP-запросы с использованием `aiohttp`. Логирование осуществляется через стандартную библиотеку `logging`, а для тестирования используется `pytest`.

### Основные особенности:
- **Асинхронность**: Параллельный парсинг данных с нескольких сайтов.
- **Логирование**: Все этапы работы парсера логируются в файл.
- **Тестирование**: Тестирование с использованием `pytest` и мокирования HTTP-запросов.
- **Расширяемость**: Легкость добавления новых парсеров для других сайтов.

---

## Установка и настройка

1. **Клонировать репозиторий**:
    ```bash
    git clone https://github.com/yourusername/product-parser.git
    cd product-parser
    ```

2. **Создать виртуальное окружение и установить зависимости**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # Для Linux/macOS
    venv\Scripts\activate     # Для Windows
    pip install -r requirements.txt
    ```

---

## Запуск парсинга

1. **Запуск парсинга всех сайтов**:
    Для запуска парсинга с сайта используйте команду:
    ```bash
    python main.py
    ```
    Это запустит парсинг для всех сайтов, добавленных в `main.py`.

2. **Просмотр логов**:
    Логи работы парсера сохраняются в файл `parser.log`. Логи также выводятся в консоль. Это поможет вам отслеживать успехи и возможные ошибки.

---

## Добавление нового парсера

Чтобы добавить новый парсер для другого сайта, выполните следующие шаги:

1. Создайте новый класс, который наследуется от `BaseParser` в файле `parsers/`:
```python
from parsers.base_parser import BaseParser
from bs4 import BeautifulSoup

class NewSiteParser(BaseParser):
    async def get_html(self, session):
        await self.fetch_html(session)

    def parse_data(self):
        soup = BeautifulSoup(self.html, 'html.parser')
        products = []
        for product in soup.find_all('div', class_='product-item'):
            title = product.find('h2').text
            price = product.find('span', class_='product-price').text
            products.append({'title': title, 'price': price})
        return products

    def save_data(self, data):
        for product in data:
            print(f"Product: {product['title']}, Price: {product['price']}")
```

2. В файле `main.py` добавьте новый парсер в список сайтов для обработки:
```python
import asyncio
from new_site_parser import NewSiteParser
from aiohttp import ClientSession

async def main():
    url = "https://newsite.com/products"
    
   
    # Создаем парсеры для сайтов
    parsers = [NewSiteParser(url)]

    # Используем aiohttp для асинхронных HTTP-запросов
    async with ClientSession() as session:
        tasks = [parse_site(parser, session) for parser in parsers]
        await asyncio.gather(
            *tasks)  # Параллельный запуск парсинга для всех сайтов

if __name__ == "__main__":
    asyncio.run(main())
```

3. Теперь, когда вы добавите новый парсер и запустите `main.py`, он начнёт обрабатывать новый сайт.

---

## Логирование

Проект использует библиотеку `logging` для логирования действий парсера. Логи пишутся в файл `parser.log` и выводятся в консоль.

Пример логов:
```
2024-11-11 10:00:00,123 - product_parser - INFO - Загружаем страницу: https://site1.com/products
2024-11-11 10:00:02,456 - product_parser - INFO - Страница успешно загружена: https://site1.com/products
2024-11-11 10:00:03,789 - product_parser - INFO - Парсинг завершен для https://site1.com/products, найдено 15 товаров
```

---

## Тестирование

Для тестирования проекта используется библиотека `pytest`. Тесты проверяют корректность работы парсеров и логирование. Для мокирования HTTP-запросов используется библиотека `aioresponses`.

1. **Запуск тестов**:
    Для запуска тестов используйте команду:
    ```bash
    pytest
    ```

2. **Тесты проверяют**:
   - Правильность парсинга данных с различных сайтов.
   - Логирование успешных и ошибочных операций.

Пример теста:

```python
from aioresponses import aioresponses
from parsers.site1_parser import Site1Parser
import pytest


@pytest.mark.asyncio
async def test_site1_parser():
    url = "https://site1.com/products"
    parser = Site1Parser(url)

    # Мокаем запрос
    with aioresponses() as m:
        m.get(url,
              body="<html><body><div class='product'><h3>Product 1</h3><span class='price'>$10</span></div></body></html>",
              status=200)

        # Асинхронно получаем HTML
        await parser.get_html(m._session)

        # Парсим и проверяем данные
        data = parser.parse_data()
        assert len(data) == 1
        assert data[0]['title'] == "Product 1"
        assert data[0]['price'] == "$10"
```

---

## Структура проекта

```
product-parser/
├── parsers/
│   ├── __init__.py
│   ├── base_parser.py   # Абстрактный парсер для всех сайтов
│   ├── site1_parser.py  # Парсер для сайта 1
│   ├── site2_parser.py  # Парсер для сайта 2
│   └── utils/
│       ├── __init__.py
│       └── logger.py    # Логирование
├── tests/               # Тесты проекта
│   ├── test_parsers.py  # Тесты для парсеров
├── main.py              # Основной файл для запуска парсинга
├── requirements.txt     # Список зависимостей
└── README.md            # Описание проекта
```

---

## Требования

Проект использует следующие библиотеки:

- `aiohttp` — асинхронные HTTP-запросы.
- `BeautifulSoup4` — парсинг HTML.
- `asyncio` — асинхронное выполнение задач.
- `pytest` — для тестирования.
- `aioresponses` — для мокирования HTTP-запросов.

---

## Лицензия

Этот проект распространяется под лицензией **MIT**. Подробности см. в файле [LICENSE](LICENSE).

---

**Спасибо, что используете этот проект! Если у вас есть предложения или вопросы, не стесняйтесь обратиться через [Issues](https://github.com/yourusername/product-parser/issues).**
