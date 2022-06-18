import streamlit as st
import pandas as pd
import os, sys
import pathlib
from selenium import webdriver
import platform
import warnings
from selenium.webdriver.firefox.options import Options
import time
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def getdriver():
    options = Options()

    #s = Service(ChromeDriverManager().install())
    driver = webdriver.Remote(
      command_executor='https://anirudhjm_01m5Ny:3z5Hx6obs9hesLmAeA3Z@hub-cloud.browserstack.com/wd/hub')
                  


desired_cap = {
    'os_version': 'Catalina',
    'os': 'OS X',
    'browser': 'chrome',
    'browser_version': 'latest',
    'name': 'Parallel Test1',  # test name
    'build': 'browserstack-build-1'  # Your tests will be organized within this build
}


def scroll_to_bottom(driver):
    old_position = 0
    new_position = None

    while new_position != old_position:
        # Get old scroll position
        old_position = driver.execute_script(
            ("return (window.pageYOffset !== undefined) ?"
             " window.pageYOffset : (document.documentElement ||"
             " document.body.parentNode || document.body);"))
        # Sleep and Scroll
        time.sleep(2)
        driver.execute_script((
            "var scrollingElement = (document.scrollingElement ||"
            " document.body);scrollingElement.scrollTop ="
            " scrollingElement.scrollHeight;"))
        # Get new position
        time.sleep(2)
        new_position = driver.execute_script(
            ("return (window.pageYOffset !== undefined) ?"
             " window.pageYOffset : (document.documentElement ||"
             " document.body.parentNode || document.body);"))
        time.sleep(2)


st.title('facebook ad scraper')

link = st.text_input('Enter page link after searching for the ad and applying any filters')

if st.button('Scrape Data') and link is not None:
    browser = getdriver()

    browser.get(link)
    time.sleep(4)
    if browser.title == 'Ad Library':
        time.sleep(2)
    else:
        st.write('Page not loading try again in sometime')
        browser.quit()
        quit()

    scroll_to_bottom(browser)

    primarytext = []
    header2 = []
    header3 = []
    creativelinks = []
    CTA = []

    search = browser.find_elements(
        By.XPATH, '//div[@class="_7jyg _7jyh"]'
    )

    print(len(search))

    for i in search:
        # time.sleep(2)
        try:

            primary_text = i.find_element(By.XPATH, './/div[@class="_7jyr _a25-" or @class = "_7jyr"]')
            print(primary_text.text)
            primarytext.append(primary_text.text)

        except NoSuchElementException:
            primarytext.append(None)
            # continue
        try:

            header_2 = i.find_element(By.XPATH, './/div[@class="_8jh2"]')
            header2.append(header_2.text)
            print(header_2.text)
        except NoSuchElementException:
            print('no header 2')
            header2.append(None)
            # continue
        try:

            header_3 = i.find_element(By.XPATH, './/div[@class="_8jh3"]')
            header3.append(header_3.text)
            print(header_3.text)
        except NoSuchElementException:
            print('no header 3')
            header3.append(None)
            # continue
        try:
            image = i.find_element(By.XPATH, './/img[@class="_7jys img"]')
            creativelinks.append(image.get_attribute("src"))
        except NoSuchElementException:
            creativelinks.append(None)
            # continue
        try:

            callta = i.find_element(By.XPATH, './/div[@class="_8jh0"]')
            CTA.append(callta.text)
            print(callta.text)
        except NoSuchElementException:
            print('no cta')
            CTA.append(None)
            # continue

    df = pd.DataFrame()
    df['primarytext'] = primarytext
    df['header2'] = header2
    df['header3'] = header3
    df['img links'] = creativelinks
    df['cta'] = CTA

    df.to_csv('scraped_data.csv', index=False)

    browser.quit()

    with open('scraped_data.csv') as f:
        st.download_button('Download CSV', f)  # Defaults to 'text/plain'

#
