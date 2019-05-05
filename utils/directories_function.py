import os
from constants.parameters import filenames_parameters


def find_song_and_karaoke_name(directory):
    songs_files = os.listdir(directory)
    first_is_karaoke = 'קריוקי' in songs_files[0]
    second_is_karaoke = 'קריוקי' in songs_files[1]
    if first_is_karaoke and not second_is_karaoke:
        karaoke_name = songs_files[0]
        song_name = songs_files[1]
    elif not first_is_karaoke and second_is_karaoke:
        karaoke_name = songs_files[1]
        song_name = songs_files[0]
    else:
        raise Exception
    return karaoke_name, song_name


def rename_songs(directory):
    origin_karaoke_name, origin_song_name = find_song_and_karaoke_name(directory)
    karaoke_path_src = os.path.join(directory, origin_karaoke_name)
    karaoke_path_dst = os.path.join(directory, filenames_parameters.karaoke_name)

    song_path_src = os.path.join(directory, origin_song_name)
    song_path_dst = os.path.join(directory, filenames_parameters.song_name)

    os.rename(karaoke_path_src, karaoke_path_dst)
    os.rename(song_path_src, song_path_dst)
