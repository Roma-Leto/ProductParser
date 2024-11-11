import pytest
from aioresponses import aioresponses
from parsers.site1_parser import Site1Parser
from parsers.site2_parser import Site2Parser


@pytest.mark.asyncio
async def test_site1_parser():
    url = "https://site1.com/products"
    parser = Site1Parser(url)

    # Мокаем запрос
    with aioresponses() as m:
        m.get(url,
              body="<html><body><div class='product'><h3>Product 1</h3>"
                   "<span class='price'>$10</span></div></body></html>",
              status=200)

        # Асинхронно получаем HTML
        await parser.get_html(m._session)

        # Парсим и проверяем данные
        data = parser.parse_data()
        assert len(data) == 1
        assert data[0]['title'] == "Product 1"
        assert data[0]['price'] == "$10"

        # Проверяем логирование
        with open('parser.log', 'r') as log_file:
            logs = log_file.read()
            assert "Загружаем страницу: https://site1.com/products" in logs
            assert "Парсинг завершен для https://site1.com/products" in logs


@pytest.mark.asyncio
async def test_site2_parser():
    url = "https://site2.com/products"
    parser = Site2Parser(url)

    # Мокаем запрос
    with aioresponses() as m:
        m.get(url,
              body="<html><body><div class='item'><span class='product-name'>"
                   "Product 2</span><span class='product-price'>$20</span>"
                   "</div></body></html>",
              status=200)

        # Асинхронно получаем HTML
        await parser.get_html(m._session)

        # Парсим и проверяем данные
        data = parser.parse_data()
        assert len(data) == 1
        assert data[0]['title'] == "Product 2"
        assert data[0]['price'] == "$20"

        # Проверяем логирование
        with open('parser.log', 'r') as log_file:
            logs = log_file.read()
            assert "Загружаем страницу: https://site2.com/products" in logs
            assert "Парсинг завершен для https://site2.com/products" in logs
