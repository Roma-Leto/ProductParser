import re
import sqlite3
from datetime import datetime
from bs4 import BeautifulSoup
from parsers.base_parser import BaseParser
from parsers.utils.logger import logger


class Site1Parser(BaseParser):
    async def get_html(self, session):
        # Используем общий метод для получения HTML
        await self.fetch_html(session)

    def parse_data(self):
        if not self.html:
            logger.error(f"HTML не загружен для {self.url}")
            raise Exception("HTML не загружен")

        logger.info(f"Парсим данные с сайта: {self.url}")
        soup = BeautifulSoup(self.html, 'html.parser')
        products = []
        # Парсинг списка продуктов
        for product in soup.find_all(
                'div',
                class_='unit-catalog-product-preview-text'):
            title = product.find(
                'div',
                class_='pl-text unit-catalog-product-preview-title').text
            price = product.find(
                'span',
                {'data-v-de2089e9': ''}).get_text()
            # Извлекаем только цифры
            clean_price = re.findall(r'\d+\.\d+', price)[0]
            products.append({'title': title, 'price': clean_price})

        logger.info(
            f"Парсинг завершен для {self.url}, "
            f"найдено {len(products)} товаров")
        return products

    def save_data(self, data):
        """
        Функция сохранения извлечённых данных в базу данных SQLite
        """
        if not data:
            logger.warning(f"Нет данных для сохранения на {self.url}")

        # Создать подключение к базе данных (создание файла БД).
        self.db_name = self.url.split('/')[2] + '.sqlite'
        connection = sqlite3.connect(self.db_name)
        logger.info(f"Подключение к базе данных {self.db_name}")
        cursor = connection.cursor()
        # Создать таблицу, если она еще не существует.
        cursor.execute("""
                    CREATE TABLE IF NOT EXISTS products(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT NOT NULL,
                        price REAL NOT NULL,
                        date TEXT NOT NULL,
                        UNIQUE(title, date)
                    )
                """)

        for product in data:
            logger.info(
                f"Product: {product['title']}, Price: ₽{product['price']}")
            # Вставить данные в таблицу.
            if 'title' in product and 'price' in product:
                # Получаем текущую дату без времени
                current_date = datetime.now().strftime('%d-%m-%Y')

                try:
                    # Пытаемся вставить данные в таблицу
                    cursor.execute("""
                                    INSERT INTO products (title, price, date) 
                                    VALUES (?, ?, ?)
                                """, (
                    product['title'], product['price'], current_date))
                except sqlite3.IntegrityError:
                    # Если комбинация title и date уже существует, пропускаем
                    logger.warning(
                        f"Продукт '{product['title']}' на дату {current_date} уже существует.")
            else:
                logger.warning(f"Недостающие данные для продукта: {product}")

        # Сохранение изменений в базе данных
        connection.commit()

        # Закрытие подключения
        connection.close()
        logger.info(f"Данные успешно сохранены в базе данных {self.db_name} "
                    f"на {self.url}")

