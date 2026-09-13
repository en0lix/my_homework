"""
Общий модуль инициализации пакета src.
"""

import logging
import sys
from pathlib import Path

# Создание папки для логов
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)


# Настройка корневого логгера
def setup_logging():
    """Настройка логирования для всего проекта."""
    # Создаем корневой логгер
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)

    # Очищаем существующие обработчики
    root_logger.handlers.clear()

    # Создаем форматтер
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Создаем обработчик для записи в файл
    file_handler = logging.FileHandler(
        LOG_DIR / 'app.log',
        mode='w',
        encoding='utf-8'
    )
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    # Создаем обработчик для вывода в консоль
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    # Добавляем обработчики к корневому логгеру
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)

    return root_logger


# Инициализируем логирование при импорте
logger = setup_logging()
logger.info("Приложение запущено")