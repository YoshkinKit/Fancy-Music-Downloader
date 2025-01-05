# Fancy Music Downloader

A program to automatically download and process music from YouTube using data from Google Sheets

## Features

- Download audio from YouTube
- Convert to MP3 format
- Automatically add metadata (author, album, title)
- Add album cover image
- Google Sheets integration for batch processing
- Informative output of processing status

## Requirements

- Python 3.12+
- Poetry
- Google Sheets API credentials

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/YoshkinKit/Fancy-Music-Downloader.git
   cd Fancy-Music-Downloader
   ```
2. Install dependencies using Poetry:
   ```bash
   poetry install
   ```
3. Create an `.env` file in the root directory:
   ```
   SHEET_URL=https://docs.google.com/spreadsheets/d/your-sheet-id/edit
   SHEET_NAME=Sheet1
   DOWNLOAD_PATH=Music
   CREDENTIALS_PATH=credentials.json
    ```
4. Put the Google Sheets API credentials file (credentials.json) in the root directory

## Project Structure

```
Fancy-Music-Downloader/
├── src/
│   ├── __init__.py
│   ├── config.py        # App configuration
│   ├── converter.py     # Audio converting
│   ├── downloader.py    # YouTube download
│   ├── metadata.py      # Metadata handling
│   ├── sheets.py        # Google Sheets handling
│   └── utils.py         # Utils functions
├── .env                 # Environment variables
├── credentials.json     # Google API credentials
├── pyproject.toml       # Poetry configuration
├── poetry.lock          # Poetry lock-file
├── README.md
└── main.py              # Entry point
```

## Configuration

Settings in the `.env` file:
- `SHEET_URL`: The URL of your Google Sheet
- `SHEET_NAME`: The name of the data sheet
- `DOWNLOAD_PATH`: Path to save files (default is "Music")
- `CREDENTIALS_PATH`: Path to the Google API credentials file (default is "credentials.json")

## Google Sheet Setup

1. Create a spreadsheet with the following columns:
   - URL: link to YouTube video
   - Author: artist
   - Album: album title
   - CoverURL: link to album cover image (or "-" if not required)
2. Grant access to the spreadsheet using the service account from credentials.json

## Usage

1. Fill a Google spreadsheet with music data
2. Run the program with Poetry:
   ```bash
   poetry run python main.py
   ```