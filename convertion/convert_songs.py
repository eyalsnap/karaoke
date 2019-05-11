import os
import pandas as pd
from constants.configs import config
import subprocess

sox_path = config.sox_path
main_dir = config.data_dir
meta_data_file = config.meta_data_file


def _mp3_to_wav(input_path, output_path, is_delete=True):
    cmd = 'sox.exe ' + input_path + ' ' + output_path
    os.system(cmd)
    if (is_delete):
        os.remove(input_path)


def get_meta_data(full_path, parameter):
    return subprocess.run('sox.exe --i -' + parameter + ' ' + full_path, stdout=subprocess.PIPE,
                          universal_newlines=True).stdout


def enrich_with_metadata(row):
    row['channles'] = int(get_meta_data(row['full_path'], 'c'))
    row['sample_rate'] = int(get_meta_data(row['full_path'], 'r'))
    row['duration'] = get_meta_data(row['full_path'], 'd').strip()
    return row


def convert_row(row):
    # because pandas runs over the first row twice in apply:
    if not os.path.exists(row['full_path']):
        return row
    if row['full_path'].endswith('.mp3'):
        full_mp3 = row['full_path'].replace('.mp3', '.wav')
        _mp3_to_wav(row['full_path'], full_mp3)
        row['relative_url'] = row['relative_url'].replace('.mp3', '.wav')
    print(row['full_path'])
    return row


def main():
    initial_dir = os.curdir
    df = pd.read_csv(meta_data_file)
    os.chdir(sox_path)
    df['full_path'] = df['relative_url'].apply(lambda x: os.path.join(main_dir, x))
    df = df.apply(enrich_with_metadata, axis=1)
    df = df.apply(convert_row, axis=1)
    df = df.reset_index(drop=True)
    df = df.drop('full_path', axis=1)
    df.to_csv(config.meta_data_file, encoding='utf-8', index=False)
    os.chdir(initial_dir)


if __name__ == '__main__':
    # # os.chdir(sox_path)
    # # path = r"C:\dev\free_time_projects\kareoke\notebooks\samples_data\eyal\full.mp3"
    # # out_path = r"C:\dev\free_time_projects\kareoke\notebooks\samples_data\eyal\output.wav"
    # # _mp3_to_wav(path, out_path)
    #
    # song_list = [r"C:\dev\free_time_projects\kareoke\notebooks\samples_data\eyal\full.mp3",
    #              r"C:\dev\free_time_projects\kareoke\notebooks\samples_data\eyal\kareokey.mp3"]
    # new_list = convert_songs(song_list)
    main()
