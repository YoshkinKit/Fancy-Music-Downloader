"""Модуль для конвертации аудио файлов.

Предоставляет функции для конвертации аудио файлов в MP3 формат.
"""

import os

from pydub import AudioSegment

from .utils import print_status

def convert_to_mp3(input_file: str) -> str:
    """Конвертирует аудио файл в формат MP3.

    Args:
        input_file (str): Путь к входному файлу

    Returns:
        str: Путь к сконвертированному MP3 файлу
    """
    
    print_status("Конвертация в MP3...", "PROCESSING")
    base = os.path.splitext(input_file)[0]
    output_file = base + '.mp3'

    audio = AudioSegment.from_file(input_file)
    audio.export(output_file, format='mp3')
    
    os.remove(input_file)
    return output_file