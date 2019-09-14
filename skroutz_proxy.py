import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
import os
from time import sleep
import random

def spider(df, link):
    #proxies = ['46.102.96.5:60099', '46.102.96.23:60099', '46.102.96.42:60099', '46.102.96.71:60099', '46.102.96.122:60099', '46.102.96.173:60099', '46.102.96.180:60099', '46.102.96.192:60099', '46.102.96.231:60099', '46.102.96.237:60099', '46.102.97.3:60099', '46.102.97.52:60099', '46.102.97.66:60099', '46.102.97.75:60099', '46.102.97.155:60099', '46.102.97.156:60099', '46.102.97.182:60099', '46.102.97.211:60099', '46.102.97.230:60099', '46.102.97.234:60099', '46.102.98.31:60099', '46.102.98.38:60099', '46.102.98.57:60099', '46.102.98.69:60099', '46.102.98.158:60099', '46.102.98.170:60099', '46.102.98.176:60099', '46.102.98.183:60099', '46.102.98.205:60099', '46.102.98.223:60099', '46.102.99.10:60099', '46.102.99.61:60099', '46.102.99.72:60099', '46.102.99.85:60099', '46.102.99.110:60099', '46.102.99.160:60099', '46.102.99.169:60099', '46.102.99.182:60099', '46.102.99.202:60099', '46.102.99.212:60099', '94.177.67.32:60099', '94.177.67.152:60099', '94.177.67.208:60099', '94.176.109.12:60099', '94.176.109.27:60099', '94.176.109.38:60099', '94.176.109.67:60099', '94.176.109.83:60099', '94.176.109.146:60099', '94.176.109.150:60099', '94.176.109.172:60099', '94.176.109.188:60099', '94.176.109.241:60099', '94.177.67.23:60099', '94.177.67.97:60099', '94.177.67.126:60099', '94.177.67.157:60099', '94.177.67.171:60099', '94.177.67.201:60099', '94.177.67.226:60099', '86.107.62.3:60099', '86.107.62.37:60099', '86.107.62.67:60099', '86.107.62.125:60099', '86.107.62.137:60099', '86.107.62.161:60099', '86.107.62.188:60099', '86.107.62.211:60099', '86.107.62.212:60099', '86.107.62.242:60099', '89.34.103.34:60099', '89.34.103.36:60099', '89.34.103.77:60099', '89.34.103.88:60099', '89.34.103.136:60099', '89.34.103.155:60099', '89.34.103.161:60099', '89.34.103.193:60099', '89.34.103.205:60099', '89.34.103.231:60099', '89.39.255.6:60099', '89.39.255.52:60099', '89.39.255.60:60099', '89.39.255.61:60099', '89.39.255.126:60099', '89.39.255.149:60099', '89.39.255.189:60099', '89.39.255.205:60099', '89.39.255.222:60099', '89.39.255.228:60099', '195.66.142.18:60099', '195.66.142.61:60099', '195.66.142.66:60099', '195.66.142.77:60099', '195.66.142.90:60099', '195.66.142.146:60099', '195.66.142.165:60099', '195.66.142.197:60099', '195.66.142.205:60099', '195.66.142.247:60099']
    proxies = ['103.87.170.236:40650', '124.158.177.171:23500', '209.203.130.51:8080']
    headers = [{'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'}, {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}, {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'}, {'user-agent': 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322)'}, {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36'}, {'user-agent': 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)'}, {'user-agent': 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)'}]

    factory_code = link.split('=')[1]

    proxy = random.choice(proxies)
    response = requests.get(link, headers=random.choice(headers), proxies={'http': proxy, 'https': proxy})
    print(response)

    if '200' not in str(response):
        print('Daily limit exceeded, try again tommorow')

        exit()

    page_source = bs(response.text, 'html.parser')
    print(link)

    title = page_source.select('#sku-info > div:nth-child(1) > h1')
    if not title:
        return df
    else:
        title = title[0].text.replace('\n', '').strip()

    image = page_source.select('#sku-info > div.sku-card-wrapper.content > div > a.sku-image > img')[0].get('src')
    price1 = page_source.select('#shops .price .product-link')[0].text.strip()

    if len(page_source.select('#shops .price .product-link')) > 1:
        price2 = page_source.select('#prices .price .product-link')[1].text.strip()    
    else:
        price2 = ''
        price3 = ''

    if len(page_source.select('#shops .price .product-link')) > 2:
        price3 = page_source.select('#prices .price .product-link')[2].text.strip()
    else:
        price3 = ''

    specs = page_source.select('.spec-details')[0].find_all('dl')
    count = len(df)
    df.at[count, 'Factory Code'] = factory_code
    df.at[count, 'Product Name'] = title
    df.at[count, 'Image'] = image
    df.at[count, 'Price1'] = price1.split(' ')[0].replace(',', '.')
    
    if not price2:
        df.at[count, 'Price2'] = None
    else:
        df.at[count, 'Price2'] = price2.split(' ')[0].replace(',', '.')
    if not price3:
        df.at[count, 'Price3'] = None
    else:
        df.at[count, 'Price3'] = price3.split(' ')[0].replace(',', '.')
    
    specifications = '['
    for spec in specs:
        key = spec.find('dt').text
        value = spec.find('dd').text
        print(key, value)
        specifications = specifications + '"' + key + ':' + value + '"' + ', '
            
    df.at[count, 'Specifications'] = specifications.strip(', ') + ']'

    print(df.loc[len(df)-1])

    df.to_excel('skroutz_data.xlsx', index=None)

    return df
    

def main():
    search_url = 'https://www.skroutz.gr/search?keyphrase='
    products = pd.read_excel('input.xlsx')['factoruy code'].tolist()

    try:
        with open('count.txt', 'r') as f:
            f.seek(0)
            count = f.readline()
            if not count:
                count = 0
            else:
                count = int(count)
    except:
        count = 0

    file_path = '.\\skroutz_data.xlsx'

    if os.path.exists(os.path.join(os.getcwd(), file_path)) and count != 0:
        df = pd.read_excel('skroutz_data.xlsx')

    else:
        df = pd.DataFrame(columns=['Factory Code', 'Product Name', 'Image', 'Price1', 'Price2', 'Price3', 'Specifications'])

    for product in products[count:]:
        df = spider(df, search_url + str(product))
        count += 1
        with open('count.txt', 'w') as f:
            f.write(str(count))

        #sleep(8)

    df = df.drop_duplicates()
    df.to_excel('skroutz_data.xlsx', index=None)

if __name__ == '__main__':
    main()