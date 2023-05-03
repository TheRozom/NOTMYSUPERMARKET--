from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time

# Set up the webdriver
driver = webdriver.Chrome()
driver.get('https://www.shufersal.co.il/online/he/%D7%A7%D7%98%D7%92%D7%95%D7%A8%D7%99%D7%95%D7%AA/%D7%A1%D7%95%D7%A4%D7%A8%D7%9E%D7%A8%D7%A7%D7%98/%D7%97%D7%98%D7%99%D7%A4%D7%99%D7%9D%2C-%D7%9E%D7%AA%D7%95%D7%A7%D7%99%D7%9D-%D7%95%D7%93%D7%92%D7%A0%D7%99-%D7%91%D7%95%D7%A7%D7%A8/c/A25')

driver.implicitly_wait(10)

lenOfPage = driver.execute_script(
    "window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
while True:
    lastCount = lenOfPage
    time.sleep(2)
    lenOfPage = driver.execute_script(
        "window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
    if lastCount == lenOfPage:
        break

html = driver.page_source


# Scroll down the page
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
