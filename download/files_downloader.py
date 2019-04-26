import re
import os

from download.downloader import download_by_song_object
from download.song import Song


def download_by_files_path(hebrew_file_path, english_file_path):

    with open(english_file_path, 'r') as f:
        english_lines = f.readlines()

    with open(hebrew_file_path, 'r', encoding="utf8") as f:
        hebrew_lines = f.readlines()

    # running over all the singers
    for hebrew_singer_line, english_singer_line in zip(hebrew_lines, english_lines):

        hebrew_singer, hebrew_songs = extract_singer_and_song(hebrew_singer_line)
        english_singer, english_songs = extract_singer_and_song(english_singer_line)

        # running over all the songs
        for hebrew_song, english_song in zip(hebrew_songs, english_songs):
            song = Song(hebrew_singer, hebrew_song, english_singer, english_song)
            print(f'now download: {english_singer} - {english_song}')
            download_by_song_object(song)


def extract_singer_and_song(hebrew_name):
    hebrew_name = re.sub('\n', '', hebrew_name)
    parts = hebrew_name.split(':')
    hebrewSinger = parts[0]
    hebrewSongs = parts[1].split(',')
    return hebrewSinger, hebrewSongs


if __name__ == '__main__':

    currentFolder = os.getcwd()

    hebrew_names_path = os.path.join(currentFolder, "hebrew_names.txt")
    english_names_path = os.path.join(currentFolder, "english_names.txt")

    download_by_files_path(hebrew_names_path, english_names_path)
