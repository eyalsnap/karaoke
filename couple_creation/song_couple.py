import os

from couple_creation.song_metadata import SongMetadata
from utils.directories_function import find_song_and_karaoke_name


class SongCouple:

    def __init__(self, directory):

        self.directory = directory

        self.karaoke_name, self.song_name = find_song_and_karaoke_name(directory)

        self.karaoke = SongMetadata(os.path.join(self.directory, self.karaoke_name))
        self.song = SongMetadata(os.path.join(self.directory, self.song_name))
