from multiprocessing import Pool
from bs4 import BeautifulSoup
import requests
import re
import time
import csv

def sendRequest(url,header):
	try:
		a=requests.get(url,headers=header)
		return a
	except:
		print('sleep')
		time.sleep(8)
		a=sendRequest(url,header)
		return a

def makePerfect(keyword):
	return keyword.replace(' ','_')

def makePerfectKeyword(keyword):
	return keyword.replace(' ','+')

def find_url_page(keyword,page_num,state,suburb):
	url='https://www.yellowpages.com.au/search/listings?clue={}&locationClue=&lat=&lon=&referredBy=UNKNOWN&selectedViewMode=list&eventType=refinement&openNow=false&pageNumber={}&state={}&suburb={}'.format(keyword,page_num,state,suburb)
	return url

def parse(d):
	#header={'user-agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'}
	header={'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:63.0) Gecko/20100101 Firefox/63.0'}
	# print(url)
	for page in range(1,30):
		url=find_url_page(makePerfectKeyword(d['keyword']),page,d['state'],d['subrub'])
		print(url)
		a=sendRequest(url,header)
		print(a.status_code)
		if(a.status_code==200):
			soup=BeautifulSoup(a.text,'html.parser')
			elem=soup.find_all('div',class_='cell in-area-cell find-show-more-trial middle-cell')
			pg=soup.find('span',class_='pagination current')
			if(pg!=None):
				pg=pg.text
			else:
				pg='1'
			patt='pageNumber=.*'
			qu=url.split('&')
			ind=0
			for i in range(len(qu)):
				if(re.match(patt,qu[i])):
					ind=i
					break
			pageNum=qu[i].split('=')[-1]
			print('len:',len(elem))
			if(len(elem)==0):
				print('May be problem')
			if(pg==pageNum):
				# print('matched')
				for i in range(len(elem)):
					cards=elem[i].find('div',class_='listing listing-search listing-data')
					phone="NA"
					mail="NA"
					website="NA"
					address="NA"
					title="NA"
					rating="NA"
					desc=""
					category=""
					if(cards!=None):
						contacts=cards.find_all('span',class_='contact-text')
						if(len(contacts)>0):
							phone=contacts[0].text.strip()
						category=cards.find('p',class_='listing-heading')
						if(category!=None):
							category=category.text.strip().split('-')[0].strip()
						else:
							category="NA"
						ratings=cards.find_all('span',class_='de-emphasis count-long')
						if(len(ratings)>0):
							rating=ratings[0].text.strip().split(' ')[0].strip()
						adds=cards.find_all('p',class_='listing-address mappable-address mappable-address-with-poi')
						if(len(adds)>0):
							address=adds[0].text.strip()
						elif(len(cards.find_all('p',class_='listing-address mappable-address'))>0):
							adds=cards.find_all('p',class_='listing-address mappable-address')
							address=adds[0].text.strip()
						title=cards.find('a',class_='listing-name')
						if(title!=None):
							title=title.text.strip()
						email=cards.find('a',class_='contact contact-main contact-email ')
						if(email!=None):
							mail=email.get('data-email').strip()
						web=cards.find_all('a',class_='contact contact-main contact-url ')
						if(len(web)>0):
							website=web[0].get('href').strip()
						descs=cards.find_all('li')
						if(len(descs)>0):
							for i in descs:
								desc=desc+i.text.strip()+","
							desc=desc[:-1]
							desc=desc.strip()
						else:
							desc="NA"
						# csv_file='data_yellowpage_mechanic_fast_1.csv'
						# csv_file='data_yellowpage_painter_fast_1.csv'
						csv_file='data_yellowpage_{}_.csv'
						csv_file=csv_file.format(makePerfect(d['keyword']))
						# print(2,csv_file)
						row=[title,category,desc,rating,address,phone,mail,website]
						if(i==0):
							print(row)
						with open(csv_file, mode='a') as file:
							writer = csv.writer(file)
							writer.writerow(row)
			else:
				break
			time.sleep(1)

# def find_url(page_num):
# 	# url='https://www.yellowpages.com.au/search/listings?clue=mechanical&pageNumber={}&referredBy=UNKNOWN&eventType=pagination'.format(page_num)
# 	url='https://www.yellowpages.com.au/search/listings?clue=Car+repair&eventType=pagination&openNow=false&pageNumber={}&referredBy=UNKNOWN&&state=NSW&suburb=Brookvale+NSW'.format(page_num)
# 	return url

# csv_file='data_yellowpage_mechanic_fast_1.csv'
# csv_file='data_yellowpage_painter_fast_1.csv'
# csv_file='data_yellowpage_sign_writter_fast_1.csv'
# head_row=['Name','Category','Description','Rating','Address','Phone','Mail','Website']
# with open(csv_file, mode='w') as file:
# 	writer = csv.writer(file)
# 	writer.writerow(head_row)
# list_pages=[i for i in range(1,30)]
# list_url=[]
# for i in range(1,30):
# 	list_url.append(find_url(i))
# for i in list_pages:
# 	parse(find_url(i))

# file_='subrub_mechanic.csv'
# file_='subrub_painter.csv'
with open('keywords_yellow_pages.txt','r') as f1:
	for line in f1:
		keyword=line.split('\n')[0].strip()
		file_='subrub_{}.csv'
		file_=file_.format(makePerfect(keyword))
		data=[]
		with open(file_,'r') as f:
			reader = csv.reader(f)
			data= [row for row in reader]
		data_dict=[]

		for i in range(1,len(data)):
			try:
				dict1={'state':'','subrub':'','keyword':''}
				subrub=data[i][1].replace(' ','+')+'+'+data[i][0]
				dict1['subrub']=subrub
				dict1['state']=data[i][0]
				dict1['keyword']=keyword
				data_dict.append(dict1)
			except:
				pass

		# data_dict=[{'state':'NSW','subrub':'Yerrinbool+NSW'}]

		# print(data_dict)
		csv_file='data_yellowpage_{}_.csv'
		csv_file=csv_file.format(makePerfect(keyword))
		# print(1,csv_file)
		head_row=['Name','Category','Description','Rating','Address','Phone','Mail','Website']
		with open(csv_file, mode='w') as file:
			writer = csv.writer(file)
			writer.writerow(head_row)
		print('FILE:',csv_file)
		for i in range(len(data_dict)):
		 	parse(data_dict[i])
		#with Pool(5) as p:
		#   p.map(parse,data_dict)