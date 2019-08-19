# PROJECT SCRAPE
#   Project Scrape is part of a larger goal of closing deals. 
#   In Project Scrape we take a list a addresses and feed them
#   through publics records to scrape property and owner information
# 
#   Copyright (C) Divitiae Properties, LLC - All Rights Reserved
#   Unauthorized copying of this file, via any medium is strictly prohibited
#   Proprietary and confidential
#   Written by Malik Parker <divitiaep@gmail.com>, August 2019
#   Written by Darius Davis <divitiaep@gmail.com>, August 2019
# 
import string, re, csv, os, argparse, pickle

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.command import Command
from selenium.common.exceptions import TimeoutException
from os import system

# Wait for the page to load before taking action
def loadPageUntilID(id1, id2=None):
    global browser
    try:
        (WebDriverWait(browser, 2).until(EC.presence_of_element_located((By.ID, id1))))
        return id1
    except TimeoutException:
        try:
            return (WebDriverWait(browser, 2).until(EC.presence_of_element_located((By.ID, id2))))
            return id2
        except:
            return -1
            # browser.quit()
            # if(id2==None):
            #     print("TIMEOUT while Looking for element id: " + id1)
            # else:
            #     print("TIMEOUT while Looking for element id: " + id2)
            # exit()

# Compare Property Address with that of Search Results
def addrCompare(prop1, prop2=None):
    x1 = re.search("\d{1,5}\s+(\D\s+)?\w+\s+\w{2,4}", prop1)
    x1 = re.split('\s+', x1.group())

    if(prop2):
        x2 = re.search("\d{1,5}\s+(\D\s+)?\w+\s+\w{2,4}", prop2)
        x2 = re.split('\s+', x2.group())
        # print(x1, end='\t')
        # print(x2)
        return x1 == x2
    else:
        return x1

# Cleanly exit the program 
def leave():
    global browser
    browser.quit()
    exit()

# Setup the program environment
def appSetup():
    global browser
    browser.get("http://www2.county.allegheny.pa.us/RealEstate/Default.aspx")
    # loadPageUntilID("btnContinue")
    Agree = browser.find_element_by_id("btnContinue")
    webdriver.ActionChains(browser).move_to_element(Agree).click(Agree).perform()

# Returns City, State, and ZipCode
def addrParser(st_type, addr):
    parts = re.findall(r"[\w']+", addr)

    if(len(parts) == 7):
        city = parts[3] + " " + parts[4]
        state = parts[5]
        zipcode = parts[6]
    elif(len(parts) == 6):
        city = parts[3]
        state = parts[4]
        zipcode = parts[5]
    elif (len(parts) == 5):
        #remove street Type from parts[2]
        city = parts[2].replace(st_type, '')
        state   = parts[3]
        zipcode = parts[4]
      
    return city, state, zipcode

# Search for Property Address, State, Zipcode, & Owner
def Search(house_num, st_name, st_type):
    global browser
    # [Uncomment] This is a new feature
    browser.get("http://www2.county.allegheny.pa.us/RealEstate/Search.aspx")

    # Search for Property Address
    if(loadPageUntilID("txtStreetNum") == -1):
        return -1

    HouseNum = browser.find_element_by_id("txtStreetNum")
    Street = browser.find_element_by_id("txtStreetName")
    
    HouseNum.send_keys(house_num)
    Street.send_keys(st_name)
    
    go = browser.find_element_by_id("btnSearch")
    webdriver.ActionChains(browser).move_to_element(go).click(go).perform()

    # Results are returned
    # Check for multiple results
    element = loadPageUntilID("dgSearchResults", "Table1")
    skip = 0
    if(element == "dgSearchResults"):
        address = house_num + " " + st_name + " " + st_type
        rowCount = len(browser.find_elements_by_xpath("//table[@id='dgSearchResults']/tbody/tr"))
        for rowNum in range(2,rowCount):
            row = browser.find_elements_by_xpath("//table[@id='dgSearchResults']/tbody/tr[" + str(rowNum) +"]/td")
            if(addrCompare(row[2].text, address)):
                parcel = row[0].text.replace('-','')
                link = "http://www2.county.allegheny.pa.us/RealEstate/GeneralInfo.aspx?ParcelID=" + parcel
                browser.get(link)
                if(loadPageUntilID("Table1") == -1):
                    return -1
                skip = 1
                break
        # Address Wasn't Found in Search Table
        if(not skip):
            return -1
    elif(element == -1):
        return -1


    # Results are good, then parse Results
    parcelId = browser.find_element_by_id("BasicInfo1_lblParcelID").text
    owner = browser.find_element_by_id("BasicInfo1_lblOwner").text

    # parse the Address
    addr = browser.find_element_by_id("BasicInfo1_lblAddress").text
    city, state, zipcode = addrParser(st_type, addr)
    address = house_num + " " + st_name + " " + st_type

    return [address, city, state, zipcode, owner]

def main():
    global browser

    # Parsing the Command-Line Arguments
    parser = argparse.ArgumentParser(description="Retrieve Owners from a Leads List")
    parser.add_argument('-f', action="store", help="Lead's List Input File")
    x = vars(parser.parse_args())

    try:
        in_file = (x['f'])
        out_file = in_file + "_out.csv"
        # Gets the file names for input and output files
        leads_file = open(in_file)
        csv_out = open(out_file, mode='w')
    except FileNotFoundError:
        print("Filename Doesn't Exist! Please check your spelling")
        exit()
    except:
        parser.print_help()
        exit()

    # Setup the CSV output file
    prop_writer = csv.writer(csv_out, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    prop_writer.writerow(['Address', 'City', 'State', 'ZipCode', 'Name'])

    # Setup Browser Environment
    browser = webdriver.Chrome()
    appSetup()

    # Open up the Properties Database 
    try:
        database = open('Support/database.dp', 'rb')
        invalid_properties, previous_properties = pickle.load(database)
        print(invalid_properties)
        print(previous_properties)
        database.close()
    except:
        system("mkdir Support")
        system("touch Support/database.dp")
        invalid_properties = {}
        previous_properties = {}

    for prop in leads_file:
        addr = re.search("\d{1,5}\s+(\D\s+)?\w+\s+\w{2,4}", prop)
        x = re.split('\s+', addr.group())
        # Some municipalties are 2 words. 
        #   Ex. West Mifflin
        if(len(x) == 4):
            x = [x[0], x[1] + ' ' + x[2], x[3]]

        # Remove any puncations and Uppercase the letters
        st_name = x[1].translate(str.maketrans('', '', string.punctuation)).upper()
        st_type = x[2].translate(str.maketrans('', '', string.punctuation)).upper()
        

        # No match in our Database
        addr = x[0] + " " + x[1] + " " + x[2]
        if(not ((addr in previous_properties) or (addr in invalid_properties))):
            property = Search(x[0],st_name, st_type)

            # Invalid Address
            if(property == -1):
                print(addr + " - Is an Invalid Address")
                invalid_properties[addr] = addr
            
            # We got a result
            else:
                print(property)
                prop_writer.writerow(property)
                previous_properties[addr] = property
                
    # Update the database
    print("Saving files: Do NOT TURN OFF Program")
    database_data = [invalid_properties, previous_properties]
    database = open("Support/database.dp", "wb")
    pickle.dump(database_data, database)

    # Close all the files that are open
    leads_file.close()
    csv_out.close()
    browser.quit()


if __name__ == "__main__":
    main()