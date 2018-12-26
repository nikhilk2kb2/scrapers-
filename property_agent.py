# -*- coding: utf-8 -*-
import os
import time
import xlwt
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
options = Options()
options.add_argument("--headless")
from selenium.webdriver.common.keys import Keys
profile=webdriver.FirefoxProfile()



baseUrl = 'https://www.property24.com'

url= 'https://www.property24.com/for-sale/val-de-vie-estate/paarl/western-cape/11726'


pageList = ['/p'+str(x) for x in range(2, 13)]
pageList.insert(0,'/')

book = xlwt.Workbook(encoding="utf-8")

sheet1 = book.add_sheet("Estates")

sheet1.write(0, 0, 'Agent Name') 
sheet1.write(0, 1, 'Mobile')
sheet1.write(0, 2, 'Phone')


# https_proxy = "https://45.77.192.166:8080"
# proxyDict = {"https" : https_proxy}

index1 = 1
for page in pageList:
    print "Checking Page " , page
    index2 = index1

    pageUrl = url + page
    pageData = requests.get(url)
    soup = BeautifulSoup(pageData.text, 'html.parser')

    foundResults = soup.find_all(class_='js_resultTile')
    # import pdb;pdb.set_trace()
    for result in foundResults:
        print "Checking result " , result

        try:
            resultPageUrl = baseUrl+result.find_all('a')[0]['href']
        except:
            print "Not found!!"
            pass
            
        resultPageData = requests.get(resultPageUrl) #, proxies=proxyDict)
        
        # soup1 = BeautifulSoup(resultPageData.text, 'html.parser')        
        
        dr = webdriver.Firefox(firefox_options=options)
        dr.get(resultPageUrl)
        dr.add_cookie({'name' : 'P24UUEYED=Id', 'value' : 'jref4z0eaexitfnydu03angv'})
        
        import time
        time.sleep(5)
        
        try:
            dr.find_element_by_xpath("//a[@class='js-p24_sidebarContactNumbersLink']").click()
        except:
            import time
            time.sleep(10)
            dr.find_element_by_xpath("//a[@class='js-p24_sidebarContactNumbersLink']").click()

        import time
        time.sleep(5)

        agent_name = mobile = phone = ''

        try:
            agent_name = dr.find_element_by_class_name("p24_agentPhoto").text
        except:
            pass

        try:
            mobile = dr.find_element_by_class_name("js-P24_Mobile").text
        except:
            pass

        try:
            phone = dr.find_element_by_class_name("js-P24_Telephone").text
        except:
            pass

        dr.close()

        try:
            sheet1.write(index2, 0, agent_name) 
            sheet1.write(index2, 1, mobile) 
            sheet1.write(index2, 2, phone)
            print index2, " - Rows Done !! with data -", agent_name, mobile, phone
        except:
            print 'Error occured!!!'
        
        index2 = index2+1

    index1 = index2+1


output_file = 'Agent Data Scrapped Data at '+str(time.strftime("%m-%d-%Y_%H-%M-%s-%p"))+'.xls'
book.save(output_file) 
print "Search Results Saved To File - ", output_file 
