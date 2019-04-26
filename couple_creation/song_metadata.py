from mutagen.mp3 import MP3
import re
from scipy.io import wavfile
import numpy as np


class SongMetadata:

    def __init__(self, path):
        self.path = path
        self.fs, self.data = wavfile.read(path)

    def get_length(self):
        audio = MP3(re.sub('wav', 'mp3', self.path))
        return audio.info.length

    def cut_song_by_time(self, start_time, end_time):
        start_bit = int(np.floor(start_time * self.fs))
        end_bit = int(np.ceil(end_time * self.fs))
        return self.cut_song_by_bits(start_bit, end_bit)

    def cut_song_by_bits(self, start_bit, end_bit):
        return self.fs, self.data[start_bit:end_bit, :]

    def cut_song_by_start_bits(self, start_bit):
        return self.fs, self.data[start_bit:, :]

    def song_transfer(self, song2, time):
        bit = time * self.fs
        new_song = song2.data
        new_song.setflags(write=1)
        new_song[:bit, :] = self.data[:bit, :]
        return self.fs, new_song
