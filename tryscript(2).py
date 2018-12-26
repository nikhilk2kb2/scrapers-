import pandas as pd
import requests
import time
from bs4 import BeautifulSoup
import urllib
from lxml.html import fromstring
import requests
from itertools import cycle
from lxml.html import fromstring

#Currently script scrapes all the results for the url with different pages
#"https://www.walmart.com/browse/home-improvement/electrical/1072864_1067619?povid=1072864+%7C+2018-05-02+%7C+Flyout_Electrical"
#and proxy is changed


class Product:
    def __init__(self,url,proxy):
        try:
            self.myRequest=requests.get(url,proxies={"http": proxy, "https": proxy})
        except Exception as E:
            print(E)

        self.source_code=self.myRequest.text.encode("utf-8")
        try:
            self.generalInfoStartIndex=self.source_code.index('"modules"')
        except ValueError:
            print("error in url ",url)
            raise Exception("skipping")
        open=0
        self.generalInfo="Not found"
        got_once=False
        for i in range(self.generalInfoStartIndex,len(self.source_code)):
            if self.source_code[i]=="{":
                got_once=True
                open+=1
            elif self.source_code[i]=="}":
                open-=1

            if got_once and open==0:
                # print(i)
                self.generalInfo = self.source_code[self.generalInfoStartIndex:i+1]
                break
        self.generalInfo=self.generalInfo.replace("false",'False')
        self.generalInfo=self.generalInfo.replace("true", 'True')
        self.midasContext=self.get_midasContext()

    def get_general_info(self):
        return eval("{"+self.generalInfo+"}")


    def get_ingredients(self):
        return self.get_general_info()["modules"]["Ingredients"]["ingredients"]["values"]


    def get_directions(self):
        first_key=self.get_general_info()["modules"]["Directions"].keys()[0]
        return self.get_general_info()["modules"]["Directions"][first_key]["values"]

    def get_short_description(self):
        first_key = self.get_general_info()["modules"]["ShortDescription"].keys()[0]
        return self.get_general_info()["modules"]["ShortDescription"]["product_short_description"]["values"][0].replace("<p>","").replace("</p>","\n").replace("<b>","'").replace("</b>","'")

    def get_indications(self):
        first_key = self.get_general_info()["modules"]["Indications"].keys()[0]
        return self.get_general_info()["modules"]["Indications"]["animal_health_concern"]["values"]

    def get_long_description(self):
        first_key = self.get_general_info()["modules"]["LongDescription"].keys()[0]
        return self.get_general_info()["modules"]["LongDescription"]["product_long_description"]["values"][0].replace("<ul>","\n").replace("</ul>","").replace("<li>","\n*").replace("</li>","").replace("<br />","").replace("<b>","")


    def get_specifications(self):
        list_of_specifications=self.get_general_info()["modules"]["Specifications"]["specifications"]["values"][0]
        empty_dict={}
        for j in range(len(list_of_specifications)):
            empty_dict[list_of_specifications[j].keys()[0]]=list_of_specifications[j][list_of_specifications[j].keys()[0]]["displayValue"]
        return empty_dict



    def get_midasContext(self):
        self.start = self.source_code.index('"midasContext"')
        open = 0
        got_once = False
        self.midasContext=""
        for i in range(self.start, len(self.source_code)):
            if self.source_code[i] == "{":
                got_once = True
                open += 1
            elif self.source_code[i] == "}":
                open -= 1

            if got_once and open == 0:
                # print(i)
                self.midasContext = self.source_code[self.start:i + 1]
                break

        self.midasContext = self.midasContext.replace("false", '"False"')
        self.midasContext = self.midasContext.replace("true", '"True"')
        return eval("{"+self.midasContext+"}")


    def get_price(self):
        return "$"+str(self.midasContext["midasContext"]["price"])

    def get_brand(self):
        return self.midasContext["midasContext"]["brand"]


def get_proxies():
    url = 'https://free-proxy-list.net/'
    response = requests.get(url)
    parser = fromstring(response.text)
    proxies = set()
    for i in parser.xpath('//tbody/tr')[:10]:
        if i.xpath('.//td[7][contains(text(),"yes")]'):
            proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
            proxies.add(proxy)
    return proxies

def extract_product_details(url,proxy):
    p=Product(url,proxy)
    request_page=p.myRequest
    soup=BeautifulSoup(request_page.text)
    product_title=""
    walmart_no=""
    shippingFullfillmentSection=""
    pickupFullfillmentSection=""
    aboutthisShortDesciption=""
    ingredients=""
    specifications=""
    brand=""
    directions=""
    longDescription=""
    price=""
    indications=""
    try:
        product_title=soup.find_all("div",class_="ProductTitle")[0].text
    except IndexError:
        pass
    try:
        walmart_no=soup.select(".wm-item-number")[0].text
    except IndexError:
        pass

    try:
        shippingFullfillmentSection=soup.select(".prod-shippingMessage")[0].text
    except IndexError:
        pass

    try:
        pickupFullfillmentSection=soup.select(".prod-pickupMessage")[0].text
    except IndexError:
        pass

    try:
        aboutthisShortDesciption=soup.select(".about-desc")[0].text
    except IndexError:
        pass

    try:
        ingredients=p.get_ingredients()
    except KeyError:
        pass

    try:
        specifications=p.get_specifications()
    except KeyError:
        pass

    try:
        brand=p.get_brand()
    except KeyError:
        pass

    try:
        directions=p.get_directions()
    except KeyError:
        pass

    try:
        longDescription=p.get_long_description()
    except KeyError:
        pass

    try:
        price=p.get_price()
    except KeyError:
        pass

    try:
        indications = p.get_indications()
    except KeyError:
        pass

    data={
        "product_title":product_title,
        "walmart_no":walmart_no,
        "shippingFullfillmentSection":shippingFullfillmentSection,
        "pickupFullfillmentSection":pickupFullfillmentSection,
        "aboutthisShortDesciption":aboutthisShortDesciption,
        "ingredients":ingredients,
        "specifications":specifications,
        "brand":brand,
        "directions":directions,
        "longDescription":longDescription,
        "price":price,
        "indications":indications

    }
    return data


proxies = get_proxies()
proxy_pool = cycle(proxies)

BASE_URL="https://www.walmart.com"


i=1
proxy=next(proxy_pool)
url="https://www.walmart.com/browse/home-improvement/electrical/1072864_1067619?povid=1072864+%7C+2018-05-02+%7C+Flyout_Electrical"+"&page="+str(i)

while True:
    try: #if any exception occured proxies are re fetched
        x=requests.get(url,proxies={"http": proxy, "https": proxy})
        break
    except:
        proxy_pool=cycle(get_proxies())
        proxy=next(proxy_pool)
        continue


soup=BeautifulSoup(x.content)
paginator_list=soup.find_all("ul",{"class":"paginator-list"})
total_no_of_pages=paginator_list[0].find_all("li")[-1].text
ALL_PRODUCT_URLS=[]

for i in range(1,int(total_no_of_pages)+1):
    print("getting data from page no ",i)
    proxy=next(proxy_pool)
    url = "https://www.walmart.com/browse/home-improvement/electrical/1072864_1067619?povid=1072864+%7C+2018-05-02+%7C+Flyout_Electrical"+"&page="+str(i)
    while True:
        try:
            x = requests.get(url, proxies={"http": proxy, "https": proxy})
            print("current page request completed")
            break
        except Exception as E: #in case of error in requesting proxies are refetched
            print(E,"while searching paginator page")
            proxy_pool = cycle(get_proxies())
            proxy = next(proxy_pool)
            continue

    soup = BeautifulSoup(x.content)
    all_items_on_page=soup.find_all("a",{"class":"product-title-link"})
    for item in all_items_on_page:
        product_url=BASE_URL+item.get("href")
        product_title=item.text
        ALL_PRODUCT_URLS.append(product_url)


print(ALL_PRODUCT_URLS)
print("Total no of products are ",ALL_PRODUCT_URLS)


list_of_data=[]
count=0
for url in ALL_PRODUCT_URLS:
    count+=1
    print("collecting product",count)
    try:
        if int(time.time()) % 5 == 0:
            proxy_pool=cycle(get_proxies())

        proxy=next(proxy_pool)
        detail = extract_product_details(url,proxy)
        detail["url"]=url
        list_of_data.append(detail)
    except Exception as E:
        print(E)

dataframe=pd.DataFrame(list_of_data)
dataframe.to_excel("tryscript1.xlsx")
