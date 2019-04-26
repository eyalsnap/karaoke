import os

sox_path = r'C:\Program Files (x86)\sox-14-4-2'


def _mp3_to_wav(input_path, output_path, delete=False):
    cmd = 'sox.exe ' + input_path + ' ' + output_path
    os.system(cmd)
    if delete:
        os.remove(input_path)


def _make_path_absolute(path):
    if not os.path.isabs(path):
        path = os.path.join(os.curdir, path)
    return path


def convert_songs(path_list):
    path_list = [_make_path_absolute(path) for path in path_list]
    out_path_list = [path.replace('.mp3','.wav') for path in path_list]
    initial_dir = os.curdir
    os.chdir(sox_path)
    for input_path, output_path in zip(path_list, out_path_list):
        _mp3_to_wav(input_path, output_path)
    os.chdir(initial_dir)
    return initial_dir


if __name__ == '__main__':
    # os.chdir(sox_path)
    # path = r"C:\dev\free_time_projects\kareoke\notebooks\samples_data\eyal\full.mp3"
    # out_path = r"C:\dev\free_time_projects\kareoke\notebooks\samples_data\eyal\output.wav"
    # _mp3_to_wav(path, out_path)

    song_list = [r"C:\dev\free_time_projects\kareoke\notebooks\samples_data\eyal\full.mp3",
                 r"C:\dev\free_time_projects\kareoke\notebooks\samples_data\eyal\kareokey.mp3"]
    new_list = convert_songs(song_list)
