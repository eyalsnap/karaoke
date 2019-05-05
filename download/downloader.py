import os
import re
from selenium import webdriver
import shutil

from auto_vadilation import is_valid
from download.webdriver_functions import download_by_youtube_url_using_webdriver
from constants.parameters.filenames_parameters import karaoke_page_signature
from constants.parameters.url_parameters import youtube_search_prefix, youtube_watch_prefix, youtube_videos_regex
from utils.directories_function import rename_songs
from utils.string_functions import find_first_apperence_by_regex
from constants.configs import config

DOWNLOAD_DIRECTORY = config.data_dir
WEB_DRIVER_PATH = config.web_driver_path


def download_by_song_object(downloaded_songs, song):

    download_dir = song.get_download_dir(DOWNLOAD_DIRECTORY)
    if os.path.isdir(download_dir):
        return
    else:
        os.makedirs(download_dir, exist_ok=True)

    full_name = ' '.join([song.singer_hebrew, song.song_hebrew])
    song_youtube_url_for_download = create_youtube_url_for_download(full_name)
    download_by_youtube_url_using_webdriver(download_dir, song_youtube_url_for_download)

    full_name = ' - '.join([song.singer_hebrew, song.song_hebrew, karaoke_page_signature])
    karaoke_youtube_url_for_download = create_youtube_url_for_download(full_name)
    download_by_youtube_url_using_webdriver(download_dir, karaoke_youtube_url_for_download)

    if not is_valid(download_dir):
        shutil.rmtree(download_dir)
    else:
        rename_songs(download_dir)
        song.set_download_urls(song_youtube_url_for_download, karaoke_youtube_url_for_download)
        downloaded_songs.append(song)


def create_youtube_url_for_download(search_expression):

    search_expression = re.sub(" +", "+", search_expression)
    full_youtube_search_url = youtube_search_prefix + search_expression

    video_name = find_first_video_name(full_youtube_search_url)

    full_video_url = youtube_watch_prefix + video_name

    return full_video_url


def find_first_video_name(youtube_search_url):

    driver = webdriver.Chrome(WEB_DRIVER_PATH)
    driver.get(youtube_search_url)
    source = driver.page_source
    driver.quit()

    first_search_result = find_first_apperence_by_regex(source, youtube_videos_regex)

    return first_search_result
