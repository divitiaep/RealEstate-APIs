from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.command import Command
from os import system
import string
import re
import csv
import selenium
import os
# num = []
# st = []
# tpe = []

def loadPageUntilID(id):
    global browser
    try:
        element = WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.ID, id)))
    except TimeoutException:
        pass
        

def appSetup():
    global browser
    browser.get("http://www2.county.allegheny.pa.us/RealEstate/Default.aspx")
    # loadPageUntilID("footer-text")
    Agree = browser.find_element_by_id("btnContinue")
    Agree.click()

def Search(house_num, st_name, st_type):
    global browser
    # [Uncomment] This is a new feature
    browser.get("http://www2.county.allegheny.pa.us/RealEstate/Search.aspx")

    # Remove any puncations and Uppercase the letters
    st_name = st_name.translate(str.maketrans('', '', string.punctuation)).upper()
    st_type = st_type.translate(str.maketrans('', '', string.punctuation)).upper()

    # Search for Property Address
    loadPageUntilID("txtStreetNum")

    HouseNum = browser.find_element_by_id("txtStreetNum")
    Street = browser.find_element_by_id("txtStreetName")
    
    HouseNum.send_keys(house_num)
    Street.send_keys(st_name)
    
    go = browser.find_element_by_id("btnSearch")
    go.click()


    # Results are returned
    # Check for multiple results

    try:
        loadPageUntilID("dgSearchResults")
        mult_list = browser.find_element_by_id("dgSearchResults")
        print("found it")
        rowCount = len(browser.find_elements_by_xpath("//table[@id='dgSearchResults']/tbody/tr"))
        print(rowCount)
        check = house_num + " " + st_name + " " + st_type

        for row in range(2, rowCount-1):
            row = str(row)
            text = browser.find_element_by_xpath("//table[@id='dgSearchResults']/tbody/tr[" + row + "]/td[3]").text.replace(' ', '')
            check = check.replace(' ', '')

            if check.replace(' ', '') == text.replace(' ', ''):
                print("We Found A Match!")
                link = browser.find_element_by_xpath("//table[@id='dgSearchResults']/tbody/tr[" + row + "]/td[1]")
                link.click()
                browser.quit()
                break
    except NoSuchElementException:
        print("No Multiple listings")


    # Results are good, then parse Results
    loadPageUntilID("BasicInfo1_lblParcelID")

    parcelId = browser.find_element_by_id("BasicInfo1_lblParcelID").text
    owner = browser.find_element_by_id("BasicInfo1_lblOwner").text

    # parse the Address
    addr = browser.find_element_by_id("BasicInfo1_lblAddress").text
    city, state, zipcode = addrParser(st_type, addr)
    address = house_num + " " + st_name + " " + st_type

    return [address, city, state, zipcode, owner]

# Returns City, State, and ZipCode
def addrParser(st_type, addr):
    parts = re.findall(r"[\w']+", addr)

    if(len(parts) == 6):
        city = parts[3]
        state = parts[4]
        zipcode = parts[5]
    elif (len(parts) == 5):
        #remove street Type from parts[2]
        city = parts[2].replace(st_type, '')
        state   = parts[3]
        zipcode = parts[4]
      
    return city, state, zipcode


def main():
    global browser

    # system("ls -l")

    # leads = input("\nEnter the name of your leads file: ")
    # output = input("Name of output file: ")

    props = open("Leads List 1")
    properties = open('test.csv', mode='w')
    prop_writer = csv.writer(properties, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    prop_writer.writerow(['Address', 'City', 'State', 'ZipCode', 'Name'])

    browser = webdriver.Chrome()
    appSetup()


    for prop in props:
        x = re.search("\d{1,5}\s+(\D\s+)?\w+\s+\w{2,4}", prop)
        print(x.group())
        x = re.split('\s+', x.group())
        if(len(x) == 4):
            x = [x[0], x[1] + ' ' + x[2], x[3]]
        property = Search(x[0],x[1], x[2])
        print(property)


    
        # property = Search("6419", "Deary", "St")
        # prop_writer.writerow(property)
        # property = Search("1840", "Jancey", "st")
        # prop_writer.writerow(property)


    # Close all the files that are open
    props.close()
    properties.close()
    browser.quit()


if __name__ == "__main__":
    main()
