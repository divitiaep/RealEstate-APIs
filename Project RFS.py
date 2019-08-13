# importing the requests library 
import requests 
from xml.etree.ElementTree import ET 
  
# # api-endpoint 
# URL = "http://maps.googleapis.com/maps/api/geocode/json"
  
# # location given here 
# location = "delhi technological university"
  
# # defining a params dict for the parameters to be sent to the API 
# PARAMS = {'address':location} 
  
# # sending get request and saving the response as response object 
# r = requests.get(url = URL, params = PARAMS) 
  
# # extracting data in json format 
# data = r.json() 
  
  
# # extracting latitude, longitude and formatted address  
# # of the first matching location 
# latitude = data['results'] 
# # longitude = data['results'][0]['geometry']['location']['lng'] 
# # formatted_address = data['results'][0]['formatted_address'] 
  
# # printing the output 
# print("Latitude:%s\n"
#       %(latitude)) 
# print("Data:%s\n"
#       %(data))
# # print("Longitude:%s\n"
# #       %(longitude))

URL = "http://www.zillow.com/webservice/GetDeepSearchResults.htm?zws-id=X1-ZWz17r5sqd32mj_aypsc&address=2114+Bigelow+Ave&citystatezip=Seattle%2C+WA"

response = requests.get(url = URL)

tree = ElementTree.fromstring(response.content)

data = response.text

# print("Data:%s\n"
#       %(data))
print("Tree:%s\n"
      %(tree))