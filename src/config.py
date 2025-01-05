"""Модуль конфигурации приложения.

Загружает настройки из переменных окружения и предоставляет их через класс Config.
"""

import os

from dotenv import load_dotenv

class Config:
    """Класс конфигурации приложения.

    Attributes:
        sheet_url (str): URL Google таблицы
        sheet_name (str): Название листа
        download_path (str): Путь для сохранения файлов
        credentials_path (str): Путь к файлу учетных данных Google API
    """
    
    def __init__(self):
        load_dotenv()
        self.sheet_url = os.getenv("SHEET_URL")
        self.sheet_name = os.getenv("SHEET_NAME")
        self.download_path = os.getenv("DOWNLOAD_PATH", "Music")
        self.credentials_path = os.getenv("CREDENTIALS_PATH", "credentials.json")

    @classmethod
    def load(cls) -> 'Config':
        return cls()

config = Config.load()