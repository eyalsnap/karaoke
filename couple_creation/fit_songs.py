import matplotlib.pyplot as plt

from couple_creation.song_correlation import wave_correlation
from couple_creation.song_file import SongFile
from scipy.io import wavfile


fps = 2.26e-5
seconds = 10

if __name__ == '__main__':

    song_path = r'C:\Users\Eyal\Desktop\eyal\python\temp\אייל_גולן_קחי_לך_את_היום\אייל גולן - קחי לך את היום.wav'
    karaoke_path = r'C:\Users\Eyal\Desktop\eyal\python\temp\אייל_גולן_קחי_לך_את_היום\קחי לך את היום - אייל גולן - שרים קריוקי.wav'
    new_path = r'C:\Users\Eyal\Desktop\eyal\python\temp\אייל_גולן_קחי_לך_את_היום\mix.wav'

    song = SongFile(song_path)
    karaoke = SongFile(karaoke_path)

    translation = wave_correlation(song, karaoke)
    new_fs, new_song_data = karaoke.cut_song_by_start_bits(-translation)

    transfer_fs, transfer_song = song.song_transfer(karaoke, 20)

    wavfile.write(new_path, transfer_fs, transfer_song)
    # wavfile.write(new_path, new_fs, new_song_data)
