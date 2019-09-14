from bs4 import BeautifulSoup
import requests
import csv

user_agent= 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'

def scraper():
    response= requests.get('https://www.sec.gov/cgi-bin/own-disp?action=getissuer&CIK=0001318605', headers= {'user-agent':user_agent})
    soup= BeautifulSoup(response.content, 'html.parser')
    rows= soup.find_all('table')[6].findChildren('tr')
    links= []
    for r in range(1, len(rows)):
        a= rows[r].findChildren('td')[1].findChildren('a')[0]
        links.append('https://www.sec.gov'+a['href'])
    #print(links)
    for link in links:
        response= requests.get(link, headers= {'user-agent':user_agent})
        soup= BeautifulSoup(response.content, 'html.parser')
        rows= soup.find('table', class_= 'tableFile2').findChildren('tr')
        links_doc= []
        for r in range(1, len(rows)):
            a = rows[r].findChildren('td')[1].findChildren('a')[0]
            links_doc.append('https://www.sec.gov' + a['href'])
        #print(links_doc)
        for l in links_doc:
            try:
                html= requests.get(l, headers= {'user-agent':user_agent})
                soup_html= BeautifulSoup(html.content, 'html.parser')
                tr = soup_html.find('table', class_='tableFile').findChildren('tr')[1]
                url= 'https://www.sec.gov'+tr.findChildren('td')[2].findChildren('a')[0]['href']
                print(url)
                page= requests.get(url, headers= {'user-agent':user_agent})
                soup_page= BeautifulSoup(page.content, 'html.parser')
            except:
                continue

            try:
                try:
                    name= soup_page.select('td td a')[0].string.strip()
                except:
                    name= 'NA'

                try:
                    issuer= soup_page.select('br+ a')[0].string.strip()
                except:
                    issuer= 'NA'

                try:
                    date= soup_page.select('br+ .FormData')[0].string.strip()
                except:
                    date= 'NA'

                try:
                    relation= []
                    table_row= soup_page.select('br~ table')[0].findChildren('tr')
                    for row in table_row:
                        td= row.findChildren('span', class_= 'FormData')
                        if len(td) is not 0:
                            for t in td:
                                relation.append(t.findNext('td').contents[0].string.strip().partition('(')[0])
                    relation.append('')
                    relation= ','.join(relation).rstrip(',').rstrip(',')
                except Exception as e:
                    print(e)
                    relation= 'NA'

                try:
                    type= []
                    try:
                        table_row = soup_page.select('tr~ tr+ tr table')[0].findChildren('tr')
                        for row in table_row:
                            td = row.findChildren('span', class_='FormData')
                            if len(td) is not 0:
                                for t in td:
                                    type.append(t.findNext('td').contents[0].string.strip())
                        ''.join(type)
                    except:
                        table_row = soup_page.select('tr+ tr .MedSmallFormText+ table')[0].findChildren('tr')
                        for row in table_row:
                            td = row.findChildren('span', class_='FormData')
                            if len(td) is not 0:
                                for t in td:
                                    type.append(t.findNext('td').contents[0].string.strip())
                        ''.join(type)
                except Exception as e:
                    print(e)
                    type= 'NA'

                maindatatable1, j, t1= "", 1, []
                for record in soup_page.select('table:nth-child(3)')[0].find_all('tr'):
                    datatable1 = ""
                    for data in record.findAll('td'):
                        datatable1 = datatable1 + ';' + data.text.strip('\n')
                    maindatatable1 =  datatable1.lstrip(';')
                    i = j - 3
                    if i >= 1:
                        t1.append({'row'+str(i):maindatatable1})
                    j += 1

                maindatatable2, j, t2 = "", 1, []
                for record in soup_page.select('table+ table:nth-child(4)')[0].find_all('tr'):
                    datatable2 = ""
                    for data in record.findAll('td'):
                        datatable2 = datatable2 + ';' + data.text.strip('\n')
                    maindatatable2 = datatable2.lstrip(';')  # + '\n'
                    i = j-3
                    if i>=1:
                        #t2['row'+str(i)]= maindatatable2
                        t2.append({'row'+str(i):maindatatable2})
                    j += 1

                details= [name, issuer, date, relation, type[0], t1, t2]
                with open('form_data.csv', 'a', encoding='utf-8') as f:
                    writer= csv.writer(f, lineterminator='\n')
                    writer.writerow(details)
            except Exception as e:
                print(e )
                continue

if __name__=='__main__':
    row1= ['NAME', 'ISSUER NAME', 'DATE OF EARLIEST TRANSACTION', 'RELATIONSHIP OF REPORTING PERSON', 'INDIVIDUAL OR JOINT/GROUP FILLING',
           'TABLE 1', 'TABLE 2']
    with open('form_data.csv', 'w', encoding='utf-8') as f:
        writer = csv.writer(f, lineterminator='\n')
        writer.writerow(row1)
    scraper()







