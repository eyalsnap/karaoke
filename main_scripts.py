# technique functions

import os
import re
from selenium import webdriver
from time import sleep
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotVisibleException
import webbrowser


def getEnglishLinesByFileName(fileName):
    file = open(fileName)
    data = file.readlines()
    file.close()
    return data


def getHebrewLinesByFileName(fileName):
    file = open(fileName, encoding="utf8")
    data = file.readlines()
    file.close()
    return data


def changeFolder():
    currentFolder = os.getcwd()
    newFolderName = currentFolder + "\\snappir list"
    downloadFolderName = findDownloadFolder()
    if not os.path.exists(newFolderName):
        os.makedirs(newFolderName)

    for filename in os.listdir(downloadFolderName):
        if filename.endswith(".mp3"):
            oldName = downloadFolderName + '\\' + filename
            newName = newFolderName + '\\' + filename
            os.rename(oldName, newName)


# creating url of youtube result by given singer and song name
def createSearchName(singerName, songName):
    ### getting into youtube by searching the song and the singer
    # the beginning of the search url
    searchStart = "https://www.youtube.com/results?search_query="

    # strcat the name of the singer and name of the song
    fullName = singerName + songName

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
    driver = webdriver.Chrome()
    driver.get(fullPath)

    # extracting the the page source of the youtube results page
    source = driver.page_source

    # finding the url of the first result by regex
    newUrl = findStrByRegex(source, regex)

    # closing the chrome
    driver.quit()

    return newUrl


################################################

# running over the folder

# a function that waits while there is a file that is in downloading procces
def checkIfStillDownload():
    directory = findDownloadFolder()
    still = 1
    while (still == 1):
        still = 0
        # checking if there is a file that its download wasnt finished
        for fileName in os.listdir(directory):
            if fileName.endswith(".crdownload"):
                still = 1


# a function that changes the name of the last song that was downloaded
def changeNames(singer, song):
    directory = findDownloadFolder()
    index = 1
    for filename in os.listdir(directory):
        if filename.endswith(".mp3") and not 'fixed' in filename:
            oldFileName = directory + '\\' + filename
            newName = directory + '\\fixed' + str(index) + ' ' + singer + ' ' + song + '.mp3'
            os.rename(oldFileName, newName)
            index = index + 1


# running over all the songs and fixed their name - deletinig the start of their name
def fixingAllTheNames():
    directory = findDownloadFolder()
    for filename in os.listdir(directory):
        if filename.endswith(".mp3") and 'fixed' in filename:
            oldFileName = directory + '\\' + filename
            newName = re.sub('  ', ' ', oldFileName)
            newName = re.sub('fixed1 ', '', oldFileName)
            os.rename(oldFileName, newName)


# finding the downloads folder
def findDownloadFolder():
    directory = "C:\\Users"
    for filename in os.listdir(directory):
        if filename.startswith('Default') or filename.startswith('public') or filename.startswith(
                'Public') or filename.startswith('all') or filename.startswith('desktop') or filename.startswith('All'):
            continue
        fullFileName = directory + '\\' + filename
        if os.path.isdir(fullFileName):
            for subFile in dirList:
                fullSubFile = fullFileName + '\\Downloads'
                if ('Downloads' == subFile and os.path.isdir(fullSubFile)):
                    return fullSubFile


######################################

# wating for bottom and clicking them

# a function that waits until the download bottom is ready and clicks it
def clickUnVisible(driver):
    TIME_TO_WAIT_EACH_TIME = 2
    link = None
    while not link:
        try:
            driver.find_element_by_id("file").click()
            return
        except ElementNotVisibleException:
            sleep(TIME_TO_WAIT_EACH_TIME)


# a function that search the convert bottom and click it
# after a minute when the bottom wasnt found we do refresh - download this song from the beginning
def waitingForPage(driver, downloadPath):
    TIME_TO_WAIT_EACH_TIME = 2
    TOTAL_TIME_TO_WAIT = 60

    totalTime = 0
    link = None
    while not link:
        try:
            clickUnVisible(driver)
            sleep(16)
            checkIfStillDownload()
            driver.quit()
            return
        except NoSuchElementException:
            # in case that the convert bottom wasnt found
            sleep(TIME_TO_WAIT_EACH_TIME)
            totalTime = totalTime + TIME_TO_WAIT_EACH_TIME

            # in case we wait over a minute
            if (totalTime > TOTAL_TIME_TO_WAIT):
                driver.quit()
                downLoadByPath(downloadPath)
                return


#########################################

# flow function

def downLoadBySingerAndSong(singer, song, singerName, songName):
    downLoadPath = createSearchName(singer, song)
    downLoadByPath(downLoadPath)

    changeNames(singerName, songName)


# downloading a video by its path in youtube
def downLoadByPath(downloadPath):
    # the url of the website that converts videos to mp3 files
    downLoadWebPath = 'https://ytmp3.cc/'

    # openning the crome
    driver = webdriver.Chrome()
    driver.get(downLoadWebPath)

    # finding the box where we write the url to download and writing it
    inputElement = driver.find_element_by_id("input")
    inputElement.send_keys(downloadPath)

    # finding the bottom that converts the video to mp3 file and clicking it
    element = driver.find_element_by_id("submit")
    element.click()

    # clicking download bottom
    waitingForPage(driver, downloadPath)


##########################################

# main flow

# the full function that download all the songs per language
def downloadForLang(hebrewFilename, englishFilename, isHebrew):
    ### reading the names of the singers and songs
    englishData = getEnglishLinesByFileName(englishFilename)

    if isHebrew:
        hewbrewData = getHebrewLinesByFileName(hebrewFilename)
        englishData[0] = englishData[0][3:]
    else:
        hewbrewData = getEnglishLinesByFileName(hebrewFilename)

    # running over all the singers
    for singerIndex in range(len(hewbrewData)):

        ### parsing
        # hebrew
        hebrewLine = re.sub('\n', '', hewbrewData[singerIndex])
        parts = hebrewLine.split(':')
        # the singer name
        hebrewSinger = parts[0]
        # the songs
        hebrewSongs = parts[1].split(',')

        # english
        englishLine = re.sub('\n', '', englishData[singerIndex])
        parts = englishLine.split(':')
        # the singer name
        englishSinger = parts[0]
        # the songs
        englishSongs = parts[1].split(',')

        # running over all the songs
        for songIndex in range(len(hebrewSongs)):
            hebrewSong = hebrewSongs[songIndex]
            englishSong = englishSongs[songIndex]
            print('now download: ' + englishSinger + '- ' + englishSong)
            downLoadBySingerAndSong(hebrewSinger, hebrewSong, englishSinger, englishSong)


#############################################

currentFolder = os.getcwd()

# files name
# fileNameEnglishSong = currentFolder + "\\" + "english song.txt"
hebrewFilename = currentFolder + "\\" + "hebrew songs.txt"
englishNamesFilename = currentFolder + "\\" + "hebrew names.txt"

# download songs in english
# downloadForLang(fileNameEnglishSong, fileNameEnglishSong, 0)
# download songs in hebrew
downloadForLang(hebrewFilename, englishNamesFilename, 1)

# fixing all the song names
fixingAllTheNames()

# inserting into new folder
changeFolder()
