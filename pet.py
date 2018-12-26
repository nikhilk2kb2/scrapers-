from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time


fnames=[]
lnames=[]
emails=[]
options = Options()
df=pd.read_csv("details.csv")
#print(df["Fname"][2])
for i in range(0,10):

    fnames.append(df["Fname"][i])
    lnames.append(df["Lname"][i])
    emails.append(df["Email"][i])

#print(fnames,lnames,emails)

driver=webdriver.Chrome()
for i in range(0,10):

    driver.get("https://www.parliament.nz/en/petitions/sign/PET_80471")
    fname=driver.find_element_by_id("FirstName")
    fname.send_keys(fnames[i])
    time.sleep(2)
    lname=driver.find_element_by_id("LastName")
    lname.send_keys(lnames[i])
    time.sleep(2)
    email=driver.find_element_by_id("EmailAddress")
    email.send_keys(emails[i])
    time.sleep(2)
    terms=driver.find_element_by_id("Privacy")
    terms.click()
    time.sleep(2)
    frame = driver.find_element_by_xpath('//iframe[contains(@src, "recaptcha")]')
    driver.switch_to.frame(frame)
    captcha=driver.find_element_by_xpath("//*[@id='recaptcha-anchor']")
    captcha.click()
    time.sleep(2)
    driver.switch_to.default_content()
    sign=driver.find_element_by_class_name("form__multistep-control")
    sign.click()
    time.sleep(5)

