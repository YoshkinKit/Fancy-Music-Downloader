import os
import requests
from pytubefix import YouTube
from pydub import AudioSegment

from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, APIC

import gspread
from gspread_dataframe import get_as_dataframe
from google.oauth2.service_account import Credentials

def download_and_convert(url: str, author: str, album: str, cover_url: str) -> None:
    yt = YouTube(url)
    
    video = yt.streams.filter(only_audio=True).first()
    out_file = video.download("Music")

    base = os.path.splitext(out_file)[0]
    
    new_file = base + '.mp3'
    audio = AudioSegment.from_file(out_file)
    audio.export(new_file, format='mp3')
    
    os.remove(out_file)

    audiofile = EasyID3(new_file)
    audiofile['title'] = yt.title
    audiofile['artist'] = author
    audiofile['album'] = album
    audiofile.save()

    if str(cover_url) != '-':
        response = requests.get(cover_url)
        audiofile = ID3(new_file)
        audiofile.add(APIC(
            encoding=3,
            mime='image/jpeg',
            type=3,
            data=response.content
        ))
        audiofile.save()
    
    print(f"Скачано и конвертировано: {new_file}")

def process_google_sheet(sheet_url: str, sheet_name: str) -> None:
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = Credentials.from_service_account_file("credentials.json", scopes=scope)
    client = gspread.authorize(creds)
    
    sheet = client.open_by_url(sheet_url)
    worksheet = sheet.worksheet(sheet_name)
    
    df = get_as_dataframe(worksheet)

    for index, row in df.iterrows():
        url = row['URL']
        author = row['Author']
        album = row['Album']
        cover_url = row["CoverURL"]
        download_and_convert(url, author, album, cover_url)

if __name__ == "__main__":
    sheet_url = 'https://docs.google.com/spreadsheets/d/1buhff7T8gzYbDPgQeOGI8hKC5fhenr4FC9tFRd7SYEk/edit'
    sheet_name = 'Music'
    process_google_sheet(sheet_url, sheet_name)