import os


def find_song_and_karaoke_name(directory):
    songs_files = os.listdir(directory)
    if 'קריוקי' in songs_files[0]:
        karaoke_name = songs_files[0]
        song_name = songs_files[1]
    elif 'קריוקי' in songs_files[1]:
        karaoke_name = songs_files[1]
        song_name = songs_files[0]
    else:
        raise Exception
    return karaoke_name, song_name
