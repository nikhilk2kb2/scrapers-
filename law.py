# -*- coding: utf-8 -*-
import os
import time
import csv
import xlwt
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

baseUrl = 'https://www.naela.org/findlawyer'
driver = webdriver.Chrome()
dr=driver

book = xlwt.Workbook(encoding="utf-8")
sheet1 = book.add_sheet("Results")
sheet1.write(0, 0, 'ZIP')
sheet1.write(0, 1, 'First Name')
sheet1.write(0, 2, 'Last Name')
sheet1.write(0, 3, 'Email')
sheet1.write(0, 4, 'Phone')
sheet1.write(0, 5, 'Address')

# Function to get the zipcodes
def get_zipcode():
    zipcodes = []
    with open('us_postal_codes.csv', 'r') as csvFile:
        reader = csv.reader(csvFile)
        for row in reader:
            zipcodes.append(row[0])
    return zipcodes

#Open Url
driver.get(baseUrl)
time.sleep(5)
zipList = get_zipcode()
index = 1

# Iterating over zip codes list
for zipcode in zipList[:1]:
    time.sleep(5)
    print("zip code to search : ",zipcode)
    dr.find_element_by_id('ctl01_TemplateBody_WebPartManager1_gwpste_container_iPart_ciiPart_txtCityStateZip').click()
    dr.find_element_by_id('ctl01_TemplateBody_WebPartManager1_gwpste_container_iPart_ciiPart_txtCityStateZip').clear()
    dr.find_element_by_id('ctl01_TemplateBody_WebPartManager1_gwpste_container_iPart_ciiPart_txtCityStateZip').send_keys(zipcode)
    dr.find_element_by_class_name('SearchButton').click()
    time.sleep(3)

    total_pages = int(dr.find_element_by_id('ctl01_TemplateBody_WebPartManager1_gwpste_container_iPart_ciiPart_ListView1_dpOne_ctl00_Label3').text)
    pages_to_scroll = int(total_pages / 12) + 1

    print("pages_to_scroll : ", pages_to_scroll)
    dr.find_element_by_class_name('PageArrow').click()

    for page in range(0,pages_to_scroll):
        print("page number : ",page)
        time.sleep(5)

        for div in dr.find_elements_by_class_name('SeventyFiveRow'):
            print("************** div text ************",)
            email=""
            phone=""
            fullname=""
            address=""
            try:
                emailbtn = div.find_element_by_class_name('EmailLink')
                email = emailbtn.get_attribute('href').split('mailto:')[1].split('?')[0]
            except Exception as e:
                print("exception in finding email : ",e)
                pass
            try:
                phone = div.find_element_by_class_name('PhoneLink').text
            except Exception as e:
                print("Exception in finding Phone : ",e)
                pass
            try:
                fullname = div.find_elements_by_tag_name('a')[0].text.split(',')[0]
            except Exception as e:
                print("exception in finding Name  : ",e)
                pass
            try:
                address= div.find_element_by_class_name('LocRight').text.split('\n')[0]
            except Exception as e:
                print("exception in finding Address: ",e)
                pass
            fname = fullname.split()[0]
            lname = " ".join(fullname.split()[1:])
            print("First Name : ",fname)
            print("Last  Name : ",lname)
            print("Email      : ", email)
            print("Phone      : ", phone)
            print("Address    : ",address)

            print("*********** Writing to Sheet **************")

            try:
                sheet1.write(index, 0, zipcode)
                sheet1.write(index, 1, fname)
                sheet1.write(index, 2, lname)
                sheet1.write(index, 3, email)
                sheet1.write(index, 4, phone)
                sheet1.write(index, 5, address)
                index = index + 1
                print ("new Index is - " , index)
            except Exception as e:
                print ('Exception in writing output to excel : ',e)
                pass

        pgarrow = dr.find_elements_by_class_name('PageArrow')[1].click()

output_file = 'Lawyers Scrapped Data at '+str(time.strftime("%m-%d-%YT%H-%M-%S"))+'.xls'
book.save(output_file)
print( "Search Results Saved To File - ", output_file)

# filename.close()
