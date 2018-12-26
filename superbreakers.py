# -*- coding: utf-8 -*-
import os
import time
import csv
import xlwt
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException

baseUrl = 'https://www.widespreadsales.com/Products/Shunt-Trips'
driver = webdriver.Firefox()
driver.get(baseUrl)
links_to_products_details = []
time.sleep(8)
book = xlwt.Workbook(encoding="utf-8")
sheet1 = book.add_sheet("ProductsDetails")
sheet1.write(0, 0, 'Product Name')
sheet1.write(0, 1, 'Part Number')
sheet1.write(0, 2, 'Manufacturers')
sheet1.write(0, 3, 'Sub-Category')
sheet1.write(0, 4, 'Family')
sheet1.write(0, 5, 'Type')
sheet1.write(0, 6, 'Phase')
sheet1.write(0, 7, 'Poles')
sheet1.write(0, 8, 'Volatge')
sheet1.write(0, 9, 'Amperage')
sheet1.write(0, 10, 'Connection')
sheet1.write(0, 11, 'Protection')
sheet1.write(0, 12, 'Functions')
sheet1.write(0, 13, 'AIC Rating')
sheet1.write(0, 14, 'Description')
sheet1.write(0, 15, 'New Surplus Price')
sheet1.write(0, 16, 'Re-Certified Price')
row=1


def get_links():

    try:
        driver.find_elements_by_xpath("//a[text()='DETAILS']")
    except:
        print("not found")
    for detail in driver.find_elements_by_xpath("//a[text()='DETAILS']"):
        links_to_products_details.append(detail.get_attribute('href'))
    try:                                                                   #for more products
        time.sleep(5)
        driver.find_element_by_link_text("Next Page").click()
        get_links()
    except:
        pass
    return links_to_products_details
links_to_products_details=get_links()
print(len(links_to_products_details))

for link in links_to_products_details:
    driver.implicitly_wait(10)
    driver.get(link)

    productName=driver.find_element_by_class_name('productName').text
    description=driver.find_element_by_class_name('description').text
    print("*********** Writing to Sheet **************")
    col=0
    sheet1.write(row, col, productName)
    col=col+1
    specifications=driver.find_element_by_xpath('//div[@class="specifications"]')
    for tr in specifications.find_elements_by_tag_name('tr'):
        td=tr.find_elements_by_tag_name('td')
        # print(td[1].text)
        sheet1.write(row, col, td[1].text)
        # print(td)
        col+=1
       # print(td[0].text+"::"+ td[1].text)
    sheet1.write(row, col, description)
    col+=1
    price_types=driver.find_elements_by_class_name('PurchaseField')
    price1=""
    price2=""
    if len(price_types)>0:

        for p in price_types:
            price_type=p.find_element_by_class_name('title')
            price_text=price_type.text
            if "New Surplus" in price_text:
                price_value=p.find_element_by_class_name('purchaseAmount').text
                price1=price_value[:-2]
            if "Re-Certified" in price_text:
                price_value = p.find_element_by_class_name('purchaseAmount').text
                price2 = price_value[:-2]
        if len(price1)==0:
            price1="$0"

        if len(price2)==0:
            price2="$0"


    else:
        price1 = "$0"
        price2 = "$0"
    sheet1.write(row, col, price1)
    col += 1
    sheet1.write(row, col, price2)
    row += 1



    # price=driver.find_elements_by_xpath('//span[@class="purchaseAmount"]')


    # print("Description--{}".format(description))

output_file = 'Products Scrapped Data at ' + str(time.strftime("%m-%d-%YT%H-%M-%S")) + '.xls'
book.save(output_file)
print("Search Results Saved To File - ", output_file)

    # soup=BeautifulSoup(driver.page_source,'lxml')
    # productName=soup.find('span',class_='productName').contents[0]
    # description=soup.find('p',class_='description').contents[1]
    # print(productName)
    # print(productName+description)
    # break






