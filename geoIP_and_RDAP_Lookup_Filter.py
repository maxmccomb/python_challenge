# -*- coding: utf-8 -*-
"""
Created on Thu Oct 25 18:59:51 2018



@author: Maxwell McComb
"""
import re
import urllib.request
import json
import ipwhois
from ipwhois import IPWhois
from guizero import App, PushButton, Text, Combo, TextBox, Window


class Address:
    #constructor, accepts GeoIP lookup data and sets RDAP lookup data to the empty String
    def __init__(self, add, busN, busW, cit, reg, coun, counC, cont, ipN, 
                     ipT, isp, lat, lon, org, quer):
        self.ip_address = add
        self.business_name = busN
        self.business_website = busW
        self.city = cit
        self.region = reg
        self.country = coun
        self.country_code = counC
        self.continent = cont
        self.ip_name = ipN
        self.ip_type = ipT
        self.isp = isp
        self.latitude = lat
        self.longitude = lon
        self.organization = org
        self.query = quer
        self.asn=self.asn_cidr=self.asn_country_code=self.asn_date= ""
        self.asn_registry=self.asn_description=self.start_address= ""
        self.end_address=self.handle=self.ip_version=self.name= ""
        self.parent_handle=""
        
    #prints GeoIP lookup data when called on by an IP Object  
    def printGeoIPData(self):
        s = "GeoIP Lookup Data:  " + "\nIP Address: " + self.ip_address
        
        for i in range (len(geoCriteriaList)):
            s = s + "\n" + geoCriteriaList[i] + ": " +  self.findField(geoCriteriaList[i]) 
        return s
        
    #prints RDAP lookup data when called on by an IP Object    
    def printRDAPData(self):
        s = "RDAP Lookup Data:  "
        print(len(rdapCriteriaList))
        for i in range (len(rdapCriteriaList)):
            print(i)
            s = s + "\n" + rdapCriteriaList[i] + ": " +  self.findField(rdapCriteriaList[i])
        print(s)
        return s
    
    #uses the criteria to return which field is to be accessed when filtering
    # @param (criteria): a string of the criteria to be matched to a field
    # @return: the field that is to be accessed
    def findField(self, criteria):
        return{
                "Business Name": self.business_name,
                "Business Website": self.business_website,
                "City": self.city,
                "Region": self.region,
                "Country" : self.country,
                "Country Code": self.country_code,
                "Continent": self.continent,
                "IP Name": self.ip_name,
                "IP Type": self.ip_type,
                "ISP": self.isp,
                "Latitude": self.latitude,
                "Longitude": self.longitude,
                "Organization": self.organization,
                "Query": self.query,
                "ASN" : self.asn,
                "ASN Routing Block" : self.asn_cidr,#network routing block assigned to ASN
                "ASN Country Code": self.asn_country_code,
                "ASN Date": self.asn_date,
                "ASN Registry": self.asn_registry,
                "ASN Description": self.asn_description,
                "Start Address": self.start_address, #The start IP address in a network block
                "End Address": self.end_address, #The last IP address in a network block
                "Handle": self.handle, #Unique identifier for a registered object
                "IP Version": self.ip_version, #IPv4 or IPv6
                "Name": self.name,
                "Parent Handle": self.parent_handle,
        }[criteria]

#finds IP addresses in a given text file
# @param (textFile): a String of the filepath of the text file with 
#    IP addresses
# @return (addresses): a list of all of the IP addresses found in the 
#    text file as Strings
# Citation: re.findall from: https://stackoverflow.com/questions/
#         44469999/how-to-read-list-of-ip-address-from-a-text-file-and-print-it-out
def findIPAddresses(textFile):
    file = open(textFile, 'r')
    text = file.read()
    addresses = re.findall( r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", text)
    return addresses

#does a geoIP lookup on a given IP address by requesting information from 
#   an online API (extreme-ip-lookup.com) and recieves that information in 
#   the form of a json file
# @param (ip_address): the IP address that a geoIP lookup will be performed on
# @return (obj): the ipAddress object that will now stores all geoIP lookup data.
#   Now it can be added to a running list of objects.
def geoIP_lookup(ip_address):  
    url = "http://extreme-ip-lookup.com/json/" + ip_address
    request = urllib.request.Request(url)
    response = urllib.request.urlopen(request)    
    geo = json.load(response)
    obj = Address(ip_address,geo["businessName"],geo["businessWebsite"],
                  geo["city"],geo["region"],geo["country"],geo["countryCode"],
                  geo["continent"],geo["ipName"],geo["ipType"],geo["isp"],
                  geo["lat"],geo["lon"],geo["org"],geo["query"])
    return obj

#does a whois/RDAP lookup on a given IP address using a Python package called 
#   IPWhois.  That package returns a dictionary of results
# @param (ip_address): the IP address that a RDAP lookup will be performed on
# @param (addressObj): the IP address object that will have its data fields updated
def RDAP_lookup(ip_address, addressObj):
    try:
        obj = IPWhois(ip_address)
    except ipwhois.exceptions.IPDefinedError:
        results = {}
    else:
        try:
            results = obj.lookup_rdap(depth=1)
        except ipwhois.exceptions.HTTPLookupError:
            addressObj.asn = ""
        else: #sets RDAP lookup fields for addressObj. Done this way to try to keep GeoIP and RDAP seperate
            addressObj.asn = results["asn"]
            addressObj.asn_cidr = results["asn_cidr"]
            addressObj.asn_country_code = results["asn_country_code"]
            addressObj.asn_date = results["asn_date"]
            addressObj.asn_registry = results["asn_registry"]
            addressObj.asn_description = results["asn_description"]
            addressObj.start_address = results["network"]["start_address"]
            addressObj.end_address = results["network"]["end_address"]
            addressObj.handle = results["network"]["handle"]
            addressObj.ip_version = results["network"]["ip_version"]
            addressObj.name = results["network"]["name"]
            addressObj.parent_handle = results["network"]["parent_handle"]
            
# filters IP addresses by passed in criteria and the value of that criteria
# @param (criteria): the field to be looked at i.e. "Country", "City", etc
# @param (value): the value to be compared.  The IP address of the object will
#                   be added to the filtered list if the value of the field 
#                   matches value
def filterBy(criteria, value):
    if(criteria == "" or value == ""):
        return ip_objects
    else:
        fList = []
        for i in range(len(ip_objects)):
            if(ip_objects[i].findField(criteria) == value):
                fList.append(ip_objects[i].ip_address)
        return fList

#prints GeoIP data given an IP as a String
def printGeoData(ip):
    s = ""
    for i in range(len(ip_objects)):
        currentIP = ip_objects[i]
        if(ip == currentIP.ip_address):
            s = currentIP.printGeoIPData()
    return s        
            
#prints RDAP data given an IP as a String           
def printRDAPData(ip):
    s = ""
    for i in range(len(ip_objects)):
        currentIP = ip_objects[i]
        if(ip == currentIP.ip_address):
            s = currentIP.printRDAPData()
    return s

#initializes a list of IP Objects with GeoIP and RDAP data stored in its fields           
def initialize():
    fileToSearch = 'list_of_ips.txt'
    ip_addresses = findIPAddresses(fileToSearch) #list of IP addresses found in text file
    for i in range(10): #would use len(ip_addresses) instead of 10 but the lookups are very 
                        #   inefficient and take a long time to compute
        a = (geoIP_lookup(ip_addresses[i]))
#        a = Address("", "", "", "", "", "", "", "", "", "", "", "", "", "", "") #if user only wants RDAP data
        RDAP_lookup(ip_addresses[i], a) #updates fields for the object so it has correct RDAP lookup data
        if(a != None):
            ip_objects.append(a)
            print("added object ", i)
    print("Object List Created")

#formats the output of the ip addresses
# @param: (ipList): the list of filtered IPs to be formatted
def formatList(ipList):
    s = ""
    for i in range (len(ipList)):
        s = s + ipList[i] + "\n"
    return s

#when the filter button is clicked, a list of IPs is created based on the 
#   filter constraints provided by the user
def handleFilterButton():
    criteria = criteriaOptions.value
    value = valueTextBox.value
    resultFilterList = filterBy(criteria, value)        
    resultText.value = formatList(resultFilterList) #outputs the filtered IPs

#prints the GeoIP lookup data to a new window    
def handleGeoButton():
    tempIndex = ipIndexTextBox.value
    index = int(tempIndex)
    print (index)
    if(index > len(ip_objects)):
        geoWText.append("Invalid Index")
    else:
        geoWText.append(printGeoData(ip_objects[index].ip_address))
    geoWindow.show()

#prints the RDAP lookup data to a new window
def handleRDAPButton():
    index = int(ipIndexTextBox.value)
    if(index > len(ip_objects)):
        rdapWText.append("Invalid Index")
    else:
        rdapWText.append(printRDAPData(ip_objects[index].ip_address))
    rdapWindow.show()
        
        
ip_objects = [] #declaration of a list of IP Objects

                # list of criteria options to be filtered by
criteriaList = ["Business Name","Business Website","City","Region","Country",
                "Country Code","Continent","IP Name","IP Type", "ISP", "Latitude",
                "Longitude","Organization","Query","ASN","ASN Routing Block",
                "ASN Country Code","ASN Date","ASN Registry","ASN Description",
                "Start Address","End Address","Handle","Parent Handle","IP Version",
                "Name","RIR classification"] 

                # list of criteria options for just GeoIP data
geoCriteriaList = ["Business Name","Business Website","City","Region","Country",
                "Country Code","Continent","IP Name","IP Type", "ISP", "Latitude",
                "Longitude","Organization","Query"]
                   
                # list of criteria options for just RDAP data
rdapCriteriaList = ["ASN","ASN Routing Block","ASN Country Code","ASN Date",
                    "ASN Registry","ASN Description","Start Address","End Address",
                    "Handle","Parent Handle","IP Version","Name"]

initialize()

##code to run guizero gui
# basic initializations and instructions
app = App(title="Filter Tool")
instructionText = Text(app, text = "Instructions: Select a criteria to filter by, then \nenter a value that you want the IP addresses\n to be filtered by. Or put in a list index and press \none of the 'show' buttons to display data", size = 10)
# initializing GeoIP and RDAP lookup data windows and buttons to open them
ipIndexTextBox = TextBox(app)
geoDataButton = PushButton(app, text = "Show GeoIP Data", command = handleGeoButton)
geoWindow = Window(app, title = "GeoIP Lookup Data")
geoWindow.hide()
geoWText = Text(geoWindow, text = "", size = 10)
rdapDataButton = PushButton(app, text = "Show RDAP Data", command = handleRDAPButton)
rdapWindow = Window(app, title = "RDAP Lookup Data")
rdapWindow.hide()
rdapWText = Text(rdapWindow, text = "", size = 10)
# initializing filter tool buttons and text fields
criteriaText = Text(app, text = "Filter by Criteria:")
criteriaOptions = Combo(app, options=criteriaList)
valueText = Text(app, text = "Filter by Value:")
valueTextBox = TextBox(app, width = 40)
filterButton = PushButton(app, command = handleFilterButton, text = "Filter")
resultText = Text(app, size = 8)
app.display()   
    
##test for one IP Object
#fileToSearch = 'list_of_ips.txt'
#ip_addresses = findIPAddresses(fileToSearch)
#a = (geoIP_lookup(ip_addresses[567]))
#RDAP_lookup(ip_addresses[567], a)
#tempGeoData = a.printGeoIPData()
#tempRDAPData = a.printRDAPData()
#print(tempGeoData)
#print(tempRDAPData)

##filter test without using app
#filteredList = filterBy("IP Type", "Residential")
#print(filteredList)
#for i in range(len(filteredList)):
#    printGeoData(filteredList[i])

  

 
