from couple_creation.song_couple import SongCouple


if __name__ == '__main__':
    song_dir = r'C:\Users\EYAL\Desktop\eyal\nabaz\songs\ex1\eden_ben_zaken_half_country\2_wav_files'
    song_couple = SongCouple(song_dir)
    song_couple.align_audio()
    song_couple.save_aligned_audio()
