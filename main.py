from colorama import init

from src.config import config
from src.utils import print_status
from src.sheets import get_sheet_data
from src.converter import convert_to_mp3
from src.downloader import download_audio
from src.metadata import add_metadata, add_cover

def process_track(url: str, author: str, album: str, cover_url: str) -> None:
    """Обрабатывает один трек.

    Args:
        url (str): URL видео на YouTube
        author (str): Исполнитель
        album (str): Название альбома
        cover_url (str): URL обложки
    """
    
    try:
        input_file, title = download_audio(url)
        output_file = convert_to_mp3(input_file)
        add_metadata(output_file, title, author, album)
        add_cover(output_file, cover_url)
        print_status(f"Успешно обработано: {title}", "SUCCESS")
    except Exception as e:
        print_status(f"Ошибка при обработке {url}: {str(e)}", "ERROR")

def main():
    init()

    print_status("Начало работы программы", "INFO")

    df = get_sheet_data(config.sheet_url, config.sheet_name)
    print_status(f"Найдено {len(df)} треков для обработки", "INFO")

    for i, row in df.iterrows():
        print_status(f"Обработка трека {i + 1}/{len(df)}", "INFO")
        process_track(row['URL'], row['Author'], row['Album'], row['CoverURL'])

    print_status("Работа программы завершена", "SUCCESS")

if __name__ == "__main__":
    main()