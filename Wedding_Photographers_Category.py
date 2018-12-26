#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 21 22:07:58 2018

@author: vicky
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
import csv
import time
import re
import os


chrome_options = webdriver.ChromeOptions()
prefs = {"profile.default_content_setting_values.notifications" : 2}
chrome_options.add_experimental_option("prefs",prefs)
browser = webdriver.Chrome(chrome_options=chrome_options)

browser.get("https://www.wedmegood.com")
login_element = browser.find_element_by_xpath('.//*[text()="Log In"]')
login_element.click()
username_element = browser.find_element_by_xpath('.//*[@type="text"]')
username_element.send_keys('nikhil.thakur929@gmail.com')
pswd_element = browser.find_element_by_xpath('.//*[@type="password"]')
pswd_element.send_keys('nikhilk2kb2')
signin_element = browser.find_element_by_xpath('.//*[text()="Sign In"]')
signin_element.click()
time.sleep(10)

file_obj  = open('till.txt','r+')
id_index = int(file_obj.readline())

with open('WedMeGood_Wedding_Photographers_Profiles.csv','r') as csv_file:
    csv_reader = csv.reader(csv_file)
    with open('WedMeGood_Wedding_Photographers.csv','a') as new_file:
        csv_writer = csv.writer(new_file)
        
        for i in range(id_index):
            next(csv_reader)
        if id_index==0:
            csv_writer.writerow(['Title','Address','Contact','URL','Rating','Price','Description/About','Images Links'])
        print(id_index)
        for link in csv_reader:
            try:
                url = str(link[0])  
                browser.get(url)
                
                vendor_title = browser.find_element_by_xpath('.//*[@class="vendor-head"]//h1').text
                print(vendor_title)
                
                vendor_address = "Delhi NCR"
                print(vendor_address)
                
                try:
                    vendor_rating = browser.find_element_by_xpath('.//*[@class="fcol align-fe"]//span').text
                except:
                    vendor_rating="-"
                print(vendor_rating)
                
                try:
                    
                    price_element = browser.find_elements_by_xpath('.//*[@class="pointer regular"]//span')
                    price = "Per Day Price Estimate : \n"
                    if len(price_element)!=0:
                        price_element[0].click()
                        time.sleep(2)
                        price += str(browser.find_element_by_xpath('.//*[@class="two-column-view frow"]/div[2]/div[1]/div/div[2]').text)
                        price = price + "\n" + str(browser.find_element_by_xpath('.//*[@class="two-column-view frow"]/div[2]/div[1]/div/div[3]/div').text) + "\n" + str(browser.find_element_by_xpath('.//*[@class="two-column-view frow"]/div[2]/div[1]/div/div[4]/div').text) 
                    else:
                        price = "Per Day Price Estimate : " + "\n" + str(browser.find_element_by_xpath('.//*[@class="two-column-view frow"]/div[2]/div[1]/div/div[3]/div').text) + "\n" + str(browser.find_element_by_xpath('.//*[@class="two-column-view frow"]/div[2]/div[1]/div/div[4]/div').text) 
                    #.//*[@class="two-column-view frow"]/div[2]/div[1]/div/div[2]/div	
                    #price = str(browser.find_element_by_xpath('.//*[@class="two-column-view frow"]/div[2]/div[1]/div/div[2]/div').text)
                    #price = "Starting Price : " + str(browser.find_element_by_xpath('.//*[@class="two-column-view frow"]/div[2]/div[1]/div/div[2]/div').text) + " and " + str(browser.find_element_by_xpath('.//*[@class="two-column-view frow"]/div[2]/div[1]/div/div[3]/div').text)
                    
                except:
                    price="-"
                print(price)
                
                '''
                try:
                    menu_links = []
                    menu_element = browser.find_elements_by_xpath('.//*[@class="menu-image"]')
                    print(len(menu_element))
                    if len(menu_element)!=0:
                        for i in range(0,len(menu_element)):
                            menu_links.append(str(menu_element[i].get_attribute("src")))
                except:
                    menu_links="-"
                print(menu_links)
                '''
                
                try:
                    description_element = browser.find_elements_by_xpath('.//*[@class="info padding-h-20 padding-v-20"]')
                    vendor_description=description_element[0].text.encode('utf-8')
                except:
                    vendor_description="-"
                print(vendor_description)
                
                try:
                    
                    vendor_contact_element = browser.find_elements_by_xpath('.//*[text()="Contact"]')
                    if len(vendor_contact_element)!=0:
                        vendor_contact_element[0].click()
                    time.sleep(2)
                    contact_element = browser.find_elements_by_xpath('.//*[@class="sc-esjQYD dypAdR"]//p')
                    vendor_contact = ""
                    for i in range(0,len(contact_element)):
                        vendor_contact += str(contact_element[i].text) + "\n" 
                except:
                    vendor_contact="-"
                print(vendor_contact)
                
                try:
                    url = url + "/portfolio"
                    browser.get(url)
                    image_element = browser.find_elements_by_xpath('.//*[@class="object-fit-cover"]')
                    image_links = []
                    for i in range(0,len(image_element)):
                        image_links.append(str(image_element[i].get_attribute("src")))               
                except:
                    image_links="-"
                print(image_links)   
                
                csv_writer.writerow([vendor_title,vendor_address,vendor_contact,url,vendor_rating,price,vendor_description,image_links])
                id_index += 1
                print("Row_Count : ",id_index)
                file_obj.seek(0)
                file_obj.truncate()
                file_obj.write(str(id_index))
                
            except:
                print("Error Occurred")

browser.close()

            




