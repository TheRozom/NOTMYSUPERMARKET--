from bs4 import BeautifulSoup
import pandas
from selenium import webdriver
import time
import requests
import re
import pandas as pd

url4 = "https://quik.co.il/products/%D7%A7%D7%A0%D7%99%D7%99%D7%94_%D7%9C%D7%A4%D7%99_%D7%94%D7%A1%D7%99%D7%93%D7%95%D7%A8_%D7%91%D7%91%D7%99%D7%AA/%D7%90%D7%A8%D7%95%D7%A0%D7%95%D7%AA_%D7%9E%D7%96%D7%95%D7%9F/%D7%97%D7%98%D7%99%D7%A4%D7%99%D7%9D"
url = "https://quik.co.il/search-result/%D7%91%D7%9E%D7%91%D7%94?q=%D7%91%D7%9E%D7%91%D7%94"
url2 = "https://quik.co.il/products/%D7%A7%D7%A0%D7%99%D7%99%D7%94_%D7%9C%D7%A4%D7%99_%D7%94%D7%A1%D7%99%D7%93%D7%95%D7%A8_%D7%91%D7%91%D7%99%D7%AA/%D7%9E%D7%A9%D7%A7%D7%90%D7%95%D7%AA/%D7%9E%D7%A9%D7%A7%D7%90%D7%95%D7%AA_%D7%9E%D7%95%D7%92%D7%96%D7%99%D7%9D"
url3 = "https://quik.co.il/products/%D7%A7%D7%A0%D7%99%D7%99%D7%94_%D7%9C%D7%A4%D7%99_%D7%94%D7%A1%D7%99%D7%93%D7%95%D7%A8_%D7%91%D7%91%D7%99%D7%AA/%D7%98%D7%A8%D7%99_%D7%95%D7%9E%D7%A7%D7%A8%D7%A8/%D7%A4%D7%99%D7%A8%D7%95%D7%AA_%D7%95%D7%99%D7%A8%D7%A7%D7%95%D7%AA"
url5 = "https://quik.co.il/products/%D7%A7%D7%A0%D7%99%D7%99%D7%94_%D7%9C%D7%A4%D7%99_%D7%94%D7%A1%D7%99%D7%93%D7%95%D7%A8_%D7%91%D7%91%D7%99%D7%AA/%D7%90%D7%A8%D7%95%D7%A0%D7%95%D7%AA_%D7%9E%D7%96%D7%95%D7%9F/%D7%A9%D7%95%D7%A7%D7%95%D7%9C%D7%93_%D7%95%D7%9E%D7%9E%D7%AA%D7%A7%D7%99%D7%9D"
merged_df = pd.DataFrame(columns=["NAME", "PRICE", "GRAM"])
urls = [url, url2, url3, url4, url5]
df2 = 0

for url in urls:
    # Set up the webdriver
    driver = webdriver.Chrome()
    driver.get(url)

    driver.implicitly_wait(15)

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

    html = driver.page_source

    soup = BeautifulSoup(html, "html.parser")

    units = soup.find_all(name="div", class_="name__7t")
    units_list = [unit.getText() for unit in units]
    print(units_list)

    unit_name_list = []
    unit_gram_list = []
    # כדי להפריד את השם מהגרם שהיה מחובר אליו
    for unit in units_list:
        try:
            unit = unit.split(" ")
            unit_name = " ".join(unit[:-2])

            unit_gram = float(unit[-2])
            unit_name_list.append(unit_name)
            unit_gram_list.append(unit_gram)
        except:
            pass
    # יצירת מחיר 1 ושלא יהיה ב2 משתנים
    units_price_shekels = soup.find_all(name="strong", class_="")
    units_price_agorot = soup.find_all(name="small", class_="")
    units_price_agorot.pop(0)
    units_price_agorot.pop(0)

    units_price_agorot = [unit.getText() for unit in units_price_agorot]

    unit_price_shekels = [unit.getText() for unit in units_price_shekels]
    unit_price_shekels.pop(0)

    unit_price_list = [
        unit[0] + "." + unit[1] for unit in zip(unit_price_shekels, units_price_agorot)
    ]
    # חיבור של הכל

    # Create a new pandas DataFrame for the current URL
    df = pd.DataFrame(columns=["NAME", "PRICE", "GRAM"])

    for unit in zip(unit_name_list, unit_price_list, unit_gram_list):
        try:
            df.loc[len(df.index)] = [unit[0], unit[1], unit[2]]
        except:
            pass
    print(df)

    # Append the new DataFrame to the existing one
    merged_df = pd.concat([merged_df, df])

    driver.quit()

merged_df = merged_df.reset_index(drop=True)

print(merged_df)

merged_df.to_excel("quik.xlsx")
