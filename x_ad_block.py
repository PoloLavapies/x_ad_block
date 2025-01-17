from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import os
import re
import time
import traceback

# twitterのユーザー情報
USER_ID = os.environ.get("ACCOUNT")
PASSWORD = os.environ.get("PASSWORD")
PHONE_NUMBER = os.environ.get("PHONE")
TIME_TO_SLEEP = 3
TIME_TO_SLEEP_LONG = 6

URL_LOGIN = "https://twitter.com/login"
URL_TIMELINE = "https://x.com"

def login():
    driver.get(URL_LOGIN)
    time.sleep(TIME_TO_SLEEP_LONG)

    user_id_form = driver.find_element(By.XPATH,'//input[@autocomplete="username"]')
    user_id_form.send_keys(USER_ID)
    user_id_form.send_keys(Keys.ENTER)
    time.sleep(TIME_TO_SLEEP)

    screenshot_path = "./screenshot1.png"
    driver.save_screenshot(screenshot_path)

    try:
        phone_number_form = driver.find_element(By.XPATH, '//input[@name="text"]')
        phone_number_form.send_keys(PHONE_NUMBER)
        phone_number_form.send_keys(Keys.ENTER)
        time.sleep(TIME_TO_SLEEP)
    except:
        pass

    screenshot_path = "./screenshot2.png"
    driver.save_screenshot(screenshot_path)

    password_form = driver.find_element(By.XPATH,'//input[@autocomplete="current-password"]')
    password_form.send_keys(PASSWORD)
    password_form.send_keys(Keys.ENTER)
    time.sleep(TIME_TO_SLEEP)

    screenshot_path = "./screenshot3.png"
    driver.save_screenshot(screenshot_path)

    try:
        phone_number_form = driver.find_element(By.XPATH, '//input[@name="text"]')
        phone_number_form.send_keys(PHONE_NUMBER)
        phone_number_form.send_keys(Keys.ENTER)
        time.sleep(TIME_TO_SLEEP)
    except:
        pass

    screenshot_path = "./screenshot4.png"
    driver.save_screenshot(screenshot_path)

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
        article = driver.find_element(By.XPATH, "//article[descendant::span[contains(text(), 'プロモーション')]]")
        button = article.find_element(By.XPATH, ".//button[@aria-label='もっと見る']")
        button.click()

        spans = driver.find_elements(By.TAG_NAME, "span")
        pattern = re.compile(r"@.+さんをミュート")
        for span in spans:
            match = pattern.match(span.text)
            if match:
                sibiling_span = span.find_element(By.XPATH, "../../../..").find_elements(By.XPATH, "./*")[0].find_elements(By.TAG_NAME, "span")[0]
                if sibiling_span.text == 'この広告が表示されている理由':
                    span.click()
                    print(match.group() + "しました")
                    delete_modal()
                else:
                    print(match.group() + "しませんでした")
        
    except Exception as e:
        # print(e)
        # traceback.print_exc()
        pass

    # スクロールして再帰呼び出し
    height = driver.execute_script("return document.body.scrollHeight")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(TIME_TO_SLEEP)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if height != new_height:
        mute()

options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("start-maximized")
options.add_argument("window-size=1920,1080")
options.add_argument("--disable-extensions")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
driver = webdriver.Chrome(options=options)

login()
time.sleep(TIME_TO_SLEEP_LONG)

start_time = datetime.now()
print("ミュート処理を開始していきます")
screenshot_path = "./screenshot5.png"
driver.save_screenshot(screenshot_path)
while True:
    current_time = datetime.now()
    elapsed_time = (current_time - start_time).total_seconds()
    if elapsed_time >= 300:
        print("5分経過したので処理を終了します。")
        break
    mute()
    driver.get(URL_TIMELINE)
    time.sleep(TIME_TO_SLEEP_LONG)
