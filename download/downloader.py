import os
import re
from selenium import webdriver
import shutil

from auto_vadilation import is_valid
from download.webdriver_functions import download_by_youtube_url_using_webdriver
from utils.string_functions import find_first_apperence_by_regex
import config

DOWNLOAD_DIRECTORY = config.data_dir
WEB_DRIVER_PATH = config.web_driver_path


def download_by_song_object(song):

    download_dir = os.path.join(DOWNLOAD_DIRECTORY, re.sub(' ', '_', song.singer_hebrew) + '_' + re.sub(' ', '_', song.song_hebrew))
    if os.path.isdir(download_dir):
        return
    else:
        os.makedirs(download_dir, exist_ok=True)

    full_name = ' '.join([song.singer_hebrew, song.song_hebrew])
    youtube_url_for_download = create_youtube_url_for_download(full_name)
    download_by_youtube_url_using_webdriver(download_dir, youtube_url_for_download)

    full_name = ' - '.join([song.singer_hebrew, song.song_hebrew, 'שרים קריוקי'])
    youtube_url_for_download = create_youtube_url_for_download(full_name)
    download_by_youtube_url_using_webdriver(download_dir, youtube_url_for_download)

    if not is_valid(download_dir):
        shutil.rmtree(download_dir)


def create_youtube_url_for_download(search_expression):

    prefix_of_youtube_search_url = "https://www.youtube.com/results?search_query="

    search_expression = re.sub(" +", "+", search_expression)
    full_youtube_search_url = prefix_of_youtube_search_url + search_expression

    video_name = find_first_video_name(full_youtube_search_url)

    basic_video_url = 'https://www.youtube.com/watch?v='
    full_video_url = basic_video_url + video_name

    return full_video_url


def find_first_video_name(youtube_search_url):

    regex = '"https:\/\/i.ytimg.com\/vi\/([^\/]+)\/hqdefault.jpg'

    driver = webdriver.Chrome(WEB_DRIVER_PATH)
    driver.get(youtube_search_url)
    source = driver.page_source
    driver.quit()

    first_search_result = find_first_apperence_by_regex(source, regex)

    return first_search_result
