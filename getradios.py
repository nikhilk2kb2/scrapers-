#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import selenium

import re
import datetime
import pytz
import atexit
import csv
import time
import random


def closewebdriver(driver):
    driver.close()

# ID, weekday (1,2,3...), Start time +utc, stop time +utc, channel name, language, program name

# 1210 (ID) - Deejay (channel name) - https://www.deejay.it/palinsesti/radio/
# 1210 (ID) - Radio 105 (channel name) - http://www.105.net/sezioni/937/palinsesto
# 1202 (ID) - RAI Radio 1 (channel name) - http://www.raiplayradio.it/radio1/palinsesto
# 1216 (ID) - Radio Capital (channel name) - https://www.capital.it/palinsesto/

# 1203 (ID) - RAI Radio 2 (channel name) - http://www.raiplayradio.it/radio2/palinsesto
# 1211 (ID) - Kiss Kiss (channel name) - https://www.kisskiss.it/radio/palinsesto.html
# 1219 (ID) - Radio 24 (channel name) - http://www.radio24.ilsole24ore.com/palinsesto
# 1209 (ID) - R 101(channel name) - http://www.r101.it/radio/palinsesto/
# 1223 (ID) - Radio Subasio (channel name) - http://www.radiosubasio.it/palinsesto/
# 1221 (ID) - m2o (channel name) - https://www.m2o.it/palinsesto/

def main():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(chrome_options=options)

    atexit.register(closewebdriver, driver) # closes browser window at the exit
    random.seed()

    programs = []

    program1 = get_radio1(driver, "https://www.deejay.it/palinsesti/radio/", 1210, "Deejay", "italian", "CET")
    programs.extend(program1)

    program2 = get_radio2(driver, "http://www.105.net/sezioni/937/palinsesto", 1210, "Radio 105", "italian", "CET")
    programs.extend(program2)

    program3 = get_radio3(driver, "http://www.raiplayradio.it/radio1/palinsesto", 1202, "RAI Radio 1", "italian", "CET")
    programs.extend(program3)

    program4 = get_radio4(driver, "https://www.capital.it/palinsesto/", 1216, "Radio Capital", "italian", "CET")
    programs.extend(program4)

    program5 = get_radio3(driver, "http://www.raiplayradio.it/radio2/palinsesto", 1203, "RAI Radio 2", "italian", "CET")
    programs.extend(program5)

    ### RADIO 6 SCRIPT HAS PROBLEMS:
    ### ELEMENTS ARE NOT OFTEN VISIBLE WHEN ATTEMPTING TO CLICK THEM
    program6 = get_radio6(driver, "https://www.kisskiss.it/radio/palinsesto.html", 1211, "Kiss Kiss", "italian", "CET")
    programs.extend(program6)

    program7 = get_radio7(driver, "http://www.radio24.ilsole24ore.com/palinsesto", 1219, "Radio 24", "italian", "CET")
    programs.extend(program7)

    program8 = get_radio8(driver, "http://www.r101.it/radio/palinsesto/", 1209, "R 101", "italian", "CET")
    programs.extend(program8)

    program9 = get_radio9(driver, "http://www.radiosubasio.it/palinsesto/", 1223, "Radio Subasio", "italian", "CET")
    programs.extend(program9)

    program10 = get_radio10(driver, "https://www.m2o.it/palinsesto/", 1221, "m2o", "italian", "CET")
    programs.extend(program10)
    
    
    file = "radioprograms.csv"
    with open(file, "w") as f:
        writer = csv.DictWriter(f, fieldnames = ("id", "weekday", "channel", "language", "start time", "stop time", "name"))
        writer.writeheader()
    
        for dailyprogram in programs:
            for p in dailyprogram:
                writer.writerow(p)

    f.close()

    print("Results saved to CSV file %s" % (file))
    
    #for dailyprogram in program6:
    #    for p in dailyprogram:
    #        print(p["id"], " ",
    #              p["weekday"], " ",
    #              p["channel"], " ",
    #              p["language"], " ",
    #              p["start time"], " ",
    #              p["stop time"], " ",
    #              p["name"])

            
def get_radio10(driver, url, id, channel, language, timezone):
    driver.get(url)

    # gets the first day of the week
    datenow = datetime.datetime.now(pytz.timezone(timezone))
    weekstart = datenow - datetime.timedelta(days=datenow.weekday(),microseconds=datenow.microsecond)
    weekstart = weekstart.replace(hour=0,minute=0,second=0)

    programlist = [[], [], [], [], [], [], []]
    rawprogramlist = [[], [], [], [], [], [], []]
    
    for d in range(1,8):
        programstart = weekstart + datetime.timedelta(days=d-1)
        datestr = programstart.strftime("%d-%m-%Y")

        print("Processing date %s from %s" % (datestr, url))

        pagelooksgood = False
        failure = False
        counter = -1

        str = '//section[@class="list"]/nav/ul/li';

        while(not pagelooksgood):
            counter = counter + 1

            if(counter > 20):
                print("FAILURE: Cannot load page. SKIPPING")
                failure = True
                break

            time.sleep(10)

            while True:
                tabelems = driver.find_elements_by_xpath(str)
                
                if(not tabelems):
                    print("WARN: Cannot parse document properly (date selection element)")
                    print("Retrying..")
                    driver.get(url)
                    time.sleep(15)
                else:
                    break
        
        
            # handle possible exception from clicking element that cannot handle it (yet)
            clicking_ok = False
            
            while True:
                try:
                    # activates the given day
                    if(tabelems):
                        tabelems[d-1].click()
                        clicking_ok = True
                        break
                    else:
                        print("WARN: Clicking date element failed (no link).")
                        print("Retrying..")
                        
                        driver.get(url) # reloads the whole webpage..
                        time.sleep(15)
                        break
                        
                except selenium.common.exceptions.WebDriverException as e:
                    print("WARN: Clicking date element failed (exception): " + e.__str__())
                    print("Retrying..")
                    
                    driver.get(url) # reloads the whole webpage..
                    time.sleep(15)
                    break

            if(clicking_ok == False):
                continue #retry from the start

        
            time.sleep(5) # waits for 5 seconds for the page to reload after click


            timeelems = driver.find_elements_by_xpath('//article/span[@class="start-hour"]')

            nameelems = driver.find_elements_by_xpath('//article/div[@class="text-list"]//h3[starts-with(@class,"title")]/a')

            if(not timeelems or not nameelems):
                print("WARN: Cannot parse document properly (program table)")
                print("Retryig..")
                continue

            pagelooksgood = True

        if(failure):
            continue # try the next day then

                # next we need to process each program element
        counter = 0
        L = min([len(timeelems),len(nameelems)])

        for i in range(0,L):
            timestr = timeelems[i].text;
            namestr = nameelems[i].text;

            if(not timestr or not namestr):
                # skip empty elems
                continue

            if(timestr == "" or namestr == ""):
                # skip empty elems
                continue

            match = re.search("(\d+):(\d+)", timestr)

            if(not match):
                print("WARN: Cannot parse document properly (badly formated time)")
                continue

            start_hour = int(match.group(1))
            start_min  = int(match.group(2))

            print(start_hour, start_min, namestr)

            rawprogramlist[d-1].append({
                "start hour" : start_hour,
                "start min"  : start_min,
                "name"       : namestr })
            
            counter = counter + 1
            
    max_hour = 0
            
    # processes rawprogramlist
    for d in range(1,8):
        programstart = weekstart + datetime.timedelta(days=d-1)

        index = -1

        for p in rawprogramlist[d-1]:
            index = index + 1

            start_hour = p["start hour"]
            start_min  = p["start min"]

            if(start_hour > max_hour):
                max_hour = start_hour

            startprogram = programstart.replace(
                hour=start_hour,minute=start_min,second=0)

            if(d > 0 and start_hour == 0 and start_min == 0):
                # adds extra day (its 00:00 the next day)                
                startprogram = startprogram + datetime.timedelta(days=1)
            else:
                if(start_hour < max_hour):
                    # we have went pass midnight so increase day by one
                    startprogram = startprogram + datetime.timedelta(days=1)

            # set the end time at the beginning of the next program
            
            if(index+1 < len(rawprogramlist[d-1])):
                end_hour = rawprogramlist[d-1][index+1]["start hour"]
                end_min  = rawprogramlist[d-1][index+1]["start min"]

                if(end_hour > max_hour):
                    max_hour = end_hour
                
                endprogram = programstart.replace(hour=end_hour, minute=end_min,
                                                  second=0)
                
                if(end_hour == 0 and end_min == 0):
                    # adds extra day (its 00:00 the next day)
                    endprogram = endprogram + datetime.timedelta(days=1)
                elif(end_hour < max_hour):
                    # we have went pass midnight so increase day by one
                    endprogram = endprogram + datetime.timedelta(days=1)
                
            else:
                if(d < len(rawprogramlist)):
                    if(len(rawprogramlist[d]) > 0):
                        # we need to look the program start from the next day
                        endprogram = programstart.replace(
                            hour=rawprogramlist[d][0]["start hour"],
                            minute=rawprogramlist[d][0]["start min"],second=0)
                else:
                    # guess 04:00 is the program stopping time as usual (no data)
                    endprogram = programstart.replace(hour=4,minute=0,second=0)
                
                # add extra day
                endprogram = endprogram + datetime.timedelta(days=1)

            # convert times to UTC
            starttime_utc = startprogram.astimezone(pytz.utc).strftime("%Y-%m-%d %H:%M:%S +0000")
            endtime_utc = endprogram.astimezone(pytz.utc).strftime("%Y-%m-%d %H:%M:%S +0000")
            print(id, d, starttime_utc, endtime_utc, channel, language, p["name"])

            programlist[d-1].append({
                "id" : id,
                "weekday" : d,
                "start time" : starttime_utc,
                "stop time" : endtime_utc,
                "channel" : channel,
                "language" : language,
                "name" : p["name"] })

    
    return programlist



def get_radio9(driver, url, id, channel, language, timezone):
    driver.get(url)

    # gets the first day of the week
    datenow = datetime.datetime.now(pytz.timezone(timezone))
    weekstart = datenow - datetime.timedelta(days=datenow.weekday(),microseconds=datenow.microsecond)
    weekstart = weekstart.replace(hour=0,minute=0,second=0)

    programlist = [[], [], [], [], [], [], []]
    
    for d in range(1,8):
        programstart = weekstart + datetime.timedelta(days=d-1)
        datestr = programstart.strftime("%d-%m-%Y")

        print("Processing date %s from %s" % (datestr, url))

        pagelooksgood = False
        failure = False
        counter = -1

        str = '//ul[@role="tablist"]/li';

        while(not pagelooksgood):
            counter = counter + 1

            if(counter > 20):
                print("FAILURE: Cannot load page. SKIPPING")
                failure = True
                break

            time.sleep(10)

            while True:
                tabelems = driver.find_elements_by_xpath(str)
                
                if(not tabelems):
                    print("WARN: Cannot parse document properly (date selection element)")
                    print("Retrying..")
                    driver.get(url)
                    time.sleep(15)
                else:
                    break
        
        
            # handle possible exception from clicking element that cannot handle it (yet)
            clicking_ok = False
            
            while True:
                try:
                    # activates the given day
                    if(tabelems):
                        tabelems[d-1].click()
                        clicking_ok = True
                        break
                    else:
                        print("WARN: Clicking date element failed (no link).")
                        print("Retrying..")
                        
                        driver.get(url) # reloads the whole webpage..
                        time.sleep(15)
                        break
                        
                except selenium.common.exceptions.WebDriverException as e:
                    print("WARN: Clicking date element failed (exception): " + e.__str__())
                    print("Retrying..")
                    
                    driver.get(url) # reloads the whole webpage..
                    time.sleep(15)
                    break

            if(clicking_ok == False):
                continue #retry from the start

        
            time.sleep(5) # waits for 5 seconds for the page to reload after click


            timeelems = driver.find_elements_by_xpath('//td[@class="pal_time"]//h3')

            nameelems = driver.find_elements_by_xpath('//td[@class="pal_name"]//h2')

            if(not timeelems or not nameelems):
                print("WARN: Cannot parse document properly (program table)")
                print("Retryig..")
                continue

            pagelooksgood = True

        if(failure):
            continue # try the next day then
        
        # next we need to process each program element
        counter = 0
        L = min([len(timeelems),len(nameelems)])

        for i in range(0,L):
            timestr = timeelems[i].text;
            namestr = nameelems[i].text;

            if(not timestr or not namestr):
                # skip empty elems
                continue

            if(timestr == "" or namestr == ""):
                # skip empty elems
                continue

            match = re.search("(\d+):(\d+)\s+-\s+(\d+):(\d+)", timestr)

            if(not match):
                print("WARN: Cannot parse document properly (badly formated time)")
                continue

            start_hour = int(match.group(1))
            start_min  = int(match.group(2))
            end_hour   = int(match.group(3))
            end_min    = int(match.group(4))

            startprogram = programstart.replace(
                hour=start_hour,minute=start_min,second=0)

            if(counter > 0 and start_hour == 0 and start_min == 0):
                # adds extra day (its 00:00 the next day)
                startprogram = startprogram + datetime.timedelta(days=1)

            endprogram = programstart.replace(hour=end_hour, minute=end_min,
                                              second=0)
                
            if(end_hour == 0 and end_min == 0):
                # adds extra day (its 00:00 the next day)
                endprogram = endprogram + datetime.timedelta(days=1)
                
            # convert times to UTC
            starttime_utc = startprogram.astimezone(pytz.utc).strftime("%Y-%m-%d %H:%M:%S +0000")
            endtime_utc = endprogram.astimezone(pytz.utc).strftime("%Y-%m-%d %H:%M:%S +0000")
            print(id, d, starttime_utc, endtime_utc, channel, language, namestr)

            programlist[d-1].append({
                "id" : id,
                "weekday" : d,
                "start time" : starttime_utc,
                "stop time" : endtime_utc,
                "channel" : channel,
                "language" : language,
                "name" : namestr })

            counter = counter + 1
                
    
    return programlist
    
    

def get_radio8(driver, url, id, channel, language, timezone):
    driver.get(url)

    # gets the first day of the week
    datenow = datetime.datetime.now(pytz.timezone(timezone))
    weekstart = datenow - datetime.timedelta(days=datenow.weekday(),microseconds=datenow.microsecond)
    weekstart = weekstart.replace(hour=0,minute=0,second=0)

    programlist = [[], [], [], [], [], [], []]
    rawprogramlist = [[], [], [], [], [], [], []]

    daystr = ["LUN", "MAR", "MER", "GIO", "VEN", "SAB", "DOM"]

    for d in range(1,8):
        programstart = weekstart + datetime.timedelta(days=d-1)
        datestr = programstart.strftime("%d-%m-%Y")

        print("Processing date %s from %s" % (datestr, url))

        pagelooksgood = False
        failure = False
        counter = -1

        str = '//div[@data-tabday="%s"]/div' % (daystr[d-1]);

        while(not pagelooksgood):
            counter = counter + 1

            if(counter > 20):
                print("FAILURE: Cannot load page. SKIPPING")
                failure = True
                break

            time.sleep(10)

            while True:
                tabelems = driver.find_elements_by_xpath(str)
                
                if(not tabelems):
                    print("WARN: Cannot parse document properly (date selection element)")
                    print("Retrying..")
                    driver.get(url)
                    time.sleep(15)
                else:
                    break
        
        
            # handle possible exception from clicking element that cannot handle it (yet)
            clicking_ok = False
            
            while True:
                try:
                    # activates the given day
                    if(tabelems):
                        tabelems[0].click()
                        clicking_ok = True
                        break
                    else:
                        print("WARN: Clicking date element failed (no link).")
                        print("Retrying..")
                        
                        driver.get(url) # reloads the whole webpage..
                        time.sleep(15)
                        break
                        
                except selenium.common.exceptions.WebDriverException as e:
                    print("WARN: Clicking date element failed (exception): " + e.__str__())
                    print("Retrying..")
                    
                    driver.get(url) # reloads the whole webpage..
                    time.sleep(15)
                    break

            if(clicking_ok == False):
                continue #retry from the start

        
            time.sleep(5) # waits for 5 seconds for the page to reload after click


            programelems = driver.find_elements_by_xpath('//div[@data-day="%s"]/ul/li' % daystr[d-1])

            if(not programelems):
                print("WARN: Cannot parse document properly (program tables)")
                print("Retryig..")
                continue

            pagelooksgood = True

        if(failure):
            continue # try the next day then
        
        # next we need to process each program element

        counter = 0

        for p in programelems:
            start_time = p.get_attribute("data-start")
            end_time   = p.get_attribute("data-end")

            if(not start_time or not end_time):
                print("WARN: Cannot parse document properly (no time element)")
                continue

            start_time = start_time.strip()
            end_time   = end_time.strip()

            if(start_time == "" or end_time == ""):
                print("WARN: Cannot parse document properly (bad time element)")
                continue

            titleelem = p.find_elements_by_xpath(".//h3")

            if(not titleelem):
                print("WARN: Cannot parse document properly (no title element)")
                continue

            title = titleelem[0].text.strip()

            match = re.search("(\d+):(\d+)",start_time)

            if(not match):
                match = re.search("(\d+)",start_time)

                if(match):
                    start_hour = int(match.group(1))
                    start_min  = 0
                else:
                    print("WARN: Cannot parse document properly (invalid time format)")
                    continue # cannot parse elements
            else:
                start_hour = int(match.group(1))
                start_min  = int(match.group(2))

            match = re.search("(\d+):(\d+)",end_time)

            if(not match):
                match = re.search("(\d+)",end_time)

                if(match):
                    end_hour = int(match.group(1))
                    end_min  = 0
                else:
                    print("WARN: Cannot parse document properly (invalid time format)")
                    continue # cannot parse elements
            else:
                end_hour = int(match.group(1))
                end_min  = int(match.group(2))

            
            startprogram = programstart.replace(
                hour=start_hour,minute=start_min,second=0)

            if(counter > 0 and start_hour == 0 and start_min == 0):
                # adds extra day (its 00:00 the next day)
                startprogram = startprogram + datetime.timedelta(days=1)

            endprogram = programstart.replace(hour=end_hour, minute=end_min,
                                              second=0)
                
            if(end_hour == 0 and end_min == 0):
                # adds extra day (its 00:00 the next day)
                endprogram = endprogram + datetime.timedelta(days=1)
                
            # convert times to UTC
            starttime_utc = startprogram.astimezone(pytz.utc).strftime("%Y-%m-%d %H:%M:%S +0000")
            endtime_utc = endprogram.astimezone(pytz.utc).strftime("%Y-%m-%d %H:%M:%S +0000")
            print(id, d, starttime_utc, endtime_utc, channel, language, title)

            programlist[d-1].append({
                "id" : id,
                "weekday" : d,
                "start time" : starttime_utc,
                "stop time" : endtime_utc,
                "channel" : channel,
                "language" : language,
                "name" : title })

            counter = counter + 1
    


def get_radio7(driver, url, id, channel, language, timezone):
    driver.get(url)

    # gets the first day of the week
    datenow = datetime.datetime.now(pytz.timezone(timezone))
    weekstart = datenow - datetime.timedelta(days=datenow.weekday(),microseconds=datenow.microsecond)
    weekstart = weekstart.replace(hour=0,minute=0,second=0)

    programlist = [[], [], [], [], [], [], []]
    rawprogramlist = [[], [], [], [], [], [], []]
    

    for d in range(1,8):
        programstart = weekstart + datetime.timedelta(days=d-1)
        datestr = programstart.strftime("%d-%m-%Y")

        print("Processing date %s from %s" % (datestr, url))

        pagelooksgood = False

        str = '//a[@href="#calset--%d"]' % (d);

        daystr = ["lun", "mar", "mer", "gio", "ven", "sab", "dom"]

        while(not pagelooksgood):

            time.sleep(10)

            while True:
                tabelems = driver.find_elements_by_xpath(str)
                
                if(not tabelems):
                    print("WARN: Cannot parse document properly (date selection element)")
                    print("Retrying..")
                    driver.get(url)
                    time.sleep(15)
                else:
                    break
        
        
            # handle possible exception from clicking element that cannot handle it (yet)
            clicking_ok = False
            
            while True:
                try:
                    # activates the given day
                    if(tabelems):
                        tabelems[0].click()
                        clicking_ok = True
                        break
                    else:
                        print("WARN: Clicking date element failed (no link).")
                        print("Retrying..")
                        
                        driver.get(url) # reloads the whole webpage..
                        time.sleep(15)
                        break
                        
                except selenium.common.exceptions.WebDriverException as e:
                    print("WARN: Clicking date element failed (exception): " + e.__str__())
                    print("Retrying..")
                    
                    driver.get(url) # reloads the whole webpage..
                    time.sleep(15)
                    break

            if(clicking_ok == False):
                continue #retry from the start

        
            time.sleep(5) # waits for 5 seconds for the page to reload after click


            programtables = driver.find_elements_by_xpath('//div[starts-with(@class,"programmazione__dettagli")]')            

            if(not programtables):
                print("WARN: Cannot parse document properly (program tables)")
                print("Retryig..")
                continue

            linkelement = driver.find_elements_by_xpath("//a[starts-with(@class,'programmazione__fasciaOraria j-prg-%s')]" % daystr[d-1]) # mat, pom, ser

            if(not linkelement):
                print("WARN: Cannot parse document properly (no date part link)")
                print("Retrying..")
                continue

            clicking_ok = False

            while True:
                try:
                    # activates the given day
                    if(linkelement):
                        for i in range(0,len(linkelement)):

                            # if a.class has isActive then
                            # we dont need to click the element
                            if(linkelement[i].get_attribute("class").find("isActive") == -1):
                                time.sleep(2)
                                print("Clicking element %d" % (i))
                                linkelement[i].click()
                            else:
                                print("Element %d already active" % (i))
                                

                        clicking_ok = True
                        break
                    else:
                        print("WARN: Clicking datepart element failed (no link).")
                        print("Retrying..")

                        driver.get(url) # reloads the whole webpage..
                        time.sleep(15)
                        break
                        
                except selenium.common.exceptions.WebDriverException as e:
                    print("WARN: Clicking datepart element failed (exception): " + e.__str__())
                    print("Retrying..")

                    driver.get(url) # reloads the whole webpage..
                    time.sleep(15)
                    break

            if(clicking_ok == False):
                continue #retry from the start
            
            
            pagelooksgood = True
        
        # next we need to process each program element


        #<a href="#" class="programmazione__fasciaOraria j-prg-gio-mat" data-toggleclass-target=".j-prg-gio-mat" data-scrolltoggle-item="">Mattino</a>
        
        #<a href="#" class="programmazione__fasciaOraria j-prg-gio-pom isActive" data-toggleclass-target=".j-prg-gio-pom" data-scrolltoggle-item="">Pomeriggio</a>

        #<a href="#" class="programmazione__fasciaOraria j-prg-gio-ser" data-toggleclass-target=".j-prg-gio-ser" data-scrolltoggle-item="">Sera</a>
        

        timeelems = driver.find_elements_by_xpath("//span[@class='orario__label']")
        titleelems = driver.find_elements_by_xpath(".//h3[@class='dettaglioPuntata__titolo']")

        if(timeelems and titleelems):
            for index in range(0,len(timeelems)):
                if(timeelems[index].text != ""):
                    print(timeelems[index].text)

                    start_time = timeelems[index].text.strip()
                    
                    if(index < len(titleelems)):
                        print(titleelems[index].text)
                        name = titleelems[index].text.strip()

                        match = re.search("(\d+):(\d+)", start_time)

                        if(match):
                            start_hour = int(match.group(1))
                            start_min  = int(match.group(2))

                            rawprogramlist[d-1].append({
                                "start hour" : start_hour,
                                "start min"  : start_min,
                                "name" : name})
        continue


    # processes rawprogramlist
    for d in range(1,8):
        programstart = weekstart + datetime.timedelta(days=d-1)

        index = -1

        for p in rawprogramlist[d-1]:
            index = index + 1

            start_hour = p["start hour"]
            start_min  = p["start min"]

            startprogram = programstart.replace(
                hour=start_hour,minute=start_min,second=0)

            if(d > 0 and start_hour == 0 and start_min == 0):
                # adds extra day (its 00:00 the next day)
                startprogram = startprogram + datetime.timedelta(days=1)

            # set the end time at the beginning of the next program
            
            if(index+1 < len(rawprogramlist[d-1])):
                end_hour = rawprogramlist[d-1][index+1]["start hour"]
                end_min  = rawprogramlist[d-1][index+1]["start min"]
                
                endprogram = programstart.replace(hour=end_hour, minute=end_min,
                                                  second=0)
                
                if(end_hour == 0 and end_min == 0):
                    # adds extra day (its 00:00 the next day)
                    endprogram = endprogram + datetime.timedelta(days=1)
                
            else:
                if(d < len(rawprogramlist)):
                    if(len(rawprogramlist[d]) > 0):
                        # we need to look the program start from the next day
                        endprogram = programstart.replace(
                            hour=rawprogramlist[d][0]["start hour"],
                            minute=rawprogramlist[d][0]["start min"],second=0)
                else:
                    # guess 06:00 is the program stopping time as usual (no data)
                    endprogram = programstart.replace(hour=6,minute=0,second=0)
                
                # add extra day
                endprogram = endprogram + datetime.timedelta(days=1)

            # convert times to UTC
            starttime_utc = startprogram.astimezone(pytz.utc).strftime("%Y-%m-%d %H:%M:%S +0000")
            endtime_utc = endprogram.astimezone(pytz.utc).strftime("%Y-%m-%d %H:%M:%S +0000")
            print(id, d, starttime_utc, endtime_utc, channel, language, p["name"])

            programlist[d-1].append({
                "id" : id,
                "weekday" : d,
                "start time" : starttime_utc,
                "stop time" : endtime_utc,
                "channel" : channel,
                "language" : language,
                "name" : p["name"] })

    return programlist



def get_radio6(driver, url, id, channel, language, timezone):
    driver.get(url)

    # gets the first day of the week
    datenow = datetime.datetime.now(pytz.timezone(timezone))
    weekstart = datenow - datetime.timedelta(days=datenow.weekday(),microseconds=datenow.microsecond)
    weekstart = weekstart.replace(hour=0,minute=0,second=0)

    programlist = [[], [], [], [], [], [], []]

    daystrings = ["lunedi", "martedi", "mercoledi",
                  "giovedi", "venerdi", "sabato", "domenica"]

    for d in range(1,8):
        time.sleep(5)
        
        programstart = weekstart + datetime.timedelta(days=d-1)
        datestr = programstart.strftime("%d-%m-%Y")

        print("Processing date %s (%s) from %s" % (datestr, daystrings[d-1], url))

        str = '//input[@name="%s"]/..' % (daystrings[d-1]);

        pagelooksgood = False

        while(not pagelooksgood):

            cookie_button = driver.find_elements_by_xpath('//div[@class="cookie_button"]')
            if(cookie_button):
                while True:
                    try:
                        if(cookie_button):
                            index = random.randrange(len(cookie_button))
                            print("Clicking cookie button %d/%d" % (index,len(cookie_button)))
                            cookie_button[index].click()
                            time.sleep(2)
                        break
                    except selenium.common.exceptions.WebDriverException as e:
                        print("WARN: Clicking cookie element failed: " + e.__str__())
                        print("Retrying..")
                        driver.get(url)
                        time.sleep(5)
                        cookie_button = driver.find_elements_by_xpath('//div[@class="cookie_button"]')
                        
            

            while True:
                time.sleep(5)
                tabelems = driver.find_elements_by_xpath(str)
                
                if(not tabelems):
                    print("WARN: Cannot parse document properly (date selection element)")
                    print("Retrying..")
                    time.sleep(30)
                    driver.get(url)
                else:
                    break
        
        
            # handle possible exception from clicking element that cannot handle it (yet)
            while True:
                try:
                    # activates the given day
                    if(tabelems):
                        time.sleep(30)
                        tabelems[0].click()
                        break
                    else:
                        print("WARN: Clicking date element failed (no tabelems).")
                        print("Retrying..")
                    
                        time.sleep(30)
                        driver.get(url) # reloads the whole webpage..
                        time.sleep(5)
                        tabelems = driver.find_elements_by_xpath(str)
                        
                except selenium.common.exceptions.WebDriverException as e:
                    print("WARN: Clicking date element failed: " + e.__str__())
                    print("Retrying..")
                
                    time.sleep(30)
                    driver.get(url) # reloads the whole webpage..
                    time.sleep(5)
                    tabelems = driver.find_elements_by_xpath(str)

        
            time.sleep(5) # waits for 10 seconds for the page to reload after click

            programtables = driver.find_elements_by_xpath('//ul[@class="items_list"]//table')            
            
            if(not programtables):
                print("WARN: Cannot parse document properly (program tables)")
                print("Retryig..")
                continue

            if(len(programtables) > 2):
                pagelooksgood = True
            else:
                print("WARN: Cannot parse document properly (program tables)")
                print("Retryig..")
                continue

        pindex = 2

        while(pindex < len(programtables)):
              programdata = programtables[pindex].find_elements_by_xpath('.//td')

              pindex = pindex + 1

              if(not programdata):
                  print("WARN: Cannot parse document properly (no program data)")
                  continue

              index = 0

              while(index+3 < len(programdata)):            
            
                  start_time = programdata[index+0].text
                  end_time   = programdata[index+1].text
                  name       = programdata[index+2].text
                  link       = programdata[index+3].text

                  index = index + 4

                  start_time = re.sub('"','',start_time).strip()
                  end_time = re.sub('"','',end_time).strip()
                  name = re.sub('<\/?.+\/?>', '', name).strip() # removes html tags

                  match = re.search("(\d+):(\d+)", start_time)

                  if(not match):
                      print("WARN: Cannot parse document properly (start time)")
                      continue
                  
                  start_hour = int(match.group(1))
                  start_min  = int(match.group(2))
                  
                  match = re.search("(\d+):(\d+)", end_time)
                  
                  if(not match):
                      print("WARN: Cannot parse document properly (end time)")
                      continue
            
                  end_hour   = int(match.group(1))
                  end_min    = int(match.group(2))

                  # generate timedata elements from time information and change to UTC time
                  
                  startprogram = programstart.replace(hour=start_hour,minute=start_min,second=0)
                  endprogram = programstart.replace(hour=end_hour,minute=end_min,second=0)
                  
                  if(end_hour == 0 and end_min == 0):
                      # midnight means the next days midnight
                      endprogram = endprogram + datetime.timedelta(days=1)
            
                  # UTC
                  starttime_utc = startprogram.astimezone(pytz.utc).strftime("%Y-%m-%d %H:%M:%S +0000")
                  endtime_utc = endprogram.astimezone(pytz.utc).strftime("%Y-%m-%d %H:%M:%S +0000")
                  print(id, d, starttime_utc, endtime_utc, channel, language, name)

                  programlist[d-1].append({
                      "id" : id,
                      "weekday" : d,
                      "start time" : starttime_utc,
                      "stop time" : endtime_utc,
                      "channel" : channel,
                      "language" : language,
                      "name" : name })
        
        # its seems necessary to sleep for a long time between
        # clicking another date url.
        time.sleep(5)
    
    return programlist


def get_radio4(driver, url, id, channel, language, timezone):
    driver.get(url)

    # gets the first day of the week
    datenow = datetime.datetime.now(pytz.timezone(timezone))
    weekstart = datenow - datetime.timedelta(days=datenow.weekday(),microseconds=datenow.microsecond)
    weekstart = weekstart.replace(hour=0,minute=0,second=0)

    programlist = [[], [], [], [], [], [], []]
    rawprogramlist = [[], [], [], [], [], [], []]

    for d in range(1,8):
        programstart = weekstart + datetime.timedelta(days=d-1)
        datestr = programstart.strftime("%d-%m-%Y")

        print("Processing date %s from %s" % (datestr, url))

        str = "//section[@class='list']/nav/ul[1]/li";

        pagelooksgood = False

        while(not pagelooksgood):

            while True:
                tabelems = driver.find_elements_by_xpath(str)
                
                if(not tabelems):
                    print("WARN: Cannot parse document properly (date selection element)")
                    print("Retrying..")
                    time.sleep(60)
                    driver.get(url)
                else:
                    break

            print("day selection elements", len(tabelems))
        
            # handle possible exception from clicking element that cannot handle it (yet)
            while True:
                try:
                    # activates the given day
                    if(tabelems):
                        tabelems[d-1].click()
                        break
                    else:
                        print("WARN: Clicking date element failed.")
                        print("Retrying..")
                    
                        time.sleep(60)
                        driver.get(url) # reloads the whole webpage..
                        tabelems = driver.find_elements_by_xpath(str)
                        
                except selenium.common.exceptions.WebDriverException:
                    print("WARN: Clicking date element failed.")
                    print("Retrying..")
                
                    time.sleep(60)
                    driver.get(url) # reloads the whole webpage..
                    tabelems = driver.find_elements_by_xpath(str)

        
            time.sleep(5) # waits for 5 seconds for the page to reload after click


            timeelems = driver.find_elements_by_xpath('//section[@class="list"]/ul[1]/li/article/span')
            nameelems = driver.find_elements_by_xpath('//section[@class="list"]/ul[1]/li/article//h3/a')

            if(not timeelems):
                print("NO TIME ELEMENTS")
            else:
                print(len(timeelems))

            if(not nameelems):
                print("NO NAME ELEMENTS")
            else:
                print(len(nameelems))
            
            
            if(not nameelems or not timeelems):
                print("WARN: Cannot parse document properly (no time or no name elems)")
                print("Retryig..")
                continue

            pagelooksgood = True

        
        L = min([len(timeelems),len(nameelems)])
        
        for i in range(0,L):
            timestr = timeelems[i].text
            namestr = nameelems[i].text

            if(not timestr or not namestr):
                continue

            timestr = timestr.strip()
            namestr = namestr.strip()

            if(timestr == "" or namestr == ""):
                continue

            match = re.search("(\d+):(\d+)", timestr)

            if(not match):
                continue # bad time element

            start_hour = int(match.group(1))
            start_min  = int(match.group(2))

            print(start_hour, start_min, namestr)
        
            rawprogramlist[d-1].append({
                "start hour" : start_hour,
                "start min"  : start_min,
                "name" : namestr })
    
        continue

    
    # processes rawprogramlist
    for d in range(1,8):
        programstart = weekstart + datetime.timedelta(days=d-1)

        index = -1

        for p in rawprogramlist[d-1]:
            index = index + 1

            start_hour = p["start hour"]
            start_min  = p["start min"]

            startprogram = programstart.replace(
                hour=start_hour,minute=start_min,second=0)

            if(d > 0 and start_hour == 0 and start_min == 0):
                # adds extra day (its 00:00 the next day)
                startprogram = startprogram + datetime.timedelta(days=1)

            # set the end time at the beginning of the next program
            
            if(index+1 < len(rawprogramlist[d-1])):
                end_hour = rawprogramlist[d-1][index+1]["start hour"]
                end_min  = rawprogramlist[d-1][index+1]["start min"]
                
                endprogram = programstart.replace(hour=end_hour, minute=end_min,
                                                  second=0)
                
                if(end_hour == 0 and end_min == 0):
                    # adds extra day (its 00:00 the next day)
                    endprogram = endprogram + datetime.timedelta(days=1)
                
            else:
                if(d < len(rawprogramlist)):
                    if(len(rawprogramlist[d]) > 0):
                        # we need to look the program start from the next day
                        endprogram = programstart.replace(
                            hour=rawprogramlist[d][0]["start hour"],
                            minute=rawprogramlist[d][0]["start min"],second=0)
                else:
                    # guess 00:00 is the program stopping time as usual (no data)
                    endprogram = programstart.replace(hour=0,minute=0,second=0)
                
                # add extra day
                endprogram = endprogram + datetime.timedelta(days=1)

            # convert times to UTC
            starttime_utc = startprogram.astimezone(pytz.utc).strftime("%Y-%m-%d %H:%M:%S +0000")
            endtime_utc = endprogram.astimezone(pytz.utc).strftime("%Y-%m-%d %H:%M:%S +0000")
            print(id, d, starttime_utc, endtime_utc, channel, language, p["name"])

            programlist[d-1].append({
                "id" : id,
                "weekday" : d,
                "start time" : starttime_utc,
                "stop time" : endtime_utc,
                "channel" : channel,
                "language" : language,
                "name" : p["name"] })

    return programlist

    
        

def get_radio3(driver, url, id, channel, language, timezone):
    driver.get(url)

    # gets the first day of the week
    datenow = datetime.datetime.now(pytz.timezone(timezone))
    weekstart = datenow - datetime.timedelta(days=datenow.weekday(),microseconds=datenow.microsecond)
    weekstart = weekstart.replace(hour=0,minute=0,second=0)

    programlist    = [[], [], [], [], [], [], []]
    rawprogramlist = [[], [], [], [], [], [], [], []]

    for d in range(1,9):
        programstart = weekstart + datetime.timedelta(days=d-1)
        datestr = programstart.strftime("%d-%m-%Y")

        print("Processing date %s from %s" % (datestr, url))

        tabelems = driver.find_elements_by_xpath('//li[starts-with(@date-to-load,"%s")]' % (datestr))

        if(not tabelems):
            print("WARN: Cannot parse document properly (date selection element)")
            continue

        # handle possible exception from clicking element that cannot handle it (yet)
        while True:
            try:
                # activates the given day
                if(tabelems):
                    tabelems[0].click()
                    break
                else:
                    time.sleep(5)
                    tabelems = driver.find_elements_by_xpath('//li[starts-with(@date-to-load,"%s")]' % (datestr))
            except selenium.common.exceptions.WebDriverException:
                time.sleep(5)
                driver.get(url) # reloads the whole webpage..
                tabelems = driver.find_elements_by_xpath('//li[starts-with(@date-to-load,"%s")]' % (datestr))

        
        time.sleep(5) # waits for 5 seconds for the page to reload after click

        programelements = driver.find_elements_by_xpath('//li[@rairadio-tooltip]')

        if(not programelements):
            counter = 0
            while(counter < 5):
                tabelems[0].click()
                time.sleep(5)
                programelements = driver.find_elements_by_xpath('//li[@rairadio-tooltip]')
                if(programelements):
                    break

                counter = counter + 1

            if(counter == 5):
                print("WARN: Cannot parse document properly (program elements)")
                continue

        
        for p in programelements:
            timeelements = p.find_elements_by_xpath('.//div[starts-with(@class,"time")]')
            if(not timeelements):
                print("WARN: Cannot parse document properly (time element)")
                continue

            start_time = timeelements[0].text.strip()

            nameelements = p.find_elements_by_xpath('.//h2')

            if(not nameelements):
                print("WARN: Cannot parse document properly (program name element)")
                continue

            name = re.sub("<\/?.+?\/?>", "", nameelements[0].text).strip()

            if(not start_time or not name):
                continue

            if(start_time == "" or name == ""):
                continue

            match = re.search("(\d+):(\d+)", start_time)

            if(not match):
                print("WARN: Cannot parse document properly (bad time format)")
                continue

            start_hour = int(match.group(1))
            start_min  = int(match.group(2))
            

            rawprogramlist[d-1].append({
                "start hour" : start_hour,
                "start min"  : start_min,
                "name" : name})


    # processes rawprogramlist
    for d in range(1,8):
        programstart = weekstart + datetime.timedelta(days=d-1)

        index = -1

        for p in rawprogramlist[d-1]:
            index = index + 1
            
            startprogram = programstart.replace(
                hour=p["start hour"],minute=p["start min"],second=0)

            # set the end time at the beginning of the next program

            if(index+1 < len(rawprogramlist[d-1])):
                endprogram = programstart.replace(
                    hour=rawprogramlist[d-1][index+1]["start hour"],
                    minute=rawprogramlist[d-1][index+1]["start min"],second=0)
            else:
                if(d < len(rawprogramlist)):
                    if(len(rawprogramlist[d]) > 0):
                        # we need to look the program start from the next day
                        endprogram = programstart.replace(
                            hour=rawprogramlist[d][0]["start hour"],
                            minute=rawprogramlist[d][0]["start min"],second=0)

                if(not endprogram):
                    # guess midnight its the program stopping time as usual (no data)
                    endprogram = programstart.replace(hour=0,minute=0,second=0)
                
                # add extra day
                endprogram = endprogram + datetime.timedelta(days=1)

            # convert times to UTC
            starttime_utc = startprogram.astimezone(pytz.utc).strftime("%Y-%m-%d %H:%M:%S +0000")
            endtime_utc = endprogram.astimezone(pytz.utc).strftime("%Y-%m-%d %H:%M:%S +0000")
            print(id, d, starttime_utc, endtime_utc, channel, language, p["name"])

            programlist[d-1].append({
                "id" : id,
                "weekday" : d,
                "start time" : starttime_utc,
                "stop time" : endtime_utc,
                "channel" : channel,
                "language" : language,
                "name" : p["name"] })

    return programlist
    
            
def get_radio2(driver, url, id, channel, language, timezone):
    driver.get(url)

    # gets the first day of the week
    datenow = datetime.datetime.now(pytz.timezone(timezone))
    weekstart = datenow - datetime.timedelta(days=datenow.weekday(),microseconds=datenow.microsecond)
    weekstart = weekstart.replace(hour=0,minute=0,second=0)

    programlist = [[], [], [], [], [], [], []];
    

    for d in range(1,8):
        tabtext = "label_tab label_tab_%d" % d

        print("Processing tab %d from %s" % (d, url))        
        
        tabelems = driver.find_elements_by_xpath('//p[starts-with(@class,"%s")]' % (tabtext))
        if(not tabelems):
            print("WARN: Cannot parse document properly (tab missing)")
            continue
        
        tabelems[0].click()

        # now we have correct program elements for the date

        programelems = driver.find_elements_by_xpath('//div[starts-with(@class, "vc_article_preview_palinsesto")]')

        # print("%d program elements found." % (len(programelems)))

        for p in programelems:

            # time information
            time_elems = p.find_elements_by_xpath('.//div[@class="text_edit vc_title_preview_palinsesto"]/p')

            if(not time_elems):
                print("WARN: Cannot parse document properly (time missing)")
                continue

            time = time_elems[0].text.strip()

            # program name
            program_elems = p.find_elements_by_xpath('.//h2[@class="titolo vc_title"]')
            if(not program_elems):
                print("WARN: Cannot parse document properly (program name missing)")
                continue

            program_name = re.sub("<\/?.+?\/?>", "" , program_elems[0].text).strip()

            # when we start getting empty elements we break out of the loop
            if(not time or not program_name):
                continue
            if(time == "" or program_name == ""):
                continue

            match = re.search(".*?(\d+):(\d+)\s*-\s*(\d+):(\d+).*$", time)

            if(not match):
                print("WARN: Cannot parse document properly (time missing)")
                continue

            start_hour = int(match.group(1))
            start_min  = int(match.group(2))
            end_hour   = int(match.group(3))
            end_min    = int(match.group(4))

            programstart = weekstart + datetime.timedelta(days=d-1)
            startprogram = programstart.replace(hour=start_hour,minute=start_min,second=0)
            endprogram   = programstart.replace(hour=end_hour,minute=end_min,second=0)
            # convert times to UTC
            starttime_utc = startprogram.astimezone(pytz.utc).strftime("%Y-%m-%d %H:%M:%S +0000")
            endtime_utc = endprogram.astimezone(pytz.utc).strftime("%Y-%m-%d %H:%M:%S +0000")

            programlist[d-1].append({
                "id" : id,
                "weekday" : d,
                "start time" : starttime_utc,
                "stop time" : endtime_utc,
                "channel" : channel,
                "language" : language,
                "name" : program_name })

    return programlist


        
def get_radio1(driver, url, id, channel, language, timezone):
    driver.get(url)
    
    # get urls of each day from the front page
    dayurls = []
    elem = driver.find_element_by_xpath('//div[@class="article-list"]/ul')
    links = elem.find_elements_by_xpath("./li/span/a")
    for l in links:
        dayurls.append(l.get_attribute("href"))

    programlist = [[], [], [], [], [], [], []];
    index = -1
    
    for d in dayurls:
        print(d)
        driver.get(d)
        index = index + 1
    
        # gets date information
        hasdate = False
        match = re.search(".*?radio-(\d+)", d)
        if(match):
            datestring = match.group(1)
            if(len(datestring) == 8):
                year = int(datestring[0:4])
                month  = int(datestring[4:6])
                day = int(datestring[6:8])
                hasdate = True


        if(not hasdate):
            print("WARN: Skipping URL badly formated data")
            continue

    
        programs = driver.find_elements_by_class_name("news-preview-defaults")    

        for p in programs:
            starttime = None
            endtime = None
                        
            hourelem = p.find_elements_by_xpath('.//span[@class="hour"]')
            if(hourelem):
                hours = hourelem[0].text
                match = re.search(".*?dalle (.+?) alle (.+?)$", hours)
                if(match):
                    start_hour_str = match.group(1)
                    end_hour_str = match.group(2)
                    
                    start_hour_list = re.split(":", start_hour_str)
                    end_hour_list = re.split(":", end_hour_str)
                        
                    if(len(start_hour_list) == 2):
                        start_hour = int(start_hour_list[0])
                        start_min  = int(start_hour_list[1])
                    else:
                        start_hour = int(start_hour_str)
                        start_min  = 0
                            
                    if(len(end_hour_list) == 2):
                        end_hour = int(end_hour_list[0])
                        end_min  = int(end_hour_list[1])
                    else:
                        end_hour = int(end_hour_str)
                        end_min  = 0
                                
                    starttime = pytz.timezone(timezone).localize(datetime.datetime(year, month, day, start_hour, start_min))
                    endtime = pytz.timezone(timezone).localize(datetime.datetime(year, month, day, end_hour, end_min))
                                        
                else:
                    print("WARN: Error in parsing no time element (skipping)")

            else:
                print("WARN: Error in parsing no time element (skipping)")
                        
            name = None
            nameelem = p.find_elements_by_xpath("(.//span)[2]")
            if(nameelem):
                name = nameelem[0].text.strip()
            else:
                print("WARN: Error in parsing no program name element (skipping)")
                
            if(not name or not starttime or not endtime):
                continue # skip this program element
        

            if(starttime):
                starttime_utc = starttime.astimezone(pytz.utc).strftime("%Y-%m-%d %H:%M:%S +0000")
            else:
                starttime_utc = "NO TIME DATA"

            if(endtime):
                endtime_utc = endtime.astimezone(pytz.utc).strftime("%Y-%m-%d %H:%M:%S +0000")
            else:
                endtime_utc = "NO TIME DATA"

            if(not name):
                name = "NO NAME DATA"

            programlist[index].append({
                "id" : id,
                "weekday" : index+1,
                "start time" : starttime_utc,
                "stop time" : endtime_utc,
                "channel" : channel,
                "language" : language,
                "name" : name })

    return programlist
              

if __name__ == '__main__':
    main()
