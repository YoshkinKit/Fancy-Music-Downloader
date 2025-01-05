"""Модуль для работы с метаданными аудио файлов.

Предоставляет функции для добавления метаданных и обложек к MP3 файлам.
"""

import requests

from mutagen.id3 import ID3, APIC
from mutagen.easyid3 import EasyID3

from .utils import print_status

def add_metadata(file_path: str, title: str, author: str, album: str) -> None:
    """Добавляет метаданные к MP3 файлу.

    Args:
        file_path (str): Путь к MP3 файлу
        title (str): Название трека
        author (str): Исполнитель
        album (str): Название альбома
    """
    
    print_status("Добавление метаданных...", "PROCESSING")
    audiofile = EasyID3(file_path)
    audiofile['title'] = title
    audiofile['artist'] = author
    audiofile['album'] = album
    audiofile.save()

def add_cover(file_path: str, cover_url: str) -> None:
    """Добавляет обложку к MP3 файлу.

    Args:
        file_path (str): Путь к MP3 файлу
        cover_url (str): URL изображения обложки
    """
    
    if str(cover_url) != '-':
        print_status("Добавление обложки...", "PROCESSING")
        response = requests.get(cover_url)
        audiofile = ID3(file_path)
        audiofile.add(APIC(
            encoding=3,
            mime='image/jpeg',
            type=3,
            data=response.content
        ))
        audiofile.save()