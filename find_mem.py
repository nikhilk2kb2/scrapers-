from bs4 import BeautifulSoup

import requests
import xlsxwriter
import string



html = None
soup = None

def get_pages(code):
    base_url= ('http://www.rics.org/ae/find-a-member/?sd=y&cc=%s&fn=&ln=&ct=&p=' % code)
    html = requests.get(base_url)
    soup = BeautifulSoup(html.content, "html.parser")
    page_count = soup.findAll("div", {"class": "search-sort"})
    strong_tag_data = page_count[0].findAll('strong')
    no_text = strong_tag_data[1].text
    return (get_details(int(no_text)/10,base_url))
    


def get_details(no_of_pages,base_url):
    found_data = []
    detail_page_url = 'https://www.rics.org/ae/find-a-member/member-profile/'
    for page_no in range(0,no_of_pages):
        list_html = requests.get(base_url + str(page_no))
        list_soup = BeautifulSoup(list_html.content, "html.parser")
        list_of_member_number = list_soup.findAll("strong", {"class": "membership-number"})
        for emp_no in list_of_member_number:
            try:
                detail_html = requests.get(detail_page_url + emp_no.text)
                print detail_html
            except:
                pass
            detail_soup = BeautifulSoup(detail_html.content, "html.parser")
            article = detail_soup.findAll("div", {"id": "content"})
            try:
                names = str(article[0].findAll('h1',{'class':'fn'})[0].text).split(' ')
            except:
                names = ''
            try:
                qualificatin = article[0].findAll('div',{'class':'content'})[0].find('p').text
            except:
                qualificatin = ''
            try:
                emp1 = str(article[0].findAll('dd',{'class':'clear'})[0].findAll('p')[0].text)
                emp2 = str(article[0].findAll('dd',{'class':'clear'})[0].findAll('strong')[0].text)
                employer = emp1 +''+ '-'+ emp2
            except:
                employer=''
            try:
                role_actual = str(article[0].findAll('dd',{'class':'role'})[0].findAll('p')[0].text)
                role = role_actual.translate(string.maketrans("\n\t\r", "   "))
            except:
                role = ''
            try:
                tel_actual = str(article[0].findAll('span',{'class':'value'})[0].text)
                tel = tel_actual.translate(string.maketrans("\n\t\r", "   ")) 
            except:
                tel = ''
            try:   
                email = article[0].findAll('a',{'class':'email'})[0].findAll('span')[0].text
            except:
                email = ''
            try:
                found_data.append({'f_name':names[0],'l_name':names[1],'qual':qualificatin,'emp':employer,'role':role,'tel':tel,'email':email}) 
            except:
                pass

    print found_data
    return found_data

            



def main_scrapper():
    # country={'UAE':'AE','OMAN':'OM','Qatar':'QA','Saudi Arebia':'SA','Bahrain':'BH'}
    country={'Saudi Arebia':'SA'}
    for key,val in country.iteritems():
        workbook = xlsxwriter.Workbook('data.xlsx')
        worksheet = workbook.add_worksheet(key)
        worksheet.set_column('A:H', 20)
        worksheet.write('A1', 'First Name')
        worksheet.write('B1', 'Family Name')
        worksheet.write('C1', 'Employer')
        worksheet.write('D1', 'Job Title ')
        worksheet.write('E1', 'Telephone')
        worksheet.write('F1', 'Email ')
        worksheet.write('G1', 'Qualification ')
        worksheet.write('H1', 'Location ')

        scraped_data = get_pages(val)
        count = 2
        for dt in scraped_data: 
            worksheet.write('A%s' % (count), dt['f_name'])
            worksheet.write('B%s' % (count), dt['l_name'])
            worksheet.write('C%s' % (count), dt['qual'])
            worksheet.write('D%s' % (count), dt['emp'])
            worksheet.write('E%s' % (count), dt['tel'])
            worksheet.write('G%s' % (count), dt['email'])
            worksheet.write('H%s' % (count), key)
            count = count + 1
    workbook.close()



if __name__ == '__main__':
    main_scrapper()
