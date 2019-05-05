import re
import os


class Song:

    def __init__(self, hebrew_singer, hebrew_song, english_singer, english_song):
        self.singer_hebrew = hebrew_singer
        self.song_hebrew = hebrew_song
        self.singer_english = english_singer
        self.song_english = english_song

        self.song_url = None
        self.karaoke_url = None
        self.download_dir = None

    def get_download_dir(self, basic_directory):
        self.download_dir = os.path.join(basic_directory, self.get_song_file_name())
        return self.download_dir

    def get_song_file_name(self):
        return re.sub(' ', '_', self.singer_english) + '_' + \
               re.sub(' ', '_', self.song_english)

    def set_download_urls(self, song_url, karaoke_url):
        self.song_url = song_url
        self.karaoke_url = karaoke_url

    def print_me(self):
        print(f'hebrew_singer : {self.singer_hebrew} - '
              f'hebrew_song : {self.song_hebrew} - '
              f'english_singer : {self.singer_english} - '
              f'english_song : {self.song_english}')
