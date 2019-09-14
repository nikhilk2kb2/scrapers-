from selenium import webdriver
import csv

def scraper(i):
    driver= webdriver.Chrome()
    driver.get('https://www.asx.com.au/asx/markets/futuresPriceList.do?code=IB&type=FUTURE')

    driver.find_element_by_xpath('//*[@id="asx24_category"]/option['+str(i)+']').click()
    driver.implicitly_wait(2)
    options_1= driver.find_element_by_id('asx24_subcategory').find_elements_by_tag_name('option')
    for j in range(2, len(options_1)+1):
        driver.find_element_by_xpath('//*[@id="asx24_subcategory"]/option['+str(j)+']').click()
        driver.implicitly_wait(2)
        types= driver.find_element_by_xpath('//*[@id="asx24_sec_type"]/option[2]').text
        if(types=='Futures'):
            category= driver.find_element_by_xpath('//*[@id="asx24_category"]/option['+str(i)+']').text.strip().replace(' ','_')
            subcategory= driver.find_element_by_xpath('//*[@id="asx24_subcategory"]/option['+str(j)+']').text.strip().replace('&','')
            headers = ['Expiry', 'Bid', 'Ask', 'Open', 'High', 'Low', 'Last Trade', 'Last Trade Time', 'Change',
                       'Traded Volume', 'Previous Settlement']
            with open(category+'_'+subcategory.replace('/','_')+'.csv', 'w') as f:
                writer = csv.writer(f, lineterminator='\n')
                writer.writerow(headers)
            driver.find_element_by_xpath('//*[@id="asx24_sec_type"]/option[2]').click()
            driver.implicitly_wait(2)
            table= driver.find_element_by_class_name('table-sfe')
            rows= table.find_elements_by_class_name('row-alt')
            for r in rows:
                data= []
                td= r.find_elements_by_tag_name('td')
                for d in td:
                    data.append(d.text.strip('\n'))
                with open(category+'_'+subcategory.replace('/','_')+'.csv', 'a', encoding='utf-8') as f:
                    writer= csv.writer(f, lineterminator= '\n')
                    writer.writerow(data)
    driver.close()


if __name__=='__main__':

    for i in range(2,8):
        scraper(i)




