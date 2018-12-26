# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re
import pandas as pd

from datetime import datetime, time

from time import time
import xlsxwriter





class F2(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "https://www.katalon.com/"
        self.verificationErrors = []
        self.accept_next_alert = True
        #self.dataframe=pd.read_csv('result.csv')

        self.newdataframe=pd.DataFrame(columns=['id','fullname','email','work_phone','mobile_phone','work_address','expertise'])

    def test_f2(self):

        #df = self.dataframe
        #list_id=df['MemberNo'].values.tolist()
        driver = self.driver

        #from 100045 to 800000


        for i in range(100045,800000):
            try:
               # prog_time = time.time()
                driver.get(
                 "https://www.fpi.co.za/FPI_Consumers/FPDetails.aspx?ID=" + str(i))


                table_path = "//table[@class='FullWidth']/tbody"
                full_list=self.getTableVersion2(table_path, driver)






                experince=driver.find_element_by_xpath(
                   "//tr[@id='ctl01_TemplateBody_WebPartManager1_gwpciNewQueryMenuCommon_ciNewQueryMenuCommon_ResultsGrid_Grid1_ctl00__0']/td").text

                address=driver.find_element_by_xpath(
                   "//div[@id='ctl01_TemplateBody_WebPartManager1_gwpciNewNotificationCommon_ciNewNotificationCommon_AlertContainer']/ul/li").text
                full_list.append(address)
                full_list.append(experince)
                full_list.append(i)
                self.set_values(full_list)
                #print("take {0} sec".format(time.time() - prog_time))






            except:
                self.save_csv(self.newdataframe)
                print ("no id="+str(i))




















        #print(driver.find_element_by_id("ctl01_TemplateBody_WebPartManager1_gwpciPeopleSearch_ciPeopleSearch_ResultsGrid_Grid1_ctl00").text())


        #x = driver.find_element_by_xpath((name)).get_attribute('href')










    def getTableVersion2(self,locator,driver):
     table = driver.find_element_by_xpath(locator)
     lists=[]
     for td in table.find_elements_by_tag_name('td'):
        lists.append(td.text)
     return lists






    def save_csv(self,df):
       df.to_csv('resultfinal.csv')













         #print ("Text in TD is " + td.text)
    def set_values(self,list):

        self.newdataframe.loc[len(self.newdataframe)] =[list[6],list[0],list[1],self.replace_str(list[2]),self.replace_str(list[3]),list[4],list[5]]
    def replace_str(self,list):
        str=re.findall('\d+', list)
        return str



    def is_element_present(self, how, what):
        try:
            self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e:
            return False
        return True



    def is_alert_present(self):
        try:
            self.driver.switch_to_alert()
        except NoAlertPresentException as e:
            return False
        return True

    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally:
            self.accept_next_alert = True

    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)


if __name__ == "__main__":
    unittest.main()
