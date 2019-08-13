import requests
from bs4 import BeautifulSoup
from csv import writer

# response = requests.get('https://www.swlahec.com/2016/09/06/sample-blog-post-3/')
#
# soup = BeautifulSoup(response.text, 'html.parser')
#
# # print(response.text)
# title = soup.find(class_='entry-title')
# date = soup.find(class_='date updated')
# post = soup.find(class_='entry-content clearfix')
#
# print('Title: ')
# print(title.get_text())
# print('\n')
#
# print('Date: ')
# print(date.contents[0].get_text())
# print('\n')
#
#
# print('Post: ')
# print(post.get_text())
# print('\n')


from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

browser = webdriver.Safari()

browser.get("http://www2.county.allegheny.pa.us/RealEstate/Default.aspx")

# browser.maximize_window()

Agree = browser.find_element_by_id("btnContinue")
Agree.click()

try:
    element = WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.ID, "txtStreetNum")))
except:
    pass
HouseNum = browser.find_element_by_id("txtStreetNum")
HouseNum.send_keys("1840")

Street = browser.find_element_by_id("txtStreetName")
Street.send_keys("JANCEY")

go = browser.find_element_by_id("btnSearch")
go.click()

try:
    element = WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.ID, "BasicInfo1_lblParcelID")))
except:
    pass


ParcelId = browser.find_element_by_id("BasicInfo1_lblParcelID")
print("Parcel ID: " + ParcelId.text)

Address = browser.find_element_by_id("BasicInfo1_lblAddress")
print("Address" + Address.text)

owner = browser.find_element_by_id("BasicInfo1_lblOwner")
print("Owner: " + owner.text)

browser.quit()
