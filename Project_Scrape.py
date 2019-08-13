from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.command import Command
from os import system
import string
import re
import csv


def loadPageUntilID(id):
    global browser
    try:
        element = WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.ID, id)))
    except:
        pass
        

def appSetup():
    global browser
    browser.get("http://www2.county.allegheny.pa.us/RealEstate/Default.aspx")
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
    loadPageUntilID("textStreetNum")

    HouseNum = browser.find_element_by_id("txtStreetNum")
    Street = browser.find_element_by_id("txtStreetName")
    
    HouseNum.send_keys(house_num)
    Street.send_keys(st_name)
    
    go = browser.find_element_by_id("btnSearch")
    go.click()

    # Results are returned
    # Check for proper results

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

# appSetup()

def main():
    global browser
    system("ls -l")

    # leads = input("\nEnter the name of your leads file: ")
    # output = input("Name of output file: ")

    browser = webdriver.Safari()

    ## Leads Input File
    # file = open(leads, 'r')
    # muni = file.read()
    # file.close()

    ## Property Output File
    properties = open('test.csv', mode='w')
    prop_writer = csv.writer(properties, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    prop_writer.writerow(['Address', 'City', 'State', 'ZipCode', 'Name'])

    appSetup()
    property = Search("6419", "Deary", "St")
    prop_writer.writerow(property)
    property = Search("1840", "Jancey", "st")
    prop_writer.writerow(property)


    # Close all the files that are open
    properties.close()
    browser.quit()


if __name__ == "__main__":
    main()