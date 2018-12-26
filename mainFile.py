import pickle
import time

from selenium.webdriver.common.keys import Keys
import pandas as pd
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities

caps = DesiredCapabilities().CHROME
caps["pageLoadStrategy"] = "none"
# fp = webdriver.FirefoxProfile()
# fp.set_preference("http.response.timeout", 7)
# fp.set_preference("dom.max_script_run_time", 7)
# browser = webdriver.Firefox(firefox_profile=fp, capabilities=caps)
browser = webdriver.Chrome()  # ,
# browser.set_page_load_timeout(10)
max_pages = 9999999999
# desired_capabilities=caps)
main_url = "https://www.gumtree.com/for-sale"
try:
    browser.get("https://www.gumtree.com/login")
except:
    pass
time.sleep(10)
# ck = open("/home/nimish/PycharmProjects/so/internship/adsProject/cookies.pkl", "rb")
ck = open("/home/nimish/PycharmProjects/so/internship/adsProject/cookieList1.pkl", "rb")
cookies = pickle.load(ck)
ck.close()
time.sleep(13)
for cookie in cookies:
    browser.add_cookie(cookie)
# browser.add_cookie(cookies[6])

print("refreshing")
browser.refresh()
try:
    browser.get(main_url)
except:
    pass
time.sleep(6)
# max_pages = 7
urls = []
page_no = 1
while True:
    time.sleep(4)
    page_no += 1
    print("page_no", page_no)
    if page_no > max_pages:
        break
    a = browser.find_elements_by_css_selector("article a")
    here = 0
    for i in a:
        here += 1
        urls.append(i.get_attribute("href"))
    print(here)

    try:
        browser.find_elements_by_css_selector(".pagination-next")[0].click()
    except Exception as E:
        print(E)
        break

print("total urls extracted", len(urls))
# browser.set_page_load_timeout(4)
final_list = []
ctr = 0

start = 0
stop = len(urls)

for j in urls[start:stop]:
    ctr += 1
    if not j:
        continue
    print("url no ", ctr)
    try:
        browser.get(j+"?srn=True")
        time.sleep(4)
        # title = browser.find_element_by_id("ad-title").text
        title = str(browser.title)
        for k in browser.find_elements_by_css_selector(".txt-large"):
            if k.text.strip():
                print(k.text.strip())
                final_list.append((title, j, k.text))
                break
    except Exception as E:
        print(E)
        continue

pd.DataFrame(final_list).to_csv(main_url.split("/")[-1] + str(start) + "_" + str(stop) + ".csv")
