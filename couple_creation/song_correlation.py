import numpy as np
from time import time


SKIP = 10


def wave_correlation(song1, song2):

    st = time()

    _, short1 = song1.cut_song_by_time(0, 20)
    _, short2 = song2.cut_song_by_time(0, 20)

    short1 = short1[::SKIP, :]
    short2 = short2[::SKIP, :]

    conv1 = np.convolve(short1[:, 0], short2[::-1, 0])
    conv2 = np.convolve(short1[:, 1], short2[::-1, 1])
    conv = conv1 + conv2

    max_index = (np.argmax(conv) - short1.shape[0] + 1) * SKIP

    et = time()

    print(et - st)

    return max_index
