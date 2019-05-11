from scipy.io import wavfile
import cv2

from couple_creation.song_cutter_utils import cut_song_by_bits


class SongMetadata:

    def __init__(self, path):
        self.path = path
        self.fs, self.data = wavfile.read(path)

    def get_length(self):
        return self.data.shape[0]
        # return self.data.shape[0] / self.fs

    def song_transfer(self, song2, time):
        bit = time * self.fs
        new_song = song2.data
        new_song.setflags(write=1)
        new_song[:bit, :] = self.data[:bit, :]
        return self.fs, new_song

    def pad_song(self, start=0, end=0):
        start_bits = start * self.fs
        end_bits = end * self.fs
        return cv2.copyMakeBorder(
            src=self.data,
            top=start_bits,
            bottom=end_bits,
            left=0,
            # left=bits,
            right=0,
            borderType=cv2.BORDER_CONSTANT)

    def aligned_song(self, translation, other_song_length):
        start = max(0, translation)
        end = min(self.get_length(), other_song_length + translation)
        self.fs, self.data = cut_song_by_bits(self, start, end)

    def save_song(self, new_name):
        dirs = self.path.split('\\')
        dirs[-1] = new_name
        new_path = '\\'.join(dirs)
        wavfile.write(new_path, self.fs, self.data)
