import time
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException

urls_list = []

lid_number = []
titel = []
taal = []
accountant_sinds = []
belastingconsultant_sinds = []
adres = []
telefoon = []
fax = []
email =[]


browser = webdriver.Firefox()

url = 'http://www.iec-iab.be/nl/diensten/zoeken/Pages/Zoeken.aspx?all=true&org=on'
browser.get(url)

#elements = browser.find_elements_by_xpath("//div[@class='results']/ul/li")

soup = BeautifulSoup(browser.page_source,'html.parser')

ul = soup.find("ul", {"class": "nav_grey searchresults"})

for li in ul.findAll('li'):
    urls_list.append('http://www.iec-iab.be'+ li.a['href'])

for link in urls_list:
    browser.get(link)
    time.sleep(1)


    elements = browser.find_elements_by_class_name('right')

    lid_number.append(elements[0].text)
    titel.append(elements[1].text)
    taal.append(elements[2].text)
    accountant_sinds.append(elements[3].text)
    belastingconsultant_sinds.append(elements[4].text)
    adres.append(elements[5].text)
    telefoon.append(elements[6].text)
    fax.append(elements[7].text)
    email.append(elements[8].text)


f = open('bank_csv.csv',"w")
for i,j,k,l,m,n,o,p,q in zip(lid_number,titel,taal,accountant_sinds,
                             belastingconsultant_sinds,adres,telefoon,fax,email):
    f.write(i + ';' + j + ';' + k + ';' + l + ';' + m + ';' + n + ';' + o + ';' +
            p + ';' + q + '\n')