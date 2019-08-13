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
