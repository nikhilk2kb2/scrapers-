#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  8 17:39:30 2018

@author: vicky
"""
'''
********************************************
                   FOR USA
********************************************
'''
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

chrome_options = webdriver.ChromeOptions()
prefs = {"profile.default_content_setting_values.notifications" : 2}
chrome_options.add_experimental_option("prefs",prefs)
browser = webdriver.Chrome(chrome_options=chrome_options)

'''
brand_nav = ['#','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z'] 

url = 'https://www.amazon.com/gp/search/other/ref=sr_sa_p_89?rh=n%3A7141123011%2Cn%3A7147440011%2Cn%3A1040660%2Cn%3A1045024%2Cp_n_feature_eighteen_browse-bin%3A14630392011&bbn=1045024&pickerToList=lbr_brands_browse-bin&ie=UTF8&qid=1528299363'
total_brands = 0
browser.get(url)
with open('Brand_name_and_link_US.csv','a') as new_file:
            csv_writer = csv.writer(new_file)
            csv_writer.writerow(['Brand Name','Brand URL'])
            i = 1   
            j = 1
            while(True):
                element = browser.find_elements_by_xpath('//*[@id="ref_2528832011"]/ul['+str(i)+']/li['+str(j)+']/span/a')
                if len(element)!=0:
                    while(len(element)!=0):                   
                        #//*[@id="ref_2528832011"]/ul[1]/li[1]/span/a
                        name_element = browser.find_element_by_xpath('//*[@id="ref_2528832011"]/ul['+str(i)+']/li['+str(j)+']/span/a').text
                        brand_name = name_element[:name_element.find('(')]
                        link = browser.find_element_by_xpath('//*[@id="ref_2528832011"]/ul['+str(i)+']/li['+str(j)+']/span/a').get_attribute('href')
                        csv_writer.writerow([brand_name,link])  
                        total_brands += 1
                        j += 1
                        element = browser.find_elements_by_xpath('//*[@id="ref_2528832011"]/ul['+str(i)+']/li['+str(j)+']/span/a')              
                else:
                    if j==1:
                        break
                    else:
                        i += 1
                        j = 1

            for index in brand_nav:
                #filename = index
                #.//*[text()="#"]
                element = browser.find_elements_by_xpath('.//*[text()="'+index+'"]')
                element[0].click()
                i = 1   
                j = 1
                while(True):
                    element = browser.find_elements_by_xpath('//*[@id="ref_2528832011"]/ul['+str(i)+']/li['+str(j)+']/span/a')
                    if len(element)!=0:
                        while(len(element)!=0):                   
                            #//*[@id="ref_2528832011"]/ul[1]/li[1]/span/a
                            name_element = browser.find_element_by_xpath('//*[@id="ref_2528832011"]/ul['+str(i)+']/li['+str(j)+']/span/a').text
                            brand_name = name_element[:name_element.find('(')]
                            link = browser.find_element_by_xpath('//*[@id="ref_2528832011"]/ul['+str(i)+']/li['+str(j)+']/span/a').get_attribute('href')
                            csv_writer.writerow([brand_name,link]) 
                            total_brands += 1
                            j += 1
                            element = browser.find_elements_by_xpath('//*[@id="ref_2528832011"]/ul['+str(i)+']/li['+str(j)+']/span/a')              
                    else:
                        if j==1:
                            break
                        else:
                            i += 1
                            j = 1
            
print (total_brands)
browser.close()               
'''
#Brand_name_and_link_US.csv
with open('Brand_name_and_link_US.csv','r') as csv_file:
    csv_reader = csv.reader(csv_file)
    #for i in range(0,47):
    #    next(csv_reader)
    next(csv_reader)
    with open('amazon_brands_clothing_data_updated.csv','a') as new_file:
            csv_writer = csv.writer(new_file)
            csv_writer.writerow(['Brand Name','Brand Logo(Link)','Gender','Country','Clothing Types','00','0','1-2','3-4','5-6','7-8','9-10','11-12','13-14','16','18','XXS','XS','S','M','L','XL','XXL','00P','0P','2P','4P','6P','8P','10P','12P','14P','16P','18P','14','16','18','20','22','24','26','28','30','32','34','36','38','0X','1X','2X','3X','4X','5X','6X','7X','8X','Metric'])    
                
            index = 1
            for line in csv_reader:
                
                print(index,line[0],line[1])
                brand_name = line[0]    
                url = line[1]
                browser.get(url)
                
                try:
                    #.//*[@id="leftNav"]/div[2]/ul[2]/ul/li/span/h4/a	
                    gender = browser.find_element_by_xpath('.//*[@id="leftNav"]/div[2]/ul[2]/ul/li/span/h4/a').text
                    print(gender)
                    product_link = browser.find_element_by_xpath('.//*[@id="result_0"]/div/div[1]/div/span/div/div[1]/a/img[1]')	    
                    product_link.click()
                    logo_element = browser.find_elements_by_xpath('.//*[@id="brand"]//img')
                    if len(logo_element)!=0:
                        brand_logo_link = browser.find_element_by_xpath('.//*[@id="brand"]//img').get_attribute('src')
                        browser.get(brand_logo_link)
                    else:
                        brand_logo_link = "-"
                    print(brand_logo_link)
                except:
                    pass
                
                browser.get(url)
                clothing_element = browser.find_element_by_xpath('//*[@id="leftNavContainer"]/ul[2]/ul/li/span/ul/div/li[2]/span/h4/a')
                clothing_element.click()
                type_element = browser.find_element_by_xpath('//*[@id="leftNavContainer"]/ul[2]/ul/li/span/ul/div/li[2]/span/ul/div').text
                cl_type = type_element.replace("\n", "*").strip()       
                result=""    
                clothing_types_array = []
                for i in range(0,len(cl_type)):
                    if cl_type[i]=='*':
                        clothing_types_array.append(result)
                        result=""
                    else:
                        result=result+cl_type[i]
                clothing_types_array.append(result)
                for cltype in clothing_types_array:
                    print(cltype)
                clothing_types_link = []
                k = 2    
                for i in range(0,len(clothing_types_array)):
                    # //*[@id="leftNavContainer"]/ul[2]/ul/li/span/ul/div/li[2]/span/ul/div/li[2]/span/a        
                    link = browser.find_element_by_xpath('//*[@id="leftNavContainer"]/ul[2]/ul/li/span/ul/div/li[2]/span/ul/div/li['+str(k)+']/span/a').get_attribute('href')
                    clothing_types_link.append(link)        
                    k += 2
                print(clothing_types_link)
                print(len(clothing_types_link))
                
                flag = 0
                for k in range(0,len(clothing_types_array)):
                    browser.get(clothing_types_link[k])
                    
                    product_link = browser.find_element_by_xpath('.//*[@id="result_0"]/div/div[1]/div/span/div/div[1]/a/img[1]')	    
                    product_link.click()
                    
                    size_chart_element = browser.find_element_by_xpath('.//*[@id="size-chart-url"]')
                    size_chart_element.click()
                    #.//*[@id="size-chart-table-1"]/tbody/tr[1]/th[3]/span		
                    time.sleep(2)                    
                    metric_element = browser.find_element_by_xpath('.//*[@id="size-chart-table-1"]/tbody/tr[1]/th[3]/span').text
                    
                    close_element = browser.find_elements_by_xpath('.//*[@data-action="a-popover-close"]')
                    close_element[0].click()
                    
                    print(metric)
                    browser.get(clothing_types_link[k])
                            
                    #Show Regular Sizes
                    #Show Petite Sizes
                    #Show Plus Sizes
                    
                    element = browser.find_elements_by_xpath('.//*[text()="Show Regular Sizes"]')
                    if len(element)!=0:
                        element[0].click()
                    element = browser.find_elements_by_xpath('.//*[text()="Show Petite Sizes"]')
                    if len(element)!=0:
                        element[0].click()
                    element = browser.find_elements_by_xpath('.//*[text()="Show Plus Sizes"]')
                    if len(element)!=0:
                        element[0].click()
                        
                    size_element = browser.find_elements_by_xpath("//*[contains(@class,'a-button a-button-toggle togglebutton-group')]")    
                    print(len(size_element))        
                    size_chart = []        
                    if len(size_element)!=0:
                        for i in range(0,len(size_element)):
                            size_chart.append(str(size_element[i].text))             
                    print(size_chart) 
                    result = []
                    if flag==0:
                        flag=1
                        result.append(brand_name)
                        result.append(brand_logo_link)
                        result.append(gender)
                        result.append("USA")
                    else:
                        result.append("")
                        result.append("")
                        result.append("")
                        result.append("")
                    result.append(clothing_types_array[k])
                    
                    general_size_chart = ['00','0','1-2','3-4','5-6','7-8','9-10','11-12','13-14','16','18','XXS','XS','S','M','L','XL','XXL','00P','0P','2P','4P','6P','8P','10P','12P','14P','16P','18P','14','16','18','20','22','24','26','28','30','32','34','36','38','0X','1X','2X','3X','4X','5X','6X','7X','8X']
                    j=0 
                    i=0
                    while(i<51 and j<len(size_chart)):
                        if general_size_chart[i]==size_chart[j]:
                            result.append("Yes")
                            j += 1
                        else:
                            result.append("-")     
                        i += 1
                    result.append(metric)
                    csv_writer.writerow(result)
                index += 1

browser.close()


'''
# for all types of clothing //*[@id="leftNavContainer"]/ul[2]/ul/li/span/ul/div/li[2]/span/ul/div/li
# for size chart  //*[contains(@class,'a-button a-button-toggle togglebutton-group')]

SIZE
Regular
00 0 1-2 3-4 5-6 7-8 9-10 11-12 13-14 16 18
Women's General Size
XXS XS S M L XL XXL
Petite
00P 0P 2P 4P 6P 8P 10P 12P 14P 16P 18P 
Plus
14 16 18 20 22 24 26 28 30 32 34 36 38
Plus General Size
0X 1X 2X 3X 4X 5X 6X 7X 8X

for CANADA
https://www.amazon.ca/gp/search/other/ref=sr_sa_p_89?rh=n%3A8604903011%2Cn%3A%218604904011%2Cn%3A10287217011%2Cp_n_feature_twenty-one_browse-bin%3A17324655011&bbn=10287217011&pickerToList=lbr_brands_browse-bin&ie=UTF8&qid=1528700001

for US
https://www.amazon.com/gp/search/other/ref=sr_in_-2_1?rh=i%3Afashion-womens-clothing%2Cn%3A7141123011%2Cn%3A7147440011%2Cn%3A1040660%2Cn%3A1045024%2Cp_n_feature_eighteen_browse-bin%3A14630392011&bbn=1045024&pickerToList=lbr_brands_browse-bin&ie=UTF8&qid=1528687597

for INDIA
https://www.amazon.in/gp/search/other/ref=sr_sa_p_89?rh=n%3A1571271031%2Ck%3Awomen&bbn=1571271031&keywords=women&pickerToList=lbr_brands_browse-bin&ie=UTF8&qid=1528698006

for metric
 --- >>   .//*[@class="a-size-mini a-text-normal"]	
 
 for gender
 --->> .//*[@id="wayfinding-breadcrumbs_feature_div"]/ul/li[5]/span/a	
'''