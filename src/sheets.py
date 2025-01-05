"""Модуль для работы с Google Sheets.

Предоставляет функции для получения данных из Google таблиц.
"""

import gspread
from gspread_dataframe import get_as_dataframe
from google.oauth2.service_account import Credentials

from .config import config
from .utils import print_status

def get_sheet_data(sheet_url: str, sheet_name: str):
    """Получает данные из Google таблицы.

    Args:
        sheet_url (str): URL таблицы
        sheet_name (str): Название листа

    Returns:
        DataFrame: Данные из таблицы
    """
    
    print_status("Подключение к Google Sheets...", "PROCESSING")
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = Credentials.from_service_account_file(config.credentials_path, scopes=scope)
    client = gspread.authorize(creds)
    
    sheet = client.open_by_url(sheet_url)
    worksheet = sheet.worksheet(sheet_name)
    
    return get_as_dataframe(worksheet)