# -*- coding: utf-8 -*-
"""
Created on Tue Jun  5 20:00:11 2018

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

line_index = 1
result_index = 1
with open('locations.csv','r') as csv_file:
    csv_reader = csv.reader(csv_file)
    #next(csv_reader)
    with open('yelp_data.csv','a') as new_file:
        csv_writer = csv.writer(new_file)
        csv_writer.writerow(['Zip Code','Location[City,State]','Website URL'])
        
        for line in csv_reader:
            city = line[0]            
            state = line[1]
            print(line_index,city,state)
            location = city+','+state
            
            #url=https://www.yelp.com/search?find_desc=&find_loc=London%2C+United+Kingdom&ns=1
            url = 'https://www.yelp.com/search?find_desc=&find_loc='+city+'%2C+'+state+'&ns=1'
            browser.get(url)
            page_element = browser.find_element_by_xpath('.//*[@class="pagination-block"]/div/div[1]').text
            #print(page_element)            
            total_pages = int(page_element[page_element.rfind(' ')+1:])
            print ('Total_Pages :',total_pages)        
            start=0
            current_page=1
            address_index = 1
            while(current_page<=total_pages):
                print('Page :',current_page,start)
                # total biz-name .//*[@data-analytics-label="biz-name"]//span	
                biz_element = browser.find_elements_by_xpath('.//*[@data-analytics-label="biz-name"]//span')
                total_biz = len(biz_element)
                for i in range(1,total_biz+1):
                    # biz element //*[@id="super-container"]/div/div[2]/div[1]/div/div[4]/ul[2]/li[1]/div/div[1]/div[1]/div/div[2]/h3/span/a
                    website_url = browser.find_element_by_xpath('//*[@id="super-container"]/div/div[2]/div[1]/div/div[4]/ul[2]/li['+str(i)+']/div/div[1]/div[1]/div/div[2]/h3/span/a').get_attribute('href')
                    # for address .//*[@data-key="10"]//address	
                    address_element = browser.find_elements_by_xpath('.//*[@data-key="'+str(address_index)+'"]//address')
                    if len(address_element)!=0:
                        address = browser.find_element_by_xpath('.//*[@data-key="'+str(address_index)+'"]//address').text
                    else:
                        address = ""
                    #"abcd}def}".rfind('}')
                    zip_code = address[address.rfind(',')+2:]
                    address_index += 1
                    csv_writer.writerow([zip_code,location,website_url])
                    print(result_index,zip_code,location,website_url)
                    result_index += 1
                # for pagination .//*[@class="pagination-links arrange_unit"]/div/div[11]/a/span[2]	
                '''                
                pagination_element = browser.find_elements_by_xpath('.//*[@class="pagination-links arrange_unit"]/div/div[11]/a/span[2]')
                if len(pagination_element)!=0:
                    pagination_element[0].click()
                else:
                    break
                '''
                current_page += 1
                start += 10
                pagination_url = 'https://www.yelp.com/search?find_loc='+city+',+'+state+'&start='+str(start)
                browser.get(pagination_url)
                
            line_index += 1

browser.close()
            
        
    
