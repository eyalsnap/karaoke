import os
import re
from selenium import webdriver
from time import sleep
from selenium.common.exceptions import ElementNotVisibleException

from song import Song


DOWNLOAD_DIRECTORY = r"C:\Users\Eyal\Desktop\eyal\python\data\songs"


# creating url of youtube result by given singer and song name
def create_youtube_url_for_download(fullName):
    ### getting into youtube by searching the song and the singer
    # the beginning of the search url
    searchStart = "https://www.youtube.com/results?search_query="

    # deleting spaces
    combinningWords = re.sub(" +", "+", fullName)

    # creating the full search url of the song
    fullSearchPath = searchStart + combinningWords

    ### creating the url of the first result
    # the end of the url of the first result
    endPath = findNewUrl(fullSearchPath)

    # the url beginning of the first result in the search
    basicPath = 'https://www.youtube.com/watch?v='

    # strcat the url of the first result
    fullPath = basicPath + endPath

    return fullPath


# a parsing function that return the first group in a given string by a given regex
def findStrByRegex(string, pattern):
    regex = re.compile(pattern)
    allGroups = regex.search(string)
    return allGroups.group(1)


# by url of youtube return the first result
def findNewUrl(fullPath):
    # the regex that find the url of the first result in youtube in the page source
    regex = '"https:\/\/i.ytimg.com\/vi\/([^\/]+)\/hqdefault.jpg'

    # getting into the web in the given url
    driver = webdriver.Chrome(r'C:\Users\Eyal\Downloads\chromedriver_win32\chromedriver.exe')
    driver.get(fullPath)

    # extracting the the page source of the youtube results page
    source = driver.page_source

    # finding the url of the first result by regex
    newUrl = findStrByRegex(source, regex)

    # closing the chrome
    driver.quit()

    return newUrl


################################################

# running over all the songs and fixed their name - deletinig the start of their name
def fixing_all_the_names():
    directory = r'C:\Users\Eyal\Downloads'
    for filename in os.listdir(directory):
        if filename.endswith(".mp3") and 'fixed' in filename:
            oldFileName = directory + '\\' + filename
            newName = re.sub('  ', ' ', oldFileName)
            newName = re.sub('fixed1 ', '', oldFileName)
            os.rename(oldFileName, newName)


# a function that waits until the download bottom is ready and clicks it
def clickUnVisible(driver):
    TIME_TO_WAIT_EACH_TIME = 2
    link = None
    while not link:
        try:
            # driver.find_element_by_id("file").click()
            driver.find_element_by_id("download").click()
            return
        except ElementNotVisibleException:
            sleep(TIME_TO_WAIT_EACH_TIME)


# a function that search the convert bottom and click it
# after a minute when the bottom wasnt found we do refresh - download this song from the beginning
def waitingForPage(driver, downloadPath):
    clickUnVisible(driver)
    sleep(18)
    driver.quit()
    return


def download_by_singer_names(song):

    full_name = ' - '.join([song.singer_hebrew, song.song_hebrew])
    download_dir = os.path.join(DOWNLOAD_DIRECTORY, re.sub(' ', '_', song.singer_hebrew) + '_' + re.sub(' ', '_', song.song_hebrew))
    if os.path.isdir(download_dir):
        return
    else:
        os.makedirs(download_dir, exist_ok=True)

    youtube_url_for_download = create_youtube_url_for_download(full_name)
    download_by_url(download_dir, youtube_url_for_download)

    full_name = ' - '.join([song.singer_hebrew, song.song_hebrew, 'שרים קריוקי'])

    youtube_url_for_download = create_youtube_url_for_download(full_name)
    download_by_url(download_dir, youtube_url_for_download)


# downloading a video by its path in youtube
def download_by_url(download_dir, download_url):
    # the url of the website that converts videos to mp3 files
    down_load_web_path = 'https://ytmp3.cc/'

    options = webdriver.ChromeOptions()
    options.add_experimental_option("prefs", {
        "download.default_directory": os.path.join(download_dir),
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    })

    # openning the crome
    # driver = webdriver.Chrome(r'C:\Users\Eyal\Downloads\chromedriver_win32\chromedriver.exe')
    driver = webdriver.Chrome(r'C:\Users\Eyal\Downloads\chromedriver_win32\chromedriver.exe', chrome_options=options)

    driver.get(down_load_web_path)

    # finding the box where we write the url to download and writing it
    input_element = driver.find_element_by_id("input")
    input_element.send_keys(download_url)

    # finding the bottom that converts the video to mp3 file and clicking it
    element = driver.find_element_by_id("submit")
    element.click()

    # clicking download bottom
    waitingForPage(driver, download_url)


# the full function that download all the songs per language
def download_by_files_path(hebrew_file_path, english_file_path):

    with open(english_file_path, 'r') as f:
        english_lines = f.readlines()

    with open(hebrew_file_path, 'r', encoding="utf8") as f:
        hebrew_lines = f.readlines()

    # running over all the singers
    for hebrew_singer_line, english_singer_line in zip(hebrew_lines, english_lines):

        hebrew_singer, hebrew_songs = extract_singer_and_song(hebrew_singer_line)
        english_singer, english_songs = extract_singer_and_song(english_singer_line)

        # running over all the songs
        for hebrew_song, english_song in zip(hebrew_songs, english_songs):
            song = Song(hebrew_singer, hebrew_song, english_singer, english_song)
            print(f'now download: {english_singer} - {english_song}')
            download_by_singer_names(song)


def extract_singer_and_song(hebrew_name):
    hebrew_name = re.sub('\n', '', hebrew_name)
    parts = hebrew_name.split(':')
    hebrewSinger = parts[0]
    hebrewSongs = parts[1].split(',')
    return hebrewSinger, hebrewSongs


if __name__ == '__main__':

    currentFolder = os.getcwd()

    hebrew_names_path = os.path.join(currentFolder, "hebrew_names.txt")
    english_names_path = os.path.join(currentFolder, "english_names.txt")

    download_by_files_path(hebrew_names_path, english_names_path)

    # fixing all the song names
    fixing_all_the_names()
