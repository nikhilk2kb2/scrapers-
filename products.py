import time
import sys
# sys.setdefaultencoding() does not exist, here!
reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException

profile = webdriver.FirefoxProfile()
profile.set_preference('intl.accept_languages', 'en')
browser = webdriver.Firefox(profile)

#links for products
links = []
#Individual Page params
product_name = []
article_no = []
main_img_url = []
thumb_img_url = []
colors = []
price = []
style = []
description = []
details = []
#in page insertion list
thumb_img_list = []
color_list = []
para_list = []

#methods to check presence of elements
def is_table_present():
    try: browser.find_element_by_xpath("//div[@class='tab-pane active']/table/tbody/tr[3]/td[2]/font/font")
    except NoSuchElementException: return False
    return True

def is_details_present(detail_div):
    try:
        detail_div.find_elements_by_xpath(".//*")

    except NoSuchElementException: return False
    return True



url = 'https://www.gtworld.de/category.aspx?id=10033768'

browser.get(url)

lang = Select(browser.find_element_by_class_name('goog-te-combo'))

lang.select_by_value('en')

time.sleep(3)

select = Select(browser.find_element_by_id('content_content_ctl00_ItemList1_PageSizectl_dlPageSize'))
select.select_by_value('9999')


links_fetched = browser.find_elements_by_class_name('product-name')

for node in links_fetched:
    links.append(node.get_attribute('href'))
    product_name.append(node.text)


for page_link in links:
    browser.get(page_link)
    time.sleep(1)
    lang = Select(browser.find_element_by_class_name('goog-te-combo'))
    lang.select_by_value('en')
    time.sleep(2)
    art_no = browser.find_element_by_id('content_content_ctl00_lProductID')
    article_no.append(art_no.text)
    image = browser.find_element_by_id('Productimage')
    main_img_url.append(image.get_attribute('src'))
    colors_name = browser.find_elements_by_class_name('thumbnail')
    for element in colors_name:
        color_list.append(element.text)

    colors.append(color_list)

    thumb_img = browser.find_elements_by_xpath("//a[@class='thumbnail']/img")

    for element in thumb_img:
        thumb_img_list.append(element.get_attribute('src'))

    thumb_img_url.append(thumb_img_list)

    price_ele = browser.find_element_by_id('content_content_ctl00_lYourPrice')

    price.append(price_ele.text)

    desc = browser.find_element_by_id('content_content_ctl00_lDescription')

    description.append(desc.text)

    if(is_table_present()):
        style_list = browser.find_element_by_xpath("//div[@class='tab-pane active']/table/tbody/tr[3]/td[2]/font/font")
        style.append(style_list.text)

    else:
        style.append('none')

    detail_div = browser.find_element_by_id('details')
    if (is_details_present(detail_div)):
        p_list = detail_div.find_elements_by_xpath(".//*")

        for p in p_list:
            para_list.append(p.text)

        details.append(para_list)
    else:
        details.append('none')




f = open("products.csv",'a')

'''
i -> product_name
j -> article_no  
k -> main_img_url 
l -> thumb_img_url
m -> price
n -> colors
o -> style
p -> description
q -> details
'''

for i,j,k,l,m,n,o,p,q in zip(product_name,article_no,main_img_url,thumb_img_url,price,colors,style,description,details):
    f.write(str(i) + ';' + str(j) + ';' + str(m) + ';'+ 'Hairtail' +';'+ 'Mixed'+ ';'+ 'Premium Hair' +';' + str(p) + ';' + str(q) + ';' + str(k) + ';' + str(o) + ';' + str(n) + ';' + str(l) + '\n')

f.close()
