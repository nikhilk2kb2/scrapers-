from selenium import webdriver
import re
import time
import csv

driver=webdriver.Firefox()

# url='https://shop.saveonfoods.com/store/31AC1213#/category/573,622/bagels/2?queries=sort%3DBrand'
url='https://shop.saveonfoods.com/store/31AC1213#/category/51089,51090/organic%20%26%20natural/1?queries=sort%3DBrand'

driver.get(url)
time.sleep(3)
file_='data_saveOnFood.csv'

# with open(file_, mode='w') as f:
# 	writer = csv.writer(f)
# 	writer.writerow(['Name','Size','Price','Description','SKU','Image','Category','Sub-Category','Link'])
category='organic & natural'
sub_category=''

sub=driver.find_elements_by_class_name('ungroupedProductList__title')
if(len(sub)>0):
	sub_category=sub[0].text.strip().split('(')[0].strip()
else:
	sub_category="NA"

l=driver.find_elements_by_class_name('productList.productList--gridView')
if(len(l)>0):
	productList1=l[0].find_elements_by_class_name('productList__product')
	for num in range(len(productList1)):
		driver.get(url)
		time.sleep(3)
		l1=driver.find_elements_by_class_name('productList.productList--gridView')
		productList=l1[0].find_elements_by_class_name('productList__product')
		product=productList[num]
		# print('prod:',product.text)
		size=''
		Size=product.find_elements_by_class_name('productInfo__size')
		if(len(Size)>0):
			size=Size[0].text
		else:
			size="NA"
		product.click()
		time.sleep(2)
		name=''
		price=''
		desc=''
		sku=''
		img=''
		info=driver.find_elements_by_class_name('primaryInformation')
		if(len(info)>0):
			infos=info[0].text.split('\n')
			name=infos[0]
			patt='.*$.*'
			for i in range(1,len(infos)-1):
				if(re.match(patt,infos[i])):
					price = price + infos[i].split(' ')[-1]+' '
			price=price.strip()
			if(re.match(patt,price)):
				pass
			else:
				price="NA"
		else:
			name="NA"
			price="NA"
		l=driver.find_elements_by_class_name('secondaryInformation__section')
		if(len(l)>0):
			infos=l[0].text.split('\n')
			patSku='sku.*'
			patDesc='description.*'
			sku_flag=0
			desc_flag=0
			if(len(infos)>0):
				if(re.match(patSku,infos[0].strip(),re.IGNORECASE)):
					skus=infos[0].split(' ')
					for j in range(1,len(skus)):
						sku = sku + skus[j]+' '
					sku=sku.strip()
					sku_flag=1
			if(len(infos)>1):
				if(re.match(patDesc,infos[-1].strip(),re.IGNORECASE)):
					descs=infos[-1].split(' ')
					for j in range(1,len(descs)):
						desc = desc + descs[j]+ ' '
					desc=desc.strip()
					desc_flag=1
			if(sku_flag==0):
				sku='NA'
			if(desc_flag==0):
				desc='NA'
		else:
			sku='NA'
			desc='NA'
		l=driver.find_elements_by_class_name('primaryImage__img')
		if(len(l)>0):
			img=l[0].get_attribute('src')
		else:
			img='NA'
		Link = driver.current_url
		row=[name,size,price,desc,sku,img,category,sub_category,Link]
		with open(file_, mode='a') as f:
			writer = csv.writer(f)
			writer.writerow(row)
		print(row)
		time.sleep(2)
driver.quit()
