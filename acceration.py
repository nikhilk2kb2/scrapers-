# -*- coding: utf-8 -*-
import os
import time
import csv
import xlwt
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

baseUrl = 'https://www.bbb.org/en/us/search?find_text=bed+bug&page=33&sort=Name&filter_accredited=1'
dr = webdriver.Firefox()
book = xlwt.Workbook(encoding="utf-8")
sheet1 = book.add_sheet("Results")

sheet1.write(0, 0, 'Company') 
sheet1.write(0, 1, 'Location')
sheet1.write(0, 2, 'Web Address')
sheet1.write(0, 3, 'Phone')
sheet1.write(0, 4, 'Accreditation Ranking')
sheet1.write(0, 5, 'State')

# def get_states():
#     states = []
#     with open('states.csv', 'r') as csvFile:
#         reader = csv.reader(csvFile)
#         for row in reader:
#             states.append(row[0].lower())
#     return states

# states = get_states()

urlDict = {}
index = 1

dr.get(baseUrl)

# for state in states:    
    # dr.find_element_by_name('nearTypeaheadInput').clear()
    # print "Searching for %s" % (state)
    # for each_char in state:
    #     dr.find_element_by_name('nearTypeaheadInput').send_keys(each_char)
    #     time.sleep(0.50)
    
    # time.sleep(2)
    
    # try:
    #     suggestions = dr.find_element_by_class_name('react-autosuggest__suggestions-list').find_elements_by_tag_name('li')[1]
    #     suggestions.click()
    #     #click search
    #     dr.find_element_by_class_name('dtm-header-search-submit').click()
    #     dr.find_element_by_name('nearTypeaheadInput').clear()
    # except:
    #     pass

urlList = []

def _fetch_page():    
    results_sections = dr.find_elements_by_class_name('dtm-search-listing')

    for res in results_sections:
        try:
            print res.find_element_by_tag_name('a').text
            time.sleep(1)
            detail_url = res.find_element_by_tag_name('a').get_attribute('href')
        except:
            import pdb;pdb.set_trace()                
        urlList.append(detail_url)

_fetch_page()

def get_page_data():
    try:
        nxt_btn_click = dr.find_element_by_class_name('next').click()
        time.sleep(5)
    except:
        return
    _fetch_page()
    get_page_data()

get_page_data()

for link in urlList:
    dr.get(link)
    company_name = phone = location = website = rating = ''
    try:
        company_name = dr.find_element_by_class_name('masthead__business-name').text
    except:
        time.sleep(1)
        company_name = dr.find_element_by_class_name('masthead__business-name').text

    try:
        phone = dr.find_element_by_class_name('address__phone-number-link').text
    except:
        pass

    try:
        location = dr.find_element_by_tag_name('address').text
    except:
        pass

    try:
        rating = dr.find_element_by_class_name('bbb-rating__rating').text
    except:
        pass

    try:
        website = dr.find_elements_by_class_name('business-buttons__button')[1].get_attribute('href')
    except:
        pass            

    print company_name, phone, location, website, rating
    print '-------------------------------------------------'

    sheet1.write(index, 0, company_name) 
    sheet1.write(index, 1, location) 
    sheet1.write(index, 2, website)
    sheet1.write(index, 3, phone)
    sheet1.write(index, 4, rating)

    index = index + 1

dr.get(baseUrl)
   
output_file = 'BedBugs Data Scrapped Data at '+str(time.strftime("%m-%d-%Y_%H-%M-%s-%p"))+'.xls'
book.save(output_file) 
print "Search Results Saved To File - ", output_file 
