from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import re
import sys
import time
import traceback

# twitterのユーザー情報
USER_ID = sys.argv[1]
PASSWORD = sys.argv[2]
PHONE_NUMBER = sys.argv[3]

URL_LOGIN = "https://twitter.com/login"
URL_TIMELINE = "https://x.com"

TIME_TO_SLEEP = 3
TIME_TO_SLEEP_LONG = 6

def login():
    driver.get(URL_LOGIN)
    time.sleep(TIME_TO_SLEEP_LONG)

    user_id_form = driver.find_element(By.XPATH,'//input[@autocomplete="username"]')
    user_id_form.send_keys(USER_ID)
    user_id_form.send_keys(Keys.ENTER)
    time.sleep(TIME_TO_SLEEP)

    try:
        phone_number_form = driver.find_element(By.XPATH, '//input[@name="text"]')
        phone_number_form.send_keys(PHONE_NUMBER)
        phone_number_form.send_keys(Keys.ENTER)
        time.sleep(TIME_TO_SLEEP_LONG)
    except:
        pass

    password_form = driver.find_element(By.XPATH,'//input[@autocomplete="current-password"]')
    password_form.send_keys(PASSWORD)
    password_form.send_keys(Keys.ENTER)
    time.sleep(TIME_TO_SLEEP)

def scroll():
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(TIME_TO_SLEEP)
    return driver.execute_script("return document.body.scrollHeight")

def delete_modal():
    try:
        time.sleep(TIME_TO_SLEEP)
        button = driver.find_element(By.XPATH, "//button[descendant::span[contains(text(), '後で試す')]]")
        button.click()
    except Exception as e:
        pass

def mute():
    try:
        # TODO ツイート内容に「プロモーション」が含まれる場合の対策をする
        article = driver.find_element(By.XPATH, "//article[descendant::span[contains(text(), 'プロモーション')]]")
        button = article.find_element(By.XPATH, ".//button[@aria-label='もっと見る']")
        button.click()

        spans = driver.find_elements(By.TAG_NAME, "span")
        pattern = re.compile(r"@.+さんをミュート")
        for span in spans:
            match = pattern.match(span.text)
            if match:
                span.click()
                print(match.group() + "しました")
                delete_modal()
        
    except Exception as e:
        pass

    # スクロールして再帰呼び出し
    height = driver.execute_script("return document.body.scrollHeight")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(TIME_TO_SLEEP)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if height != new_height:
        mute()

driver = webdriver.Chrome()
driver.set_window_size(1920, 1080)
login()
time.sleep(TIME_TO_SLEEP_LONG)
while True:
    mute()
    driver.get(URL_TIMELINE)
    time.sleep(TIME_TO_SLEEP)
