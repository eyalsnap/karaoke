import time
from selenium import webdriver
import re
from download.downloader import download_by_song_object
from download.song import Song
import numpy as np
import config

NUM_OF_SAMPLE = 10000


def get_all_youtubes_names():

    url = r'https://www.youtube.com/user/sharimkaraokeltd/videos'

    driver = webdriver.Chrome(config.web_driver_path)
    driver.get(url)

    names = get_names(driver)

    driver.quit()

    # np.save('songs_name.npy', np.array(names))

    songs = get_songs_from_strings(names)

    return songs


def get_songs_from_strings(names):
    songs = []
    for name in names:
        try:
            parts = name.split('-')
            hebrew_song = parts[0]
            hebrew_singer = parts[1]
            english_song = to_english(hebrew_song)
            english_singer = to_english(hebrew_singer)
            songs.append(Song(hebrew_singer, hebrew_song, english_singer, english_song))
        except:
            print(f'failed in {name}')
    return songs


def get_names(driver):
    html = driver.page_source
    pattern = 'views" title="(.*?שרים קריוקי)" href="/watch?'
    names = re.findall(pattern, html)
    old_names = -1
    while not old_names == len(names) and len(names) < NUM_OF_SAMPLE:
        old_names = len(names)
        driver.execute_script("window.scrollTo(0, 100000);")
        time.sleep(1.5)
        html = driver.page_source
        pattern = 'views" title="(.*?שרים קריוקי)" href="/watch?'
        names = re.findall(pattern, html)
    return names[:NUM_OF_SAMPLE]


def to_english(hebrew_singer):
    hebrew_singer = re.sub('א', 'a', hebrew_singer)
    hebrew_singer = re.sub('ב', 'b', hebrew_singer)
    hebrew_singer = re.sub('ג', 'g', hebrew_singer)
    hebrew_singer = re.sub('ד', 'd', hebrew_singer)
    hebrew_singer = re.sub('ה', 'e', hebrew_singer)
    hebrew_singer = re.sub('ו', 'o', hebrew_singer)
    hebrew_singer = re.sub('ז', 'z', hebrew_singer)
    hebrew_singer = re.sub('ח', 'h', hebrew_singer)
    hebrew_singer = re.sub('ט', 't', hebrew_singer)
    hebrew_singer = re.sub('י', 'i', hebrew_singer)
    hebrew_singer = re.sub('כ', 'k', hebrew_singer)
    hebrew_singer = re.sub('ל', 'l', hebrew_singer)
    hebrew_singer = re.sub('מ', 'm', hebrew_singer)
    hebrew_singer = re.sub('נ', 'n', hebrew_singer)
    hebrew_singer = re.sub('ס', 's', hebrew_singer)
    hebrew_singer = re.sub('ע', 'a', hebrew_singer)
    hebrew_singer = re.sub('פ', 'p', hebrew_singer)
    hebrew_singer = re.sub('צ', 'ts', hebrew_singer)
    hebrew_singer = re.sub('ק', 'k', hebrew_singer)
    hebrew_singer = re.sub('ר', 'r', hebrew_singer)
    hebrew_singer = re.sub('ש', 'sh', hebrew_singer)
    hebrew_singer = re.sub('ת', 't', hebrew_singer)
    hebrew_singer = re.sub('ך', 'h', hebrew_singer)
    hebrew_singer = re.sub('ף', 'f', hebrew_singer)
    hebrew_singer = re.sub('צ', 'ch', hebrew_singer)
    hebrew_singer = re.sub('ם', 'm', hebrew_singer)
    hebrew_singer = re.sub('ן', 'n', hebrew_singer)
    return hebrew_singer


def main():

    # songs = get_all_youtubes_names()
    names = np.load('songs_name.npy')
    songs = get_songs_from_strings(names)
    songs = songs[:NUM_OF_SAMPLE]
    for s in songs:
        print(f'hebrew_singer : {s.singer_hebrew} - hebrew_song : {s.song_hebrew} - english_singer : {s.singer_english} - english_song : {s.song_english}')
        try:
            download_by_song_object(s)
        except Exception as e:
            if hasattr(e, 'message'):
                print(e.message)
            else:
                print(e)


from multiprocessing import Process
if __name__ == '__main__':
    main()
