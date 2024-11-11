import asyncio

from parsers.base_parser import BaseParser
from parsers.site1_parser import Site1Parser
from parsers.site2_parser import Site2Parser
from aiohttp import ClientSession


async def parse_site(parser: BaseParser, session: ClientSession):
    try:
        await parser.get_html(session)  # Асинхронно загружаем HTML
        data = parser.parse_data()  # Парсим данные
        parser.save_data(data)  # Сохраняем/выводим данные
    except Exception as e:
        print(f"Ошибка при парсинге {parser.url}: {e}")


async def main():
    # Указываем URL для парсинга
    url1 = "https://site1.com/products"
    url2 = "https://site2.com/products"

    # Создаем парсеры для сайтов
    parsers = [Site1Parser(url1), Site2Parser(url2)]

    # Используем aiohttp для асинхронных HTTP-запросов
    async with ClientSession() as session:
        tasks = [parse_site(parser, session) for parser in parsers]
        await asyncio.gather(
            *tasks)  # Параллельный запуск парсинга для всех сайтов


if __name__ == "__main__":
    asyncio.run(main())  # Запуск асинхронной главной функции
