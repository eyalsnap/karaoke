import os

from constants.parameters.filenames_parameters import aligned_karaoke_name, aligned_song_name
from couple_creation.song_correlation import wave_correlation
from couple_creation.song_metadata import SongMetadata
from utils.directories_function import find_song_and_karaoke_name


class SongCouple:

    def __init__(self, directory):

        self.directory = directory

        self.karaoke_name, self.song_name = find_song_and_karaoke_name(directory)

        self.karaoke = SongMetadata(os.path.join(self.directory, self.karaoke_name))
        self.song = SongMetadata(os.path.join(self.directory, self.song_name))

        self.translation = None
        self.aligned_karaoke = None
        self.aligned_song = None

    def align_audio(self):

        self.translation = wave_correlation(self.song, self.karaoke)

        self.karaoke.aligned_song(-self.translation, self.song.get_length())
        self.song.aligned_song(self.translation, self.karaoke.get_length())

    def save_aligned_audio(self):
        self.karaoke.save_song(aligned_karaoke_name)
        self.song.save_song(aligned_song_name)
