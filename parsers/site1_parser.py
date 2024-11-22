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
            clean_price = re.findall(r'\d+\.\d+',price)[0]
            products.append({'title': title, 'price': clean_price})

        logger.info(
            f"Парсинг завершен для {self.url}, найдено {len(products)} товаров")
        return products

    def save_data(self, data):
        if not data:
            logger.warning(f"Нет данных для сохранения на {self.url}")
        for product in data:
            logger.info(
                f"Product: {product['title']}, Price: ₽{product['price']}")
