from bs4 import BeautifulSoup as bs
import csv
import itertools
import requests
import time

# ------------------------FILL THIS-----------------------------
# FUNCTION TO RETURN A PROXY
# FILL THIS


def get_proxy_dict():
    # THIS VARIABLE SHOULD HOLD THE PROXY CONFIGURATION
    proxy_dict = {
        'http': 'http://103.20.81.38:45680',
        'http':'http://177.11.140.134:58720'}

    # DO SOMETHING HERE TO GET A PROXY CONFIGURATION
    # FROM A PROXY POOL
    # AN EXAMPLE IS GIVEN HERE
    prox = requests.get('https://api.getproxylist.com/proxy?protocol[]=http&anonimity[]=high%20anonimity&anonimity[]=anonymous')
    content = prox.json()
    print(content)
    proxy_dict = {"http":  content['protocol'] + "://" + content['ip'] + ":" + str(content['port'])}

    # RETURN THIS VARIABLE TO BE USED IN ALL REQUESTS
    return proxy_dict
# ----------------------------THANK YOU------------------------


url = 'https://www.yelp.com/search?'
cflt_list = ['contractors', 'electricians', 'homecleaning',
             'hvac', 'landscaping', 'locksmiths', 'movers', 'plumbing',
             'burgers', 'japanese', 'chinese', 'mexican', 'italian', 'thai'
             'autorepair', 'car_dealers', 'auto_dealing', 'oilchange',
             'bodyshops', 'parking', 'carwash', 'towing',
             'bars', 'nightlife', 'hair', 'massage', 'gyms', 'shopping']

locations = ['London', 'Leeds', 'Manchester', 'Edinburgh', 'Bristol',
             'Newyork', 'Losangeles', 'Chicago', 'Houston', 'Phoenix']

start = []
TOTAL_COUNT = 1
for i in range(0, 991, 10):
    start.append(i)


for crossprod_iter in itertools.product('London', cflt_list, start, repeat=1):
    (loc, cat, pg_num) = crossprod_iter
    params = {"cflt": cat, "find_loc": loc, "start": pg_num}
    if TOTAL_COUNT % 990 == 1:
        proxy_dict = get_proxy_dict()

    response = requests.get(url, params=params, proxies=proxy_dict)
    print(crossprod_iter)
    print(response.headers)
    time.sleep(1)
    soup = bs(response.content, "lxml")
    for j in soup.find_all("a", attrs={"class": "biz-name js-analytics-click"}):
        # print("https://yelp.com" + j['href'])
        if TOTAL_COUNT % 8 == 1:
            proxy_dict = get_proxy_dict()
        print(proxy_dict)
        resp = requests.get("https://yelp.com" + j['href'], proxies=proxy_dict)
        time.sleep(4)
        s = bs(resp.content, "lxml")
        try:
            bussiness_name = s.find("h1").text.strip()
        except:
            bussiness_name = "Bussiness name not found"
        try:
            address = s.find("address").get_text("\n").strip()
        except:
            address = "Address Not found"
        try:
            actual_site = s.find("span", attrs={"class": "biz-website js-biz-website js-add-url-tagging"}).a.get_text("\n")
        except:
            actual_site = "Actual site not found"
        attributes = []
        try:
            for i in s.find_all("dl"):
                attributes.append((i.dt.text.strip(), i.dd.text.strip()))
        except:
            print("attributes not found/error occurred")

        dict = {"Bussiness Name": bussiness_name, "Address": address,
                "Yelp WebSite": "https://yelp.com" + j['href'],
                "Actual WebSite": actual_site}
        for i in attributes:
            (a, b) = i
            dict[a] = i
        print(str(TOTAL_COUNT) + "*"*50)
        print(dict)
        print("*"*50)
        TOTAL_COUNT += 1
        with open(loc+".csv", "a") as file:
            w = csv.writer(file)
            w.writerow(dict.values())
        file.close()
