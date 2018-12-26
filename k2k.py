import csv
import time
import requests
from w3lib.html import remove_tags
from multiprocessing import cpu_count 
from multiprocessing.pool import Pool, ThreadPool

baseUrl = 'https://api.widespreadsales.com/v1/products/store/cells/{}?category=Circuit+Breaker&subcategory=Molded+Case'
productUrl='https://api.widespreadsales.com/v1/products/store/{}'

def log(*args):
    ctime = time.strftime("%m-%d-%Y %H:%M:%S")
    print '{} [WideSpreadSpider] DEBUG: {}'.format(ctime, ' '.join(args)) 

def send_request(url):
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.170 Safari/537.36'}
    response = requests.get(url, headers=headers)
    log('Crawled', str(response.status_code), response.url)
    return response 


def init_feed_export():
    global csvfile
    global writer 

    filename = 'Widespread.csv'
    csvfile = open(filename, 'wb')
    fieldnames = ['Product Name', 'Part Number', 'Manufacturer', 'Sub-Category', 
        'Family', 'Type', 'Phase', 'Poles', 'Voltage', 'Amperage', 'Connection', 'Protection',
        'Functions', 'AIC Rating', 'Description', 'New Surplus Price', 'Re-Certified Price']

    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()


init_feed_export()

def parse_product(itemName):
    url = productUrl.format(itemName)
    productDetails = send_request(url).json()

    desc = productDetails.get('displayDescription', '')
    description = remove_tags(desc)

    try: new_surplus_price = productDetails['newSurplus']['stores']['widespread']['price']
    except: new_surplus_price = '0'

    try: re_certified_price = productDetails['refurbished']['stores']['widespread']['price']
    except: re_certified_price = '0'
        
    entry = {'Product Name': productDetails.get('name'),
        'Part Number': productDetails.get('name'),
        'Manufacturer': productDetails.get('manufacturers', [''])[0],
        'Sub-Category': productDetails.get('subcategory'),
        'Family': productDetails.get('family'),
        'Type': productDetails.get('type'),
        'Phase': productDetails.get('specs', {}).get('Phase', ''),
        'Poles': productDetails.get('specs', {}).get('Poles', ''),
        'Voltage': productDetails.get('specs', {}).get('Voltage', ''),
        'Amperage': productDetails.get('specs', {}).get('Amperage', ''),
        'Connection': productDetails.get('specs', {}).get('Connection', ''),
        'Protection': productDetails.get('specs', {}).get('Protection', ''),
        'Description': description,
        'Functions': productDetails.get('specs', {}).get('Functions', ''),
        'AIC Rating': productDetails.get('specs', {}).get('AIC Rating', ''),
        'New Surplus Price': new_surplus_price,
        'Re-Certified Price': re_certified_price
        }
    writer.writerow(entry)
    log('Scraped from ', '<'+str(200), productUrl, '>\n', str(entry))
        

def worker(page):
    url = baseUrl.format(page)
    response = send_request(url).json()
    
    items = [i['name'] for i in response['docs']]
    pool = Pool( cpu_count() ) 
    pool.map(parse_product, items)


def main():
    pageCount = 10 #13190
    
    pool = ThreadPool(processes=cpu_count())
    pool.map(worker, range(1, pageCount))

    csvfile.close()

if __name__ == '__main__':
    main()
