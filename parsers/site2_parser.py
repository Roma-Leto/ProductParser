from bs4 import BeautifulSoup
from parsers.base_parser import BaseParser
from parsers.utils.logger import logger


class Site2Parser(BaseParser):
    async def get_html(self, session):
        await self.fetch_html(
            session)  # Используем общий метод для получения HTML

    def parse_data(self):
        if not self.html:
            logger.error(f"HTML не загружен для {self.url}")
            raise Exception("HTML не загружен")

        logger.info(f"Парсим данные с сайта: {self.url}")
        soup = BeautifulSoup(self.html, 'html.parser')
        products = []
        # Парсинг списка продуктов
        for product in soup.find_all('div', class_='item'):
            title = product.find('span', class_='product-name').text
            price = product.find('span', class_='product-price').text
            products.append({'title': title, 'price': price})

        logger.info(
            f"Парсинг завершен для {self.url}, найдено {len(products)} товаров")
        return products

    def save_data(self, data):
        if not data:
            logger.warning(f"Нет данных для сохранения на {self.url}")
        for product in data:
            logger.info(
                f"Product: {product['title']}, Price: {product['price']}")
