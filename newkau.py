import ast
import re
from selenium import webdriver
import time
import sys
"""
importing some libraries for headless
"""
from selenium.webdriver.firefox.options import Options
options = Options()
options.add_argument("--headless")
from selenium.webdriver.common.keys import Keys
search_url = "https://feedback.aliexpress.com/display/evaluationProductDetailAjaxService.htm?callback=jQuery1830869733211482397_1521399761658&productId=32777527172&type=default&page="
end_url = "&_=1521400004510"
login_url = "https://login.aliexpress.com/buyer.htm?spm=2114.11010108.1000002.7.5b4c649biNJs5F&return=https%3A%2F%2Fwww.aliexpress.com%2F%3Fsrc%3Dgoogle%26albch%3Dfbrnd%26acnt%3D304-410-9721%26isdl%3Dy%26aff_short_key%3DUneMJZVf%26albcp%3D54095668%26albag%3D1897140028%26slnk%3D%26trgt%3Daud-165594907443%3Akwd-14802285088%26plac%3D%26crea%3D257006900048%26netw%3Dg%26device%3Dc%26mtctp%3De%26memo1%3D1t1%26aff_platform%3Dgoogle%26gclid%3DCjwKCAjw7tfVBRB0EiwAiSYGM7IUQ2hpTSqLPWibxl5hvVaafn8dxhxlAU8TL28Ht3U4D3OPS9SN0RoCj0kQAvD_BwE&random=8D3D2CA3E9B51D529A22CF57D5E9CD60"
file_write = open("output.csv", "w")

try:
    print "Trying to start firefox headless"
    #browser = webdriver.Firefox(firefox_options=options)
    browser = webdriver.Firefox()
    browser.set_page_load_timeout(100)
    print "started firefox headless"
    browser.get("https://aliexpress.com")
    time.sleep(10)
    browser.get(login_url)
    username = browser.find_element_by_id("fm-login-id")
    password = browser.find_element_by_id("fm-login-password")
    username.send_keys("hydranoob000@gmail.com")
    password.send_keys("hydra1234")
    browser.find_element_by_id("fm-login-submit").click()
    time.sleep(5)
except Exception as e:
    print str(e) + "cannot continue further!"


for i in range(1,1000):
    try:
        browser.get(search_url+str(i)+end_url)
        #print browser.page_source
        data_raw = browser.page_source
        data_new = data_raw.replace("\n","").replace("  ","")
        print data_new
        x = ast.literal_eval(re.search('({.+})', data_new).group(0))
        for j in range(0,8):
            file_write.write(x['records'][j]['date']+str(", ")+x['records'][j]['countryCode']+str(", ")+x['records'][j]['quantity']+str("\n"))
        time.sleep(10)
    except Exception as d:
        print d
        pass
