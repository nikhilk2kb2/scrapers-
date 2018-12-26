# -*- coding: utf-8 -*-
import os
# import requestium
import time
import csv
import xlwt
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

baseUrl = 'https://www.vapornation.com/vaporizers.html'
driver = webdriver.Firefox()
book = xlwt.Workbook(encoding="utf-8")
sheet1 = book.add_sheet("ProductsImageLinks")
sheet1.write(0, 0, 'Product Name')

driver.get(baseUrl)
links_to_products = []


def get_links_to_products():
    driver.implicitly_wait(5)
    links_elements = driver.find_elements_by_class_name('product-image')
    for e in links_elements:
        links_to_products.append(e.get_attribute('href'))

    try:
        # driver.implicitly_wait(5)  # for more products
        driver.find_element_by_link_text("Next").click()
        time.sleep(5)

        get_links_to_products()

    except:
        print('not found')
        pass
get_links_to_products()
row = 1

for link in links_to_products:
    col = 0
    driver.get(link)
    time.sleep(5)
    product_name = driver.find_element_by_class_name('product-name').text
    sheet1.write(row, col, product_name)
    col += 1

    div_of_images = driver.find_element_by_tag_name('ol')
    images = div_of_images.find_elements_by_tag_name('li')
    for image in images:
        sheet1.write(0, col, 'Link To Image')
        sheet1.write(row, col, image.find_element_by_tag_name('a').get_attribute('href'))
        col+=1

    row += 1
output_file = 'Products Scrapped Data at ' + str(time.strftime("%m-%d-%YT%H-%M-%S")) + '.xls'
book.save(output_file)




