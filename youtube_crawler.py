import time
from selenium import webdriver
import re

from main_scripts import download_by_singer_names
from song import Song


def get_all_youtubes_names():

    url = r'https://www.youtube.com/user/sharimkaraokeltd/videos'

    driver = webdriver.Chrome(r'C:\Users\Eyal\Downloads\chromedriver_win32\chromedriver.exe')
    driver.get(url)

    names = get_names(driver)

    driver.quit()

    songs = []
    for name in names:
        parts = name.split(' - ')
        hebrew_song = parts[0]
        hebrew_singer = parts[1]
        english_song = to_english(hebrew_song)
        english_singer = to_english(hebrew_singer)
        songs.append(Song(hebrew_singer, hebrew_song, english_singer, english_song))

    return songs


def get_names(driver):
    html = driver.page_source
    pattern = 'views" title="(.*?שרים קריוקי)" href="/watch?'
    names = re.findall(pattern, html)
    old_names = -1
    while not old_names == len(names) and False:
        old_names = len(names)
        driver.execute_script("window.scrollTo(0, 100000);")
        time.sleep(1.5)
        html = driver.page_source
        pattern = 'views" title="(.*?שרים קריוקי)" href="/watch?'
        names = re.findall(pattern, html)
    return names[:2]


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


if __name__ == '__main__':
    songs = get_all_youtubes_names()
    for s in songs:
        print(f'hebrew_singer : {s.singer_hebrew} - hebrew_song : {s.song_hebrew} - english_singer : {s.singer_english} - english_song : {s.song_english}')
        download_by_singer_names(s)
