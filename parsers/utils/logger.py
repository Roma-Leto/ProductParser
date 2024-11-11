import logging


def setup_logger():
    """
    Настройка логгера для проекта парсера.

    Этот метод создаёт логгер с именем 'product_parser', устанавливает уровень
    логирования, добавляет обработчики для записи логов в файл и вывода
    в консоль.

    Логи сохраняются в файл 'parser.log', а также выводятся в консоль с разными
    уровнями важности.

    Возвращает:
        logger (logging.Logger): Настроенный логгер.
    """

    # Получаем логгер с именем 'product_parser'
    logger = logging.getLogger('product_parser')

    # Устанавливаем уровень логирования для логгера - DEBUG,
    # что позволяет записывать все логи, начиная с уровня DEBUG
    # (включая INFO, WARNING, ERROR и CRITICAL)
    logger.setLevel(logging.DEBUG)

    # Создаем обработчик для записи логов в файл 'parser.log'
    file_handler = logging.FileHandler('parser.log')

    # Устанавливаем уровень логирования для этого обработчика - DEBUG
    # Это означает, что все логи уровня DEBUG и выше будут записываться в файл
    file_handler.setLevel(logging.DEBUG)

    # Создаем формат для логов, который будет использоваться как для файлового,
    # так и для консольного обработчика
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Устанавливаем форматирование для файлового обработчика
    file_handler.setFormatter(formatter)

    # Создаем обработчик для вывода логов в консоль
    console_handler = logging.StreamHandler()

    # Устанавливаем уровень логирования для консольного обработчика - INFO,
    # что значит, что в консоль будут выводиться только логи уровня INFO и выше (не DEBUG)
    console_handler.setLevel(logging.INFO)

    # Устанавливаем форматирование для консольного обработчика
    console_handler.setFormatter(formatter)

    # Добавляем оба обработчика к логгеру:
    # - file_handler будет записывать логи в файл 'parser.log'
    # - console_handler будет выводить логи в консоль
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    # Возвращаем настроенный логгер
    return logger


# Получаем настроенный логгер
logger = setup_logger()
