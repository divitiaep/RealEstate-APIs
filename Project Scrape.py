from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import os
import re

# browser = webdriver.Safari()
#
# browser.get("http://www2.county.allegheny.pa.us/RealEstate/Default.aspx")
#
# # browser.maximize_window()
#
# Agree = browser.find_element_by_id("btnContinue")
# Agree.click()
#
# try:
#     element = WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.ID, "txtStreetNum")))
# except:
#     pass
# HouseNum = browser.find_element_by_id("txtStreetNum")
# HouseNum.send_keys("1840")
#
# Street = browser.find_element_by_id("txtStreetName")
# Street.send_keys("JANCEY")
#
# go = browser.find_element_by_id("btnSearch")
# go.click()
#
# try:
#     element = WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.ID, "BasicInfo1_lblParcelID")))
# except:
#     pass
#
#
# ParcelId = browser.find_element_by_id("BasicInfo1_lblParcelID")
# # print("Parcel ID: " + ParcelId.text)
#
# Address = browser.find_element_by_id("BasicInfo1_lblAddress")
# # print("Address: " + Address.text)
#
# owner = browser.find_element_by_id("BasicInfo1_lblOwner")
# # print("Owner: " + owner.text)
#
# browser.quit()

FileName = os.path.expanduser("~/Documents/Properties.txt")

PropFile = open(FileName,"r+")

with open(FileName) as f:
    lines = [line.rstrip('\n') for line in open(FileName)]

addresses = []

for items in lines:
    lowercase = items.lower()
    if "north" in lowercase:
        newStr = lowercase.replace("north", "N")
        addresses.append(newStr)
    elif "south" in lowercase:
        newStr = lowercase.replace("south", "S")
        newStr = addresses.append(newStr)
    elif "east" in lowercase:
        newStr = lowercase.replace("east", "E")
        newStr = addresses.append(newStr)
    elif "west" in lowercase:
        newStr = lowercase.replace("west", "W")
        newStr = addresses.append(newStr)
    else:
        addresses.append(items)

    print(items)
print(addresses)

