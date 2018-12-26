#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May  5 12:16:45 2018

@author: vicky
"""


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
import time
import csv
import re

chrome_options = webdriver.ChromeOptions()
prefs = {"profile.default_content_setting_values.notifications" : 2}
chrome_options.add_experimental_option("prefs",prefs)
browser = webdriver.Chrome(chrome_options=chrome_options)

phone_number_count=0
    
with open('UK_postal_codes.csv','r') as csv_file:
    csv_reader = csv.reader(csv_file)
    next(csv_reader)
    with open('Auto_Trader_Phone_Number_data.csv','w') as new_file:
        csv_writer = csv.writer(new_file)
        csv_writer.writerow(['Index','Contact_Number','Car_url'])
        
        '''
        
        for line in csv_reader:
            browser.get('https://www.autotrader.co.uk/')
            # for element containing postcode  .//*[@name="postcode"]	
            #post_code_element = browser.find_element_by_xpath('.//*[@name="postcode"]').clear()
            post_code_element = browser.find_element_by_xpath('.//*[@name="postcode"]')
            post_code_element.click()
            post_code = line[0]
            post_code_element.send_keys(post_code)
            # for search button .//*[@name="search-used-vehicles"]	
            search_button =  browser.find_element_by_xpath('.//*[@name="search-used-vehicles"]	')
            search_button.click()
            
            car_hyperlinks_by_post_code = []
            
            # for notification  .//*[text()="Ok, got it"]	
            notification_element = browser.find_elements_by_xpath('.//*[text()="Ok, got it"]')
            if len(notification_element)!=0:
                notification_element[0].click()
            
            while(True):
                # for listing of all the cars    .//*[@class="listing-title title-wrap"]//a	  
                car_list_element = browser.find_elements_by_xpath('.//*[@class="listing-title title-wrap"]//a')
                car_list_length = len(car_list_element)
                for i in range(0,car_list_length):
                    car_hyperlinks_by_post_code.append(str(car_list_element[0].get_attribute('href')))
                # for right pagination    .//*[@class="pagination--right__active"]//i	
                right_pagination = browser.find_elements_by_xpath('.//*[@class="pagination--right__active"]//i')
                if len(right_pagination)!=0:
                    right_pagination[0].click()
                else:
                    break
                
            print (car_hyperlinks_by_post_code)
            
            total_car_links = len(car_hyperlinks_by_post_code)
            for i in range(0,total_car_links):
                browser.get(car_hyperlinks_by_post_code[i])
                # for telephone element  .//*[@class="seller_trade__telephone "]
                contact_number = str(browser.find_element_by_xpath('.//*[@class="seller_trade__telephone "]').text)
                print(contact_number)
            
        '''
            
        for line in csv_reader:
            #maximum phone number extraction limitation
            if(phone_number_count==20000):
                break                
            post_code = str(line[0])
            post_code = post_code.replace(" ","")
            post_code = post_code.lower()
            print(post_code)
            url = 'https://www.autotrader.co.uk/car-search?sort=sponsored&radius=1500&onesearchad=Used&onesearchad=Nearly%20New&onesearchad=New&page=1&postcode='+post_code
            browser.get(url)
            
            '''
            # for notification  .//*[text()="Ok, got it"]	
            notification_element = browser.find_elements_by_xpath('.//*[text()="Ok, got it"]')
            if len(notification_element)!=0:
                notification_element[0].click()
            '''    
            
            total_pages = int(browser.find_element_by_xpath('.//*[@class="paginationMini__count"]//strong[2]').text)
            current_page=1
            car_hyperlinks_by_post_code = []
            
            while current_page<=total_pages:
                page_url = 'https://www.autotrader.co.uk/car-search?sort=sponsored&radius=1500&onesearchad=Used&onesearchad=Nearly%20New&onesearchad=New&page='+str(current_page)+'&postcode='+post_code
                browser.get(page_url)
                
                '''
                # for notification  .//*[text()="Ok, got it"]	
                notification_element = browser.find_elements_by_xpath('.//*[text()="Ok, got it"]')
                if len(notification_element)!=0:
                    notification_element[0].click()
                '''
                
                total_pages = int(browser.find_element_by_xpath('.//*[@class="paginationMini__count"]//strong[2]').text)
                # for listing of all the cars    .//*[@class="listing-title title-wrap"]//a	  
                car_list_element = browser.find_elements_by_xpath('.//*[@class="listing-title title-wrap"]//a')
                car_list_length = len(car_list_element)
                for i in range(0,car_list_length):
                    car_hyperlinks_by_post_code.append(str(car_list_element[i].get_attribute('href')))
                current_page+=1
            
            print (car_hyperlinks_by_post_code)
            
            total_car_links = len(car_hyperlinks_by_post_code)
            for i in range(0,total_car_links):
                browser.get(car_hyperlinks_by_post_code[i])
                # for telephone element  .//*[@class="seller_trade__telephone "]
                contact_number_element = browser.find_elements_by_xpath('.//*[@class="seller_trade__telephone "]')
                for k in range(0,len(contact_number_element)):
                    contact_number = str(contact_number_element[k].text)
                    print(contact_number)
                    number = contact_number
                    number = number.replace(" ","")
                    number = number.replace("(","")
                    number = number.replace(")","")
                    if number[0]=='0' and number[1]=='7':
                        phone_number_count+=1
                        print("Found Result",phone_number_count,contact_number)
                        result = []
                        result.append([phone_number_count,contact_number,car_hyperlinks_by_post_code[i]])
                        csv_writer.writerow(result[0])
                                
browser.close()




