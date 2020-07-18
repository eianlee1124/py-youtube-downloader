"""Simple and fast code to download all videos from YouTube channel using
`pytube` and `selenium`.

Author: Joon Seok Lee <eianlee1124@gmail.com>
"""


import os
import sys
import time

from pytube import YouTube
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys



CHANNEL_URL = "< youtube channel's videos section url here >"
CHROME_DRIVER_PATH = "< chromedriver path here >"
END_OF_SCROLL_POS = 0
SCROLL_DOWN_DELAY = 0.8


# create webdriver instance and loads web page.
driver = webdriver.Chrome(CHROME_DRIVER_PATH)
driver.get(CHANNEL_URL)

# find html body for scroll down and check bottom of the page.
body = driver.find_element(By.TAG_NAME, "body")
offset_count = 0

while True:
    prev_pos = driver.execute_script('return window.pageYOffset;')
    try:
        body.send_keys(Keys.END)
        time.sleep(SCROLL_DOWN_DELAY)
        curr_pos = driver.execute_script("return window.pageYOffset;")

        print()
        print(f"\t\tPrev POS: {prev_pos}")
        print(f"\t\tCurr POS: {curr_pos}")
        print()

        if prev_pos == curr_pos:
            offset_count += 1
        if offset_count > 3:
            END_OF_SCROLL_POS = curr_pos
            break

    except KeyboardInterrupt:
        break


contents = []
for elem in driver.find_elements(By.XPATH, '//*[@id="video-title"]'):
    # get link and title from current element.
    link, title = tuple(map(elem.get_attribute, ['href', 'title']))

    # NOTE: your conditions here
    # if "some text" in title:
    #     if any(map(title.startswith, ['some condition1', 'some condition2'])):
    contents.append((link, title))


# print out contents
for link, title in contents:
    print(f"\t\t{title} - {link}")


# download all contents
for link, title in contents:
    try:
        yt = YouTube(link)

        # download highest resolution
        # pytube details: "https://github.com/nficano/pytube"
        yt.streams\
            .filter(progressive=True, file_extension='mp4')\
            .order_by('resolution')\
            .desc()\
            .first()\
            .download()
    except Exception as e:
        print("\n" * 5)
        print("=" * 50)
        print("\t\t\t", e)
        print("=" * 50)
        print("\n" * 5)
        break
else:
    driver.quit()
    sys.exit()
