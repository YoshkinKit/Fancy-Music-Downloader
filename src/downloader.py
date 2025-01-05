"""Модуль для скачивания аудио с YouTube.

Предоставляет функции для загрузки аудио с YouTube.
"""

from pytubefix import YouTube

from .config import config
from .utils import print_status

def download_audio(url: str) -> tuple[str, str]:
    """Скачивает аудио с YouTube.

    Args:
        url (str): URL видео на YouTube

    Returns:
        tuple[str, str]: Кортеж (путь_к_файлу, название_видео)
    """

    print_status("Получение аудиопотока...", "PROCESSING")
    yt = YouTube(url)
    video = yt.streams.filter(only_audio=True).first()
    
    out_file = video.download(config.download_path)
    
    return out_file, yt.title