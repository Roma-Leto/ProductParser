import asyncio
from parsers.base_parser import BaseParser
from parsers.site1_parser import Site1Parser
from aiohttp import ClientSession


async def parse_site(parser: BaseParser, session: ClientSession):
    """
    Асинхронно загружает HTML-страницу с использованием переданного парсера,
    парсит данные и сохраняет их.

    :param parser: Парсер для конкретного сайта (наследник BaseParser).
    :param session: Объект ClientSession для выполнения HTTP-запросов.
    """
    try:
        await parser.get_html(session)  # Асинхронно загружаем HTML
        data = parser.parse_data()  # Парсим данные
        parser.save_data(data)  # Сохраняем/выводим данные
    except Exception as e:
        print(f"Ошибка при парсинге {parser.url}: {e}")


async def main():
    """
    Главная асинхронная функция, которая инициализирует парсеры и выполняет
    асинхронное парсинг всех указанных сайтов.
    """
    # Указываем URL для парсинга
    url1 = "https://magnit.ru/catalog"

    # Создаем парсер для сайта
    parsers = [Site1Parser(url1)]

    # Используем aiohttp для асинхронных HTTP-запросов
    async with ClientSession() as session:
        tasks = [parse_site(parser, session) for parser in parsers]
        await asyncio.gather(
            *tasks)  # Параллельный запуск парсинга для всех сайтов


if __name__ == "__main__":
    """
    Запуск асинхронной функции main() при запуске скрипта.
    """
    asyncio.run(main())  # Запуск асинхронной главной функции
