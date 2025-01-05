"""Модуль для скачивания аудио с YouTube.

Предоставляет функции для загрузки аудио с YouTube.
"""

from pytubefix import YouTube, Playlist

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

def download_playlist(url: str) -> list[tuple[str, str]]:
    """Скачивает все видео из плейлиста.

    Args:
        url (str): URL плейлиста YouTube

    Returns:
        list[tuple[str, str]]: Список кортежей (путь_к_файлу, название_видео)
    """
    
    print_status("Получение информации о плейлисте...", "PROCESSING")
    playlist = Playlist(url)
    results = []

    for video in playlist.videos:
        try:
            print_status(f"Обработка видео: {video.title}", "PROCESSING")
            stream = video.streams.filter(only_audio=True).first()
            out_file = stream.download(config.download_path)
            results.append((out_file, video.title))
        except Exception as e:
            print_status(f"Ошибка при обработке {video.title}: {str(e)}", "ERROR")
            continue

    return results