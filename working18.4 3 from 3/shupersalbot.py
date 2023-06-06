from bs4 import BeautifulSoup
import pandas
from selenium import webdriver
import time

# Set up the webdriver
driver = webdriver.Chrome()
driver.get(
    "https://www.shufersal.co.il/online/he/%D7%A7%D7%98%D7%92%D7%95%D7%A8%D7%99%D7%95%D7%AA/%D7%A1%D7%95%D7%A4%D7%A8%D7%9E%D7%A8%D7%A7%D7%98/%D7%97%D7%98%D7%99%D7%A4%D7%99%D7%9D%2C-%D7%9E%D7%AA%D7%95%D7%A7%D7%99%D7%9D-%D7%95%D7%93%D7%92%D7%A0%D7%99-%D7%91%D7%95%D7%A7%D7%A8/c/A25"
)
# כניסה לאתר מלקוח מזויף
driver.implicitly_wait(10)

lenOfPage = driver.execute_script(
    "window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;"
)

while True:
    lastCount = lenOfPage
    time.sleep(2)
    lenOfPage = driver.execute_script(
        "window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;"
    )
    if lastCount == lenOfPage:
        break
    # טעינה של כל ה html

html = driver.page_source

soup = BeautifulSoup(html, "html.parser")
units_name = soup.find_all(name="div", class_="text description")
unit_name_list = [unit.find(name="strong").getText() for unit in units_name]

units_price = soup.find_all(name="span", class_="price")
unit_price_list = [
    unit.find(name="span", class_="number").getText() for unit in units_price
]

unit_gram = soup.find_all(class_="smallText", name="div")
unit_gram_list = [unit.find(name="span") for unit in unit_gram]
unit_gram_list = [unit.getText() for unit in unit_gram_list if unit != None]

image_list = soup.find_all(name="a", class_="imgContainer")
images_src = [image.find(name="img")["src"] for image in image_list]

df = pandas.DataFrame(columns=["NAME", "PRICE", "GRAM", "IMAGE_LINK"])

for unit in zip(unit_name_list, unit_price_list, unit_gram_list, images_src):
    df.loc[len(df.index)] = [unit[0], unit[1], unit[2], unit[3]]
print(df)
df.to_excel("shufersal.xlsx")
