# -*- coding: utf-8 -*-
import os
import time
import csv
import xlwt
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

class LawyerScrapper:

    def __init__(self):
        self.baseUrl = 'https://www.naela.org/findlawyer'
        self.driver = webdriver.Chrome('/home/hp/Downloads/chromedriver')
        self.sheet1 = self.load_workbook()
        self.index1 = 1
        self.start_scrapper()

    def load_workbook(self):
        self.book = xlwt.Workbook(encoding="utf-8")
        book = self.book
        sheet1 = book.add_sheet("Results")

        sheet1.write(0, 0, 'ZIP') 
        sheet1.write(0, 1, 'First Name')
        sheet1.write(0, 2, 'Last Name')
        sheet1.write(0, 3, 'Email')
        sheet1.write(0, 4, 'Phone')
        sheet1.write(0, 5, 'Address')

        return sheet1
        # sheet1.write(0, 5, 'Phone')
        # sheet1.write(0, 6, 'Url')

    def get_zipcode(self):
        zipcodes = []
        with open('us_postal_codes.csv', 'r') as csvFile:
            reader = csv.reader(csvFile)
            for row in reader:
                zipcodes.append(row[0])
        return zipcodes

    def get_page_info(self, zipcode):
        dr = self.driver
        self.index2 = self.index1
        for index, lawyer in enumerate(range(0, 12)):
            print "Getting info for Page - ", lawyer+1
            try:
                page_lawyers = dr.find_elements_by_xpath("//div[@class='H4']")[lawyer]
            except:
                return
            time.sleep(1)
            try:
                lawyer_link = page_lawyers.find_element_by_tag_name('a').click()
            except:
                return
            email = fname = lname = phone = address = ''
            try:
                emailbtn = dr.find_element_by_class_name('EmailLink')
                email = emailbtn.get_attribute('href').split('mailto:')[1].split('?')[0]
            except:
                pass
            
            try:
                phone = dr.find_element_by_class_name('PhoneLink').text
            except:
                pass

            try:
                fullname = dr.find_element_by_class_name('DetailName').text
            except:
                pass
                
            fname , lname = fullname.split(' ')[0],fullname.split(' ')[1]

            try:
                try:
                    address= dr.find_element_by_id('ctl01_TemplateBody_WebPartManager1_gwpste_container_iPart_ciiPart_lblDetailContact').text
                except:
                    address= dr.find_element_by_id('ctl01_TemplateBody_WebPartManager1_gwpste_container_iPart_ciiPart_ListView1_ctrl0_ctl00_lbNamePost').text                    
                address = address.split('Phone')[0]
            
            except NoSuchElementException as e:
                return


            print fname, lname
            print email, phone, address

            sheet1 = self.sheet1

            try:
                sheet1.write(self.index2, 0, zipcode) 
                sheet1.write(self.index2, 1, fname) 
                sheet1.write(self.index2, 2, lname)
                sheet1.write(self.index2, 3, email)
                sheet1.write(self.index2, 4, phone)
                sheet1.write(self.index2, 5, address)
                print self.index2
            except:
                print 'Error occured!!!'

            self.index2 = self.index2 + 1

            dr.execute_script("window.history.go(-1)")

        self.index1 = self.index2+1
        print self.index1


          
    def try_paginate(self, zipcode):
        time.sleep(2)

        try:
            self.driver.find_elements_by_class_name('PageArrow')[1].click()
            time.sleep(2)
        except:
            return
        self.get_page_info(zipcode)
        self.try_paginate(zipcode)


    def save_workbook(self):
        output_file = 'Lawyers Scrapped Data at '+str(time.strftime("%m-%d-%Y_%H-%M-%s-%p"))+'.xls'
        self.book.save(output_file) 
        print "Search Results Saved To File - ", output_file 


    def start_scrapper(self):
        zipList = self.get_zipcode()[0]
        dr = self.driver
        dr.get(self.baseUrl)
        for zipcode in zipList:
            zipcode = self.get_zipcode()[0]
            # import pdb;pdb.set_trace()
            zipInputbox = dr.find_element_by_class_name('LocationBox').send_keys(zipcode)
            searchBtn = dr.find_element_by_class_name('SearchButton').click()
            time.sleep(1)
            self.get_page_info(zipcode)
            self.try_paginate(zipcode)
            zipInputbox = dr.find_element_by_class_name('LocationBox').clear()

        
if __name__ == '__main__':
    LawyerScrapper()