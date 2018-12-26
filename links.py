# -*- coding: utf-8 -*-
import requests, csv
from bs4 import BeautifulSoup
import time

names = []
addresses = []
numbers = []
links = []

for i in range(1,102):
    time.sleep(5)
    page = requests.get("https://www.yellowpages.com/search?search_terms=salon&geo_location_terms=Chicago%2C%20IL&page=" + str(i)).content

    soup = BeautifulSoup(page, 'html.parser')

    name = soup.find_all(attrs={"class": "business-name"})
    address = soup.select(".info-section")
    phone = soup.select(".info-section")

    j = 0
    for n in name: 
        try:
            if (j<30):
                names.append(n.select("span")[0].text)
                links.append(n.attrs['href'])
                print n.attrs['href']
            j+=1
        except:
            continue

    k = 0
    for n in address:
        try:
            if(k<30):
                addresses.append(n.select(".adr")[0].text)
            k += 1
        except:
            continue

    l = 0
    for n in phone:
        try:
            if(l<30):
                numbers.append(n.select(".phones")[0].text)
            l += 1
        except:
            continue

    print "Done reading page " + str(i)

s = 0
for link in links:
    page = requests.get("https://www.yellowpages.com" + link.strip()).content
    
    soup = BeautifulSoup(page, 'html.parser')

    email = soup.select(".email-business")

    try:
        if(s < len(numbers)):
            appendlist = [names[s].encode("utf-8").decode('ascii', 'ignore') , addresses[s].encode("utf-8").decode('ascii', 'ignore'), numbers[s].strip().encode("utf-8").decode('ascii', 'ignore'), email[0].attrs['href'][7:]]
    except:
        if(s < len(numbers)):
            appendlist = [names[s].encode("utf-8").decode('ascii', 'ignore') , addresses[s].encode("utf-8").decode('ascii', 'ignore'), numbers[s].strip().encode("utf-8").decode('ascii', 'ignore'), '']

    s = s + 1
    print appendlist

    with open('main.csv', 'a+') as f:
        writer = csv.writer(f, delimiter='#', lineterminator='\n')
        writer.writerow(appendlist)
