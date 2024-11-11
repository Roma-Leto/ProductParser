from abc import ABC, abstractmethod
from aiohttp import ClientSession
from parsers.utils.logger import logger


class BaseParser(ABC):
    def __init__(self, url: str):
        self.url = url
        self.html = None

    @abstractmethod
    async def get_html(self, session: ClientSession):
        """Метод для получения HTML-страницы"""
        pass

    @abstractmethod
    def parse_data(self):
        """Метод для парсинга данных из HTML"""
        pass

    @abstractmethod
    def save_data(self, data):
        """Метод для сохранения или обработки парсенных данных"""
        pass

    async def fetch_html(self, session: ClientSession):
        """Асинхронный метод для загрузки HTML"""
        try:
            logger.info(f"Загружаем страницу: {self.url}")
            async with session.get(self.url) as response:
                if response.status == 200:
                    self.html = await response.text()
                    logger.info(f"Страница успешно загружена: {self.url}")
                else:
                    logger.error(
                        f"Ошибка загрузки страницы {self.url}: {response.status}")
                    raise Exception(f"Ошибка при запросе страницы: {self.url}")
        except Exception as e:
            logger.error(f"Ошибка при запросе {self.url}: {str(e)}")
            raise e
