import math
import os
import time
import csv
import xlwt
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.options import Options
from selenium.webdriver import Firefox, FirefoxProfile
# options = Options()
# options.add_argument("--headless")

baseUrl = 'https://trade.4over.com/'
firefoxProfile = FirefoxProfile()
firefoxProfile.set_preference("plugin.state.flash", 2)
# driver = webdriver.Firefox(firefox_options=options)
driver = Firefox(firefoxProfile)
book = xlwt.Workbook(encoding="utf-8")
sheet1 = book.add_sheet("Results")
dr=driver

sheet1.write(0, 0, 'Buisness Card')
sheet1.write(0, 1,'Stock')
sheet1.write(0, 2,'Dimension')
sheet1.write(0, 3,'Coating')
sheet1.write(0, 4,'Rounded Corner')
sheet1.write(0, 5, 'Run Size')
sheet1.write(0, 6, 'Colour')
sheet1.write(0, 7, 'Delivery Time')
sheet1.write(0, 8, 'Total PRICE(in $)')

driver.get(baseUrl)
time.sleep(2)
login_name="4over@lordandfalconer.com"
password="fiverr01"

#######
driver.find_element_by_id("topLogin").clear()
driver.find_element_by_id("topLogin").send_keys(login_name)
driver.find_element_by_id("topPassword").clear()
driver.find_element_by_id("topPassword").send_keys(password)
driver.find_element_by_class_name("button").click()
time.sleep(5)
###########

index=1
#####
driver.find_element_by_xpath('//a[@href="https://trade.4over.com/products/business-cards/"]').click()
#####

#####
def cards_not_exist():
    sty=driver.find_element_by_id('browse_error').get_attribute('style')
    if "display: none" in sty:
        return False
    else:
        return True
#####
def main_function():
    global index
    stocks=driver.find_elements_by_css_selector("#stock option")
    stocks=list(map(lambda x:x.text,stocks))
    for diff_stock in stocks[1:]:
        diff_stock_xpath="//select[@id='stock']/option[text()=\'" + diff_stock + "\']"
        driver.find_element_by_xpath(diff_stock_xpath).click()
        time.sleep(4)

        if cards_not_exist():
            continue

        dimensions=driver.find_elements_by_css_selector("#dimensions option")
        dimensions=list(map(lambda x:x.get_attribute('value'),dimensions))
        for diff_dimension in dimensions[1:]:
            diff_dimension_xpath="//select[@id='dimensions']/option[@value=\'" + diff_dimension + "\']"
            driver.find_element_by_xpath(diff_dimension_xpath).click()
            time.sleep(4)
            
            if cards_not_exist():
                continue

            coatings=driver.find_elements_by_css_selector("#coating option")
            coatings=list(map(lambda x:x.text,coatings))
            for diff_coating in coatings[1:]:
                diff_coating_xpath="//select[@id='coating']/option[text()=\'" + diff_coating + "\']"
                driver.find_element_by_xpath(diff_coating_xpath).click()
                time.sleep(4)
                
                if cards_not_exist():
                    continue

                corners=driver.find_elements_by_css_selector("#roundcorners option")
                corners=list(map(lambda x:x.text,corners))
                for diff_corner in corners[1:]:
                    diff_corner_xpath="//select[@id='roundcorners']/option[text()=\'" + diff_corner + "\']"
                    driver.find_element_by_xpath(diff_corner_xpath).click()
                    time.sleep(5)
                    if cards_not_exist():
                        continue
                    buisnessCardLinks=getting_buisness_card_links()
                    scrappingBuisnessCard(buisnessCardLinks,diff_stock,diff_dimension,diff_coating,diff_corner)
                    time.sleep(5)
                    driver.find_element_by_xpath('//a[@href="https://trade.4over.com/products/business-cards/"]').click()
                    time.sleep(5)
                    driver.find_element_by_xpath(diff_stock_xpath).click()
                    time.sleep(5)
                    driver.find_element_by_xpath(diff_dimension_xpath).click()
                    # print(diff_dimension_xpath)
                    time.sleep(5)
                    driver.find_element_by_xpath(diff_dimension_xpath).click()
                    time.sleep(5)
                    driver.find_element_by_xpath(diff_coating_xpath).click()
                    time.sleep(5)

                    # if index==201:
                    #     return
                driver.find_element_by_xpath("//select[@id='roundcorners']/option[text()='All']").click()
                time.sleep(4)

            driver.find_element_by_xpath("//select[@id='coating']/option[text()='All']").click()
            time.sleep(4)

        driver.find_element_by_xpath("//select[@id='dimensions']/option[text()='All']").click()
        time.sleep(4)



#####

def getting_buisness_card_links():
    buisnessCardLinks=[]
    for i in range(1,12):
        try:
            temp=driver.find_element_by_css_selector("#container_"+str(i))
            sty=temp.get_attribute('style')
            if "display: none" not in sty:
                buisnessCardLinks+=temp.find_elements_by_css_selector('a')
        except:
            pass
    y=[]
    for buisnessCardTag in buisnessCardLinks:
            x=buisnessCardTag.find_element_by_xpath('..')
            x=x.find_element_by_xpath('..')
            if "display: none" not in x.get_attribute('style'):
                y.append(buisnessCardTag.get_attribute('href'))
    print(y,len(y))
    return y


#####
####
def scrappingBuisnessCard(buisnessCardLinks,diff_stock,diff_dimension,diff_coating,diff_corner):
    global index
    for buisnessCard in buisnessCardLinks:
        driver.get(buisnessCard)
        time.sleep(5)
        cardType=driver.find_element_by_class_name('whatisit').text
        runsizes=driver.find_elements_by_css_selector("#runsize option")[1:]
        runsizes=list(map(lambda x:x.get_attribute("value"),runsizes))
        for diff_runsize in runsizes:
            xpath="//select[@id='runsize']/option[@value=\'" + diff_runsize + "\']"
            driver.find_element_by_xpath(xpath).click()
            time.sleep(4)
            colors=driver.find_elements_by_css_selector("#color option")[1:]
            colors=list(map(lambda x:x.text,colors))
            for diff_color in colors:
                xpath="//select[@id='color']/option[text()=\'" + diff_color + "\']"
                driver.find_element_by_xpath(xpath).click()
                time.sleep(4)
                turn_around_time_options=driver.find_elements_by_css_selector("#tat option")[1:]
                turn_around_time_options=list(map(lambda x:x.text,turn_around_time_options))
                for diff_tat in turn_around_time_options:
                    xpath="//select[@id='tat']/option[text()=\'" + diff_tat + "\']"
                    driver.find_element_by_xpath(xpath).click()
                    time.sleep(7)
                    print("hello")
                    subTotal=driver.find_element_by_id('subby').text
                    ###########
                    print("------------")
                    print("INDEX:",index)
                    print(buisnessCard,"\n",diff_stock,diff_coating,diff_dimension,diff_corner,cardType,"\n",diff_runsize,diff_color,diff_tat,subTotal)
                    print("------------")
                    ###################
                    sheet1.write(index,0,cardType)
                    sheet1.write(index,1,diff_stock.strip())
                    sheet1.write(index,2,diff_dimension.strip())
                    sheet1.write(index,3,diff_coating.strip())
                    sheet1.write(index,4,diff_corner.strip())
                    sheet1.write(index,5,diff_runsize)
                    sheet1.write(index,6,diff_color)
                    sheet1.write(index,7,diff_tat)
                    sheet1.write(index,8,subTotal)
                    index+=1
                    # if index==201:
                    #     return

main_function()
#############
output_file = 'BuisenessCardInfoScrappedAt'+str(time.strftime("%m-%d-%Y_%H-%M-%s-%p"))+'.xls'
book.save(output_file)
print( "Search Results Saved To File - ", output_file )
