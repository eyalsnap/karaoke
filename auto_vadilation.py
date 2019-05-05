import os
from mutagen.mp3 import MP3
import numpy as np
from constants.configs import config
from utils.directories_function import find_song_and_karaoke_name


def main():
    results = []
    directory = config.data_dir
    for file in os.listdir(directory):
        song_directory = os.path.join(directory, file)
        result = is_valid(song_directory)
        results.append(result)

    results = np.array(results)
    print(f'{results.sum()} - are good of {len(results)}')


def check_types(path1, path2):
    return path1.endswith('.mp3') and path2.endswith('.mp3')


def detail_in_name(karaoke_name, song_name):
    parts = karaoke_name.split(' - ')
    singer = parts[1]
    song = parts[0]
    return singer in song_name and song in song_name


def is_valid(song_directory):
    return 'good' == check_song(song_directory)


def check_song(song_directory):
    if not os.path.isdir(song_directory):
        return 'no dir'

    songs_files = os.listdir(song_directory)
    if len(songs_files) < 2:
        return 'song missing'

    try:
        karaoke_name, song_name = find_song_and_karaoke_name(song_directory)
    except:
        return 'karaoke missing'

    karaoke_path = os.path.join(song_directory, karaoke_name)
    song_path = os.path.join(song_directory, song_name)

    if not check_types(karaoke_path, song_path):
        return 'not mp3 file'

    if not detail_in_name(karaoke_name, song_name):
        return 'name is not in the song'

    return 'good'




def get_length(path):
    audio = MP3(path)
    return audio.info.length


if __name__ == '__main__':
     main()
