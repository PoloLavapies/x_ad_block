from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import re
import sys
import time

# twitterのユーザー情報
USER_ID = sys.argv[1]
PASSWORD = sys.argv[2]

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

    password_form = driver.find_element(By.XPATH,'//input[@autocomplete="current-password"]')
    password_form.send_keys(PASSWORD)
    password_form.send_keys(Keys.ENTER)
    time.sleep(TIME_TO_SLEEP)

def mute():
    try:
        articles = driver.find_elements(By.TAG_NAME, "article")
        for article in articles:
            spans = article.find_elements(By.TAG_NAME, "span")
            for span in spans:
                if "プロモーション" in span.text:
                    button = article.find_element(By.XPATH, ".//button[@aria-label='もっと見る']")
                    button.click()
            
                    react_root = driver.find_element(By.ID, "react-root")
                    spans2 = react_root.find_elements(By.TAG_NAME, "span")
        
                    pattern = re.compile(r"@.+さんをミュート")
                    for span in spans2:
                        match = pattern.match(span.text)
                        if match:
                            span.click()
                            matched_text = match.group()
                            print(matched_text + "しました") 
            # TODO 別メソッドに切り出す
            # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # time.sleep(TIME_TO_SLEEP_LONG)
    except:
        pass

driver = webdriver.Chrome()
driver.set_window_size(390, 844)
login()
time.sleep(TIME_TO_SLEEP_LONG)
while True:
    mute()
    driver.get(URL_TIMELINE)
    time.sleep(TIME_TO_SLEEP)
