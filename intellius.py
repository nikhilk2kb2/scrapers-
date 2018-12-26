import time
from bs4 import BeautifulSoup as BS
import sys
import csv
from selenium import webdriver
"""
importing some libraries for headless
"""
from selenium.webdriver.firefox.options import Options
options = Options()
options.add_argument("--headless")
from selenium.webdriver.common.keys import Keys

final_csv = open("final.csv", "w")

search_url = "https://iservices.intelius.com/premier/dashboard.php"

details = []
try:
    print "Trying to start firefox headless"
    #browser = webdriver.Firefox(firefox_options=options)
    browser = webdriver.Firefox()
    browser.set_page_load_timeout(10)
    print "started firefox headless"
    browser.get(search_url)
    time.sleep(10)

    username = browser.find_element_by_id("email")
    password = browser.find_element_by_id("password")
    username.send_keys("gemhomebuyers@gmail.com")
    password.send_keys("Fiverr2018")
    browser.find_element_by_class_name("button-b").click()
except Exception as e:
    print e
    pass

with open("sample.csv", "rb") as f:
    reader = csv.reader(f)
    for r in reader:
        details.append(r)
for i in range(1,len(details)):
    browser.get("https://iservices.intelius.com/premier/search.php?componentId=1&qf="+str(details[i][1]).replace(" ", "+")+"&qn="+str(details[i][2]).replace(" ", "+")+"&qcs="+str(details[i][4]).replace(" ", "+")+","+str(details[i][5]).replace(" ", "+"))
    #print browser.page_source
    soup = BS(browser.page_source, "html.parser")
    new = soup.findAll("div", {"class" : "identity"})
    name = new[0].findAll("a")
    print name[0].string
    final_csv.write(name[0].string+", ")
    age = new[0].findAll("strong")
    #print age
    print ("Age: "+age[0].string)
    final_csv.write(age[0].string+", ")
    new_add = soup.findAll("ul", {"class" : "info"})
    for x in new_add[0].strings:
        print(repr(x))
        if x != "\n" and x != ",                        " and "more" not in x:
            final_csv.write(x.lstrip().replace(" ", "")+", ")
    #address = new_add[0].findAll("p")
    #for x in address[0].strings:
    #    print x
    #print address[0].string
    new_ph = soup.findAll("ul", {"class" : "info2"})
    for x in new_ph[0].strings:
        print(x)
        if x != "\n" and x != ",                        " and "more" not in x:
            final_csv.write(x.lstrip().replace(" ", "")+", ")
    #phone = new_add[0].findAll("p")
    #for x in phone[0].strings:
    #    print x
    #print phone[0].string
    final_csv.write("\n")
    time.sleep(5)
