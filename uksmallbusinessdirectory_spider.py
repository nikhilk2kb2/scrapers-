import requests
from bs4 import BeautifulSoup as bs
import pandas as pd

def dataframe(df, full_data, category, link):
    #print(full_data)
    data = full_data[0].text.strip().split('\n\n\n\n\n\n\n\n\n')[0].strip()
    try:
        description = full_data[0].text.strip().split('\n\n\n\n\n\n\n\n\n')[1].strip().split('\n\n\n\n\n')[1].replace('\n', '').strip()
    except:
        description = full_data[0].text.strip('\n\n\n')[1].strip()

    desciption = description.replace('\n', '').replace('\r', '')

    title = data.split('\t\n')[0].strip().lstrip('Silver Listing').lstrip('Boost This Listing').strip()
    address = data.split('\t')[1].strip().split('Tel:')[0].strip().replace('\n\n', ', ')

    contact = data.split('Tel:')[1].strip()
    if 'Web:' in contact:
        link = contact.split('Web:')[1].strip()
        contact = contact.split('Web:')[0].strip()
    elif '\n\n' in contact:
        link = contact.split('\n\n')[1].strip()
        contact = contact.split('\n\n')[0].strip()

    df.loc[len(df)] = [category, title, address, contact, description, link]

    print(df.loc[len(df)-1])

    return df

def spider(df, link, category):
    search_page = requests.get(link).text

    search_page = bs(search_page, 'html.parser')

    data = search_page.select('.formcontainer:nth-child(1)')
    if not data:
        data = search_page.select('.nobordercontainer div div .formcontainer:nth-child(2)')
    if not data:
        data = search_page.select('.nobordercontainer .nobordercontainer') 
    
    df = dataframe(df, data, category, link)

    return df

def main():
    url_index = 'https://www.uksmallbusinessdirectory.co.uk'
    url = 'https://www.uksmallbusinessdirectory.co.uk/business-search/builder/'

    df = pd.DataFrame(columns=['category', 'title', 'address', 'contact', 'description', 'link'])

    page_source = requests.get(url).text

    page_source = bs(page_source, 'html.parser')

    links = page_source.select('.nobordercontainer li a')

    categories = []

    for i in range(len(links)):
        categories.append(links[i].text.strip())
        links[i] = url_index + links[i].get('href')

    #print(categories, links)

    for x in range(len(links)):
        print('Category', x+1)
        spider(df, links[x], categories[i])
        other_results = bs(requests.get(links[x]).text, 'html.parser').select('span a')

        for i in range(len(other_results)):
            other_results[i] = other_results[i].get('href')

        for i in range(len(other_results)):
            print('Data', i+2)
            df = spider(df, url_index+other_results[i], categories[x])
    
    df.to_csv('uksmallbusinessdirectory_data.csv', sep='|', index=None)

if __name__ == '__main__':
    main()
