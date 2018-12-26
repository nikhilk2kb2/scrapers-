from selenium import webdriver
from selenium.webdriver.support.ui import Select
import urllib2
import re
import time
from datetime import datetime, timedelta
import unicodecsv as csv
import json

def handleInput():
	postcode=raw_input("Enter the postcode:").strip()
	opt=int(raw_input("Enter 1 for sale and 2 for rent:"))
	if(opt==1):
		print('Your postcode is {}'.format(postcode))
		print('Your choice is {} for sale'.format(opt))
	elif(opt==2):
		print('Your postcode is {}'.format(postcode))
		print('Your choice is {} for rent'.format(opt))
	else:
		print('Incorrect Choice, Please Enter correct choice!')
		(postcode,opt)=handleInput()
	return (postcode,opt)

def sendRequest(url):
	try:
		header={'user-agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'}
		req=urllib2.Request(url,headers=header)
		# a=requests.get(url)
		a=urllib2.urlopen(req)
		return a
	except:
		print('sleep')
		time.sleep(8)
		a=sendRequest(url)
		return a

def getApiBuy(locId,page_index):
	url='https://www.rightmove.co.uk/api/_search?locationIdentifier={}&numberOfPropertiesPerPage=24&radius=0.0&sortType=2&index={}&maxDaysSinceAdded=1&viewType=LIST&channel=BUY&areaSizeUnit=sqft&currencyCode=GBP&isFetching=false&includeSSTC=true'.format(locId,page_index)
	return url
def getApiRent(locId,page_index):
	url='https://www.rightmove.co.uk/api/_search?locationIdentifier={}&numberOfPropertiesPerPage=24&radius=0.0&sortType=2&index={}&maxDaysSinceAdded=1&includeLetAgreed=false&viewType=LIST&channel=RENT&areaSizeUnit=sqft&currencyCode=GBP&isFetching=false'.format(locId,page_index)
	return url

(postcode,opt) = handleInput()
driver = webdriver.Firefox()
web_source=""
curr_url=""
total_no_page=0
if(opt==1):
	url='https://www.rightmove.co.uk/'
	driver.get(url)
	driver.implicitly_wait(4)
	total_no_page=0
	curr_urll=""
	try:
		elem=driver.find_element_by_id('searchLocation').send_keys(postcode)
		driver.find_element_by_id('buy').click()
		select = Select(driver.find_element_by_id("maxDaysSinceAdded"))
		select.select_by_visible_text('Last 24 hours')
		driver.find_elements_by_class_name('tickbox--indicator')[0].click()
		driver.find_element_by_id('submit').click()
		# web_source=driver.page_source
		curr_urll=driver.current_url
		# print(curr_urll)
		eme=driver.find_elements_by_class_name('pagination-pageSelect')[0]
		# print('hi')
		total_no_page=int(eme.find_elements_by_class_name('pagination-pageInfo')[-1].text.strip())
		# print(total_no_page)
		driver.quit()
	except:
		print('ERROR! Page Source may be changed/modified')
		driver.quit()
	l=curr_urll.split('&')
	locId=""
	patt='locationIdentifier=.*'
	for i in l:
		if(re.match(patt,i,re.IGNORECASE)):
			locId=i.split('=')[-1].strip()
	file_csv='info_flat_sale.csv'
	with open(file_csv,'w') as csvfile:
		writer = csv.writer(csvfile)
		writer.writerow(['Postcode','Bedrooms','Price','Style','Date','Reason'])
	for i in range(1,total_no_page+1):
		# print(locId)
		url=getApiBuy(locId,str((i-1)*24))
		# print(url)
		a=sendRequest(url)
		# print(a.status_code)
		if(a.getcode()==200):
			# data=a.json()
			data=json.load(a)
			listt=data['properties']
			pat='.*yesterday.*'
			dateAdded=""
			for i in range(len(listt)):
				if(re.match(pat,listt[i]['addedOrReduced'],re.IGNORECASE)):
					# print('hii')
					deltas=1
					dateAdded=datetime.strftime(datetime.now() - timedelta(deltas), '%d-%m-%Y')
					# row=[postcode,bedroom,prices,style,dateAdded]
					# print(row)
				else:
					deltas=0
					dateAdded=datetime.strftime(datetime.now() - timedelta(deltas), '%d-%m-%Y')
				bedroom=str(listt[i]['bedrooms'])
				prices=listt[i]['price']['displayPrices'][0]['displayPrice']
				# prices=str(listt[i]['price']['amount']).encode('utf-8').strip()
				style=listt[i]['propertySubType']
				reason=listt[i]['listingUpdate']['listingUpdateReason']
				row=[postcode,bedroom,prices,style,dateAdded,reason]
				# print(row)
				with open(file_csv,'a') as csvfile:
					writer = csv.writer(csvfile)
					writer.writerow(row)
		time.sleep(1)
else:
	url='https://www.rightmove.co.uk/'
	driver.get(url)
	driver.implicitly_wait(4)
	curr_urll=""
	try:
		elem=driver.find_element_by_id('searchLocation').send_keys(postcode)
		driver.find_element_by_id('rent').click()
		select = Select(driver.find_element_by_id("maxDaysSinceAdded"))
		select.select_by_visible_text('Last 24 hours')
		driver.find_element_by_id('submit').click()
		# web_source=driver.page_source
		eme=driver.find_elements_by_class_name('pagination-pageSelect')[0]
		# print('hi')
		curr_urll=driver.current_url
		# print(curr_urll)
		total_no_page=int(eme.find_elements_by_class_name('pagination-pageInfo')[-1].text.strip())
		# print(total_no_page)
		driver.quit()
	except:
		print('ERROR! Page Source may be changed/modified')
		driver.quit()
	l=curr_urll.split('&')
	locId=""
	patt='locationIdentifier=.*'
	for i in l:
		if(re.match(patt,i,re.IGNORECASE)):
			locId=i.split('=')[-1].strip()
	file_csv='info_flat_rent.csv'
	with open(file_csv,'w') as csvfile:
		writer = csv.writer(csvfile)
		writer.writerow(['Postcode','Bedrooms','Price','Style','Date','Reason'])
	for i in range(1,total_no_page+1):
		url=getApiRent(locId,str((i-1)*24))
		a=sendRequest(url)
		# print(a.status_code)
		if(a.getcode()==200):
			# data=a.json()
			data=json.load(a)
			listt=data['properties']
			pat='.*yesterday.*'
			dateAdded=""
			for i in range(len(listt)):
				if(re.match(pat,listt[i]['addedOrReduced'],re.IGNORECASE)):
					# print('hii')
					deltas=1
					dateAdded=datetime.strftime(datetime.now() - timedelta(deltas), '%d-%m-%Y')
				else:
					deltas=0
					dateAdded=datetime.strftime(datetime.now() - timedelta(deltas), '%d-%m-%Y')
				bedroom=str(listt[i]['bedrooms'])
				prices=listt[i]['price']['displayPrices'][0]['displayPrice']
				# prices=str(listt[i]['price']['amount'])
				style=listt[i]['propertySubType']
				reason=listt[i]['listingUpdate']['listingUpdateReason']
				row=[postcode,bedroom,prices,style,dateAdded,reason]
				# print(row)
				with open(file_csv,'a') as csvfile:
					writer = csv.writer(csvfile)
					writer.writerow(row)
		time.sleep(1)