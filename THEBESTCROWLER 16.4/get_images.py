from bs4 import BeautifulSoup
import pandas
from selenium import webdriver
import time
import requests
# Set up the webdriver

response = requests.get('https://www.shufersal.co.il/online/he/%D7%A7%D7%98%D7%92%D7%95%D7%A8%D7%99%D7%95%D7%AA/%D7%A1%D7%95%D7%A4%D7%A8%D7%9E%D7%A8%D7%A7%D7%98/%D7%97%D7%98%D7%99%D7%A4%D7%99%D7%9D%2C-%D7%9E%D7%AA%D7%95%D7%A7%D7%99%D7%9D-%D7%95%D7%93%D7%92%D7%A0%D7%99-%D7%91%D7%95%D7%A7%D7%A8/c/A25')

soup = BeautifulSoup(response.text, "html.parser")

image_list = soup.find_all(name="a", class_='imgContainer')
images_src = [image.find(name="img")['src'] for image in image_list ] 
print(images_src)

# for image in image_list:
#     print(image['src'])

