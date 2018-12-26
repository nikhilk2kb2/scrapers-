import os
import time
# import csv
import xlwt
import requests
# from bs4 import BeautifulSoup
# from selenium import webdriver
# from selenium.common.exceptions import NoSuchElementException
# from selenium.webdriver.common.keys import Keys

from urllib.request import Request, urlopen
import re
from lxml import html
import time
# ###when window
# #driver=webdriver.Firefox(executable_path=r'C:\\Users\\pharry\\Downloads\\geckodriver\\geckodriver')
# #####
# #when ubuntu
# driver=webdriver.Firefox(executable_path=r'/media/pharry/New Volume/software/geckodriver')
# ###
# url='https://www.justdial.com/Mumbai/Holiday-Tour-Packages/nct-10489548'
# driver.get(url)
# time.sleep(8)
# webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
# body=driver.find_element_by_tag_name('body')
# for i in range(10):
# 	driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
# 	time.sleep(2)
# time.sleep(2)
# data_section=driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/div[2]/div[1]/div/section/div/ul')
# allagentLinks=data_section.find_elements_by_tag_name('li')
# a=[]
# for agent in allagentLinks:
# 	if agent.get_attribute("data-href"):
# 		a.append(agent.get_attribute("data-href"))
# 		print(agent.get_attribute("data-href"))
# print(len(a))
# #################

book = xlwt.Workbook(encoding="utf-8")
sheet1 = book.add_sheet("Results")
sheet1.write(0, 0, 'Agent Name')
sheet1.write(0, 1, 'Area')
sheet1.write(0, 2, 'Phone Number')
sheet1.write(0, 3, 'Address Detailed')
sheet1.write(0, 4, 'Website')

index=1
fh=open('mumbai_Agents_link.txt','r')
a=fh.read().strip().split('\n')
fh.close()
for url in a:
	req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
	webpage = urlopen(req).read()
	tree=html.fromstring(webpage)
	# phone_block=tree.xpath('/html/body/div[2]/div[1]/div/div[4]/div[1]/div[1]/ul/span[2]/a')[0]
	# print(html.tostring(phone_block))
	phone_list=tree.xpath('/html/body/div[2]/div[1]/div/div[1]/div[2]/div/ul/li[2]/p/span[2]/span/a/span')
	#print(phone_list)
	phone=''
	for digit in phone_list:
		dclass=digit.get('class')
		main_class=dclass.split()[1]
		ans=re.search('.'+main_class+':before[{]content[:]["](.*?)["][}]',webpage.decode())
		# print(ans.group())
		code=ans.group(1)[-2:]
		if int(code)-1<10:
			phone+=str(int(code)-1)
		else:
			phone+='+'

	# print("hello",tree.xpath('/html/body/div[2]/div[1]/div/div[1]/div[2]/div/ul/li[2]/p/span[2]/span/a/span[2]')[0].attrib['style'])
	# print('hello',html.tostring(tree.xpath('/html/body/div[2]/div[1]/div/div[1]/div[2]/div/ul/li[2]/p/span[2]/span/a/span[2]')[0]))
	agent_name=tree.xpath('/html/body/div[2]/div[1]/div/div[1]/div[2]/div/div/h1/span/span')[0].text
	address=tree.xpath('/html/body/div[2]/div[1]/div/div[4]/div[1]/div[1]/ul/li[1]/span[2]/span/span/span')[0].text
	website=""
	info_elements=tree.xpath('/html/body/div[2]/div[1]/div/div[4]/div[1]/div[1]/ul/li')
	# print(info_elements)
	for elem in info_elements:
		if elem.find('span/a')!=None and elem.find('span/a').attrib.get('href',None)!=None:
		    website=elem.find('span/a').attrib['href']
		    break
	print(agent_name.strip(),"\n")
	print(phone.strip(),"\n")
	print(address.strip(),"\n")
	print(website.strip(),"\n")
	print('\n##############\n')
	sheet1.write(index, 0, agent_name.strip())
	sheet1.write(index, 1, 'Mumbai')
	sheet1.write(index, 2, phone.strip())
	sheet1.write(index, 3, address.strip())
	sheet1.write(index, 4, website.strip())
	if (index)%100==0:
		output_file = 'TravelAgentMumbaiScrappedAt '+str(time.time())+'.xls'
		book.save(output_file)
	index+=1

output_file = 'TravelAgentMumbaiScrappedAt '+str(time.time())+'.xls'
book.save(output_file)
driver.quit()

#/html/body/div[2]/div[1]/div/div[4]/div[1]/div[1]/ul/li[3]/span