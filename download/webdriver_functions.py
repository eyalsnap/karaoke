from selenium import webdriver
from time import sleep
from selenium.common.exceptions import ElementNotVisibleException
from constants.configs import config

WEB_DRIVER_PATH = config.web_driver_path


def download_by_youtube_url_using_webdriver(download_dir, download_url):

    driver = create_download_web_driver(download_dir)
    insert_youtube_url_to_web_driver(download_url, driver)
    click_download_bottom(driver)


def insert_youtube_url_to_web_driver(download_url, driver):
    input_element = driver.find_element_by_id("input")
    input_element.send_keys(download_url)
    element = driver.find_element_by_id("submit")
    element.click()


def create_download_web_driver(download_dir):
    download_web_path = 'https://ytmp3.cc/'
    options = webdriver.ChromeOptions()
    options.add_experimental_option("prefs", {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    })
    driver = webdriver.Chrome(WEB_DRIVER_PATH, chrome_options=options)
    driver.get(download_web_path)
    return driver


def click_download_bottom(driver):

    time_to_wait_for_download_bottom = 2
    time_to_wait_after_clicking_download = 18

    while True:
        try:
            driver.find_element_by_id("download").click()
            sleep(time_to_wait_after_clicking_download)
            driver.quit()
            return
        except ElementNotVisibleException:
            sleep(time_to_wait_for_download_bottom)
