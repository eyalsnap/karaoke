import numpy as np


def cut_song_by_time(song, start_time, end_time):
    start_bit = int(np.floor(start_time * song.fs))
    end_bit = int(np.ceil(end_time * song.fs))
    return cut_song_by_bits(song, start_bit, end_bit)


def cut_song_by_start_time(song, start_time):
    start_bit = int(np.floor(start_time * song.fs))
    return cut_song_by_start_bits(song, start_bit)


def cut_song_by_end_time(song, end_time):
    end_bit = int(np.floor(end_time * song.fs))
    return cut_song_by_end_bits(song, end_bit)


def cut_song_by_bits(song, start_bit, end_bit):
    return song.fs, song.data[start_bit:end_bit, :]


def cut_song_by_start_bits(song, start_bit):
    return song.fs, song.data[start_bit:, :]


def cut_song_by_end_bits(song, end_bit):
    return song.fs, song.data[:end_bit, :]

