"""Вспомогательные функции для проекта.

Содержит утилиты для вывода статусов и проверки url.
"""

from colorama import Fore, Style

def print_status(message: str, status: str = "INFO") -> None:
    """Выводит форматированное сообщение о статусе.

    Args:
        message (str): Текст сообщения
        status (str): Тип статуса (INFO/SUCCESS/ERROR/PROCESSING)
    """
    
    status_colors = {
        "INFO": Fore.BLUE,
        "SUCCESS": Fore.GREEN,
        "ERROR": Fore.RED,
        "PROCESSING": Fore.YELLOW
    }
    print(f"{status_colors[status]}[{status}]{Style.RESET_ALL} {message}")

def is_playlist(url: str) -> bool:
    """Проверяет, является ли URL плейлистом.

    Args:
        url (str): URL для проверки

    Returns:
        bool: True если это плейлист, False если отдельное видео
    """
    return 'playlist' in url.lower()