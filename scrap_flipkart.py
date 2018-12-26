import requests
from bs4 import BeautifulSoup
import json
import time
import re

def sendRequest(url,header):
	try:
		a=requests.get(url,headers=header)
		return a
	except:
		print('sleep')
		time.sleep(8)
		a=sendRequest(url,header)
		return a

json_file=input('flip-1.json').strip()
d=[]
with open(json_file,'r') as f:
	d=json.loads(f.read())
data=[]
out_json_file='flip_data_out.json'
for i in range(len(d)):
	url=d[i]
	pat='.*flipkart.*'
	if(re.match(pat,url)):
		header={'user-agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'}
		response=sendRequest(url,header)
		if(response.status_code==200):
			soup=BeautifulSoup(response.text,'html.parser')
			title=""
			img=[]
			desc=""
			price=""
			l=soup.find_all('span',class_='_35KyD6')
			if(len(l)>0):
				title=l[0].text.strip().replace('\xa0','')
			else:
				title="NA"
			l=soup.find_all('div',class_='_1vC4OE _3qQ9m1')
			if(len(l)>0):
				price=l[0].text.strip()
			else:
				price="NA"
			l=soup.find_all('div',class_='_3la3Fn _1zZOAc')
			if(len(l)>0):
				desc=l[0].text.strip()
			else:
				desc="NA"
			l=soup.find_all('div',class_='_2_AcLJ')
			if(len(l)>0):
				for i in range(len(l)):
					imgUrl=l[i].get('style').split('(')[-1].split(')')[0]
					img.append(imgUrl)
			dict1={'title':title,'price':price,'img':img,'description':desc}
			data.append(dict1)
			print(dict1)
			json_str=json.dumps(dict1,indent=4,ensure_ascii=False)
			print(json_str)
			# with open(out_json_file,'a') as f1:
			# 	f1.write(json_str+'\n')
		time.sleep(1)
	else:
		header={'user-agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'}
		response=sendRequest(url,header)
		if(response.status_code==200):
			soup=BeautifulSoup(response.text,'lxml')
			title=""
			img=[]
			desc=""
			price=""
			l=soup.find(id='productTitle')
			if(l!=None):
				title=l.text.strip()
			else:
				title="NA"
			l=soup.find(id='priceblock_ourprice')
			if(l!=None):
				price=l.text.replace('\xa0\xa0','INR')
			else:
				price="NA"
			l=soup.find_all('ul',class_='a-unordered-list a-vertical a-spacing-none')
			if(len(l)>0):
				c=l[0].find_all('li')
				if(len(c)>0):
					for i in c:
						desc=desc+i.text.strip()+','
					desc=desc[:-1]
				else:
					desc='NA'
			else:
				desc="NA"
			c=soup.find_all('ul',class_='a-unordered-list a-nostyle a-button-list a-vertical a-spacing-top-extra-large')
			if(len(c)>0):
				d1=c[0].find_all('img')
				for i in range(len(d1)-1):
					imgUrl=d1[i].get('src').strip()
					img.append(imgUrl)
			dict1={'title':title,'price':price,'img':img,'description':desc}
			data.append(dict1)
			json_str=json.dumps(dict1,indent=4,ensure_ascii=False)
			print(json_str)	
		time.sleep(1)
json_str=json.dumps(data,indent=4,ensure_ascii=False)
# print(json_str)
with open(out_json_file,'a') as f1:
	f1.write(json_str+'\n')