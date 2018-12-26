#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 29 01:15:20 2018

@author: vicky
"""


from selenium import webdriver

from selenium.webdriver.common.proxy import Proxy, ProxyType

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
import csv
import time

prox = Proxy()
prox.proxy_type = ProxyType.MANUAL
prox.http_proxy = "ip_addr:port"
prox.socks_proxy = "ip_addr:port"
prox.ssl_proxy = "ip_addr:port"

capabilities = webdriver.DesiredCapabilities.CHROME
prox.add_to_capabilities(capabilities)

chrome_options = webdriver.ChromeOptions()
prefs = {"profile.default_content_setting_values.notifications" : 2}
chrome_options.add_experimental_option("prefs",prefs)
browser = webdriver.Chrome(desired_capabilities=capabilities,chrome_options=chrome_options)

#London : https://www.yelp.com/search?find_desc=&find_loc=London%2C+United+Kingdom&ns=1
#Leeds : https://www.yelp.com/search?find_desc=&find_loc=Leeds%2C+West+Yorkshire%2C+United+Kingdom&ns=1
#Manchester : https://www.yelp.com/search?find_desc=&find_loc=Manchester%2C+United+Kingdom&ns=1
#Edinburgh : https://www.yelp.com/search?find_desc=&find_loc=Edinburgh%2C+United+Kingdom&ns=1
#Bristol : https://www.yelp.com/search?find_desc=&find_loc=Bristol%2C+United+Kingdom&ns=1
#New York : https://www.yelp.com/search?find_desc=&find_loc=New+York%2C+NY&ns=1
#Los Angeles : https://www.yelp.com/search?find_desc=&find_loc=Los+Angeles%2C+CA&ns=1
#Chicago : https://www.yelp.com/search?find_desc=&find_loc=Chicago%2C+IL&ns=1
#Houston : https://www.yelp.com/search?find_desc=&find_loc=Houston%2C+TX&ns=1
#Pheonix : https://www.yelp.com/search?find_desc=&find_loc=Phoenix%2C+AZ&ns=1

#browser.get("https://www.google.com")

with open('yelp_data_London.csv','a') as new_file:
        csv_writer = csv.writer(new_file)
        csv_writer.writerow(['Title','Category','Yelp URL','Business URL','Address including Zip code','Wi-fi','Parking','Takes Reservation','Delivery','Take-out'])
        
        url='https://www.yelp.com/search?find_desc=&find_loc=London%2C+United+Kingdom&ns=1'
        browser.get(url)
        page_element = browser.find_element_by_xpath('.//*[@class="pagination-block"]/div/div[1]').text
        total_pages = int(page_element[page_element.rfind(' ')+1:])
        print ('Total_Pages :',total_pages)   
        
#        file_obj_page  = open('till_page.txt','r+')
#        current_page = int(file_obj_page.readline())+1
#        file_obj_start  = open('till_start.txt','r+')
#        start = int(file_obj_start.readline())
#        if current_page == 1:
#            csv_writer.writerow(['Title','Category','Yelp URL','Business URL','Address including Zip code','Wi-fi','Parking','Takes Reservation','Delivery','Take-out'])            
        start=0
        current_page=1
        while(current_page<=total_pages):
            print("Current Page : ",current_page)
            pagination_url = 'https://www.yelp.com/search?find_loc=London,+United+Kingdom&start='+str(start)
            browser.get(pagination_url)
            
            biz_element = browser.find_elements_by_xpath("//*[@class='biz-name js-analytics-click']")
            total_biz = len(biz_element)
            start_urls=[]
            for i in range(0,total_biz):
                link = str(biz_element[i].get_attribute('href'))
                start_urls.append(link)
            print(start_urls)
            for link in start_urls:
                print (link)
                browser.get(link)
                yelp_url = link
                title = browser.find_element_by_xpath('.//*[@class="top-shelf"]//h1').text
                print("Title : ",title)
                category_element = browser.find_elements_by_xpath('.//*[@class="category-str-list"]//a	')
                category = ""
                for x in range(0,(len(category_element)//2)+1):
                    category = category + str(category_element[x].text)
                    if x !=(len(category_element)//2):
                        category = category + ", "
                
                print("Category : ",category)
                business_url_element = browser.find_elements_by_xpath('//*[@id="wrap"]/div[2]/div/div[1]/div/div[4]/div[1]/div/div[2]/ul/li[4]/span[2]/a')
                if len(business_url_element)!=0:
                    business_url = business_url_element[0].text
                else:
                    business_url_element = browser.find_elements_by_xpath('//*[@id="wrap"]/div[2]/div/div[1]/div/div[4]/div[1]/div/div[2]/ul/li[5]/span[2]/a')
                    if len(business_url_element)!=0:
                        business_url = business_url_element[0].text
                    else:
                        business_url_element = browser.find_elements_by_xpath('.//*[@class="biz-website js-biz-website js-add-url-tagging"]')
                        if len(business_url_element)!=0:
                            business_url = business_url_element[0].text
                        else:
                            business_url = "NA"
                print("URL : ",business_url)
                address = browser.find_element_by_xpath('.//*[@class="street-address"]//address').text
                print("Address : ",address)
                more_business_info_element = browser.find_elements_by_xpath('.//*[@class="ywidget"]')
                if len(more_business_info_element)!=0:
                    
                    business_info = str(more_business_info_element[0].text)
                    business_info=business_info.replace("\n",",")
                    business_info=business_info.replace(" ","_")
                    business_info = business_info[business_info.find(",")+1:]
                    print(business_info)
                    k=len(business_info)
                    
                    index = business_info.find("Takes_Reservations")
                    if index == -1:
                        takes_reservation = "NA"
                    else:
                        takes_reservation = ""
                        index+=19
                        if index<k:
                            while(True):
                                if business_info[index]!="," and index<k:
                                    takes_reservation=takes_reservation+business_info[index]
                                else:
                                    break
                                index+=1
                    
                    index = business_info.find("Delivery")
                    if index == -1:
                        delivery = "NA"
                    else:
                        delivery = ""
                        index+=9
                        if index<k:
                            while(True):
                                if business_info[index]!="," and index<k:
                                    delivery=delivery+business_info[index]
                                else:
                                    break
                                index+=1
                        
                    index = business_info.find("Take-out")
                    if index == -1:
                        take_out = "NA"
                    else:
                        take_out = ""
                        index+=9
                        if index<k:
                            while(True):
                                if business_info[index]!="," and index<k:
                                    take_out=take_out+business_info[index]
                                else:
                                    break
                                index+=1
                        
                    index = business_info.find("Parking")
                    if index == -1:
                        parking= "NA"
                    else:
                        parking = ""
                        index+=8
                        if index<k:
                            while(True):                
                                if business_info[index]!="," and index<k:
                                    parking=parking+business_info[index]
                                else:
                                    break
                                index+=1
                        
                    index = business_info.find("Wi-Fi")
                    if index == -1:
                        wifi = "NA"
                    else:
                        wifi = ""
                        index+=6
                        if index<k:
                            while(True):
                                if business_info[index]!="," and index<k:
                                    wifi=wifi+business_info[index]
                                else:
                                    break
                                index+=1
                                
                else:
                    takes_reservation = "NA"
                    wifi = "NA"
                    parking= "NA"
                    take_out = "NA"
                    delivery = "NA"
                
                print(takes_reservation,wifi,parking,take_out,delivery)       
                #csv_writer.writerow(['Title','Category','Business URL','Address','Wi-fi','Parking','Takes Reservation','Delivery','Take-out'])
                csv_writer.writerow([title,category,yelp_url,business_url,address,wifi,parking,takes_reservation,delivery,take_out])
                #print(title,category,business_url,address,more_business_info)
        
#            file_obj_page.seek(0)
#            file_obj_page.truncate()
#            file_obj_page.write(str(current_page))
            current_page += 1
            start += 10
#            file_obj_start.seek(0)
#            file_obj_start.truncate()
#            file_obj_start.write(str(start))

browser.close()










