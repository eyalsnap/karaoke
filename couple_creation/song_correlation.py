import numpy as np
import cv2

from constants.parameters.number_parameter import KARAOKE_PREFIX_TIME, PAD_SONG_TIME, MATCH_TEMPLATE_METHOD
from couple_creation.song_cutter_utils import cut_song_by_end_time


def wave_correlation(song, karaoke):

    _, short_karaoke_data = cut_song_by_end_time(karaoke, KARAOKE_PREFIX_TIME)
    padded_song_data = song.pad_song(start=PAD_SONG_TIME, end=PAD_SONG_TIME)

    short_karaoke_data = prepare_data_for_cv2_correlation(short_karaoke_data)
    padded_song_data = prepare_data_for_cv2_correlation(padded_song_data)

    correlation_map = cv2.matchTemplate(padded_song_data, short_karaoke_data, method=eval(MATCH_TEMPLATE_METHOD))
    max_index = np.argmax(correlation_map)

    time_translation = max_index - song.fs * PAD_SONG_TIME

    return time_translation


def prepare_data_for_cv2_correlation(song):
    song.astype(np.float32)
    song = song / np.max(song) * 255
    song = np.array(song, dtype=np.uint8)
    return song
