import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd

from selenium.webdriver.common.keys import Keys

exe_path = '/Users/pixis/Downloads/chromedriver'
driver = webdriver.Chrome(exe_path)
driver.get(
    'https://www.facebook.com/ads/library/?active_status=all&ad_type=all&country=IN&view_all_page_id=333533779624'
    '&sort_data[direction]=desc&sort_data[mode]=relevancy_monthly_grouped&search_type=page&media_type=all'
    '&content_languages[0]=en')
print(driver.title)
driver.implicitly_wait(15)


def make_list(web_iter, name):
    text_list = []
    for i in web_iter:
        if name != 'images':
            text_list.append(i.text)
        else:
            text_list.append(i.get_attribute("src"))

    df = pd.DataFrame()
    df[name] = text_list
    df = df[df[name] != ""]
    # df = df.un
    df.to_csv(name + '.csv', index=False)


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
        time.sleep(1)
        driver.execute_script((
            "var scrollingElement = (document.scrollingElement ||"
            " document.body);scrollingElement.scrollTop ="
            " scrollingElement.scrollHeight;"))
        # Get new position
        new_position = driver.execute_script(
            ("return (window.pageYOffset !== undefined) ?"
             " window.pageYOffset : (document.documentElement ||"
             " document.body.parentNode || document.body);"))

for i in range(0,10):
    print(i)
    scroll_to_bottom(driver)

time.sleep(5)
# search = driver.find_elements(By.CLASS_NAME, '_9b9x')
# print(len(search)

primary_text = driver.find_elements(By.XPATH, '//div[@class="_7jyr" or (@class = "_7jyr _a25-")]')
header_2 = driver.find_elements(By.XPATH, '//div[@class="_8jh2"]')
header_3 = driver.find_elements(By.XPATH, '//div[@class="_8jh3"]')
image = driver.find_elements(By.XPATH, '//img[@class="_7jys img"]')
callta = driver.find_elements(By.XPATH, '//div[@class="_8jh0"]')

print(len(primary_text))
print(len(header_2))
print(len(header_3))
print(len(callta))
print(len(image))

make_list(primary_text, 'primary_text')
make_list(header_2, 'header_2')
make_list(header_3, 'header_3')
make_list(image, 'images')
make_list(callta, 'CTA')

# driver.quit()
