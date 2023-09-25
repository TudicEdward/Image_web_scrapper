#import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from PIL import Image
import urllib
import time


#inputs
object_to_search = "Pets"
number_of_pictures = 100
filter_min_height = 100
filter_min_width = 100
filter_max_height = 1000
filter_max_width = 1000
resize = True
resize_width = 500
resize_height = 500

#location of the driver for edge browser inside the project folder
s = Service("D:\Faculta\CV\Project\msedgedriver.exe")
text = "Before you continue to Google"
driver = webdriver.Edge(service=s)
width = False
height = True

#Launch Browser on images url
driver.get("https://www.google.com/imghp?hl=EN")
if text in driver.page_source:
    buttons = driver.find_elements(By.XPATH, "//*[contains(text(), 'Accept all')]")
    for btn in buttons:
        btn.click()

#seach for prefference
search = driver.find_element(By.NAME,'q')
search.send_keys(object_to_search)
search.send_keys(Keys.RETURN)

#Load the images
if number_of_pictures > 50:
    for counter in range(int(number_of_pictures/25)):
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
        time.sleep(2)
driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
time.sleep(2)

#Find and extract images
imgResults = driver.find_elements(By.XPATH,"//img[contains(@class,'Q4LuWd')]")
src = []
for img in imgResults:
    for i,j in  img.size.items():
        if i == "height":
            if j >= filter_min_height and j <= filter_max_height:
                height = True
            else:
                height = False
        elif i == "width":
            if j >= filter_min_width and j <= filter_max_width:
                width = True
            else:
                width = False
    if height and width and img.get_attribute('src')!=None:
        src.append(img.get_attribute('src'))
if len(src) == 0:
    print("There are no files with the desired size")
else:
    #Download images
    for z in range(number_of_pictures):      
        urllib.request.urlretrieve(str(src[z]),"images/{}.jpeg".format(z))
driver.close()

if resize:
    for image_name in range(number_of_pictures):
        image = Image.open('images/{}.jpeg'.format(image_name)).convert('RGB').save('images/{}.jpeg'.format(image_name))
        image = Image.open('images/{}.jpeg'.format(image_name))
        new_image = image.resize((resize_width,resize_height))
        new_image.save('images/{}.jpeg'.format(image_name))