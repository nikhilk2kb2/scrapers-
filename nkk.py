import requests
import xlwt
import json
import time


baseUrl = 'https://api.widespreadsales.com/v1/products/store/cells/{}?category=Circuit+Breaker&subcategory=Molded+Case'
productUrl='https://api.widespreadsales.com/v1/products/store/{}'
book = xlwt.Workbook(encoding="utf-8")
sheet1 = book.add_sheet("ProductsDetails")
sheet1.write(0, 0, 'Product Name')
sheet1.write(0, 1, 'Part Number')
sheet1.write(0, 2, 'Manufacturers')
sheet1.write(0, 3, 'Sub-Category')
sheet1.write(0, 4, 'Family')
sheet1.write(0, 5, 'Type')
sheet1.write(0, 6, 'Phase')
sheet1.write(0, 7, 'Poles')
sheet1.write(0, 8, 'Volatge')
sheet1.write(0, 9, 'Amperage')
sheet1.write(0, 10, 'Connection')
sheet1.write(0, 11, 'Protection')
sheet1.write(0, 12, 'Functions')
sheet1.write(0, 13, 'AIC Rating')
sheet1.write(0, 14, 'Description')
sheet1.write(0, 15, 'New Surplus Price')
sheet1.write(0, 16, 'Re-Certified Price')
row=1

for page in range(100,1000):
    print("++++++++++++++page" + str(page) + "++++++++++++++++++++")
    try:
        response = requests.get(baseUrl.format(page)).json()
    except:
        pass
        continue

    for product in response['docs']:
        col = 0
        print("----" + product['name'] + '------')
        try:
            productDetails = requests.get(productUrl.format(product['name'])).json()
        except:
            pass
            continue
        productName = productDetails['name']
        print("PRoduct Name:" + productName)
        sheet1.write(row, col, productName)
        col = col + 1
        partNumber = productName
        print(partNumber)
        sheet1.write(row, col, partNumber)
        col += 1
        manufacturers = productDetails['manufacturers'][0]
        print(manufacturers)
        sheet1.write(row, col, manufacturers)
        col += 1
        subcategory = productDetails['subcategory']
        print(subcategory)
        sheet1.write(row, col, subcategory)
        col += 1
        family = productDetails['family']
        print(family)
        sheet1.write(row, col, family)
        col += 1
        type = productDetails['type']
        print(type)
        sheet1.write(row, col, type)
        col += 1
        phase = productDetails['specs']['Phase']
        print(phase)
        sheet1.write(row, col, phase)
        col += 1
        poles = productDetails['specs']['Poles']
        print(poles)
        sheet1.write(row, col, poles)
        col += 1
        voltage = productDetails['specs']['Voltage']
        print(voltage)
        sheet1.write(row, col, voltage)
        col += 1
        try:
            amperage = productDetails['specs']['Amperage']
        except:
            amperage = ''
            pass
        print(amperage)
        sheet1.write(row, col, amperage)
        col += 1
        try:
            connection = productDetails['specs']['Connection']
        except:
            connection = ''
            pass
        print(connection)
        sheet1.write(row, col, connection)
        col += 1
        try:
            protection = productDetails['specs']['Protection']
        except KeyError:

            pass
            protection = 'None'
        print(protection)
        sheet1.write(row, col, protection)
        col += 1
        try:
            functions = productDetails['specs']['Functions']
        except:
            functions = ''
            pass
        print(functions)
        sheet1.write(row, col, functions)
        col += 1
        try:
            ac = productDetails['specs']['AIC Rating']
        except:
            ac = ''
            pass
        print(ac)
        sheet1.write(row, col, ac)
        col += 1
        try:
            description = productDetails['displayDescription']
        except:
            description = ''
            pass

        description = description.split(',', 1)[1]
        print(description)
        sheet1.write(row, col, description)
        col += 1
        try:
            new_surplus_price = productDetails['newSurplus']['stores']['widespread']['price']
        except:
            new_surplus_price = '0'
        print("New surplus price" + str(new_surplus_price))
        sheet1.write(row, col, new_surplus_price)
        col += 1
        try:
            re_certified_price = productDetails['refurbished']['stores']['widespread']['price']
        except:
            re_certified_price = '0'
        print("Re-certified price" + str(re_certified_price))
        sheet1.write(row, col, re_certified_price)
        print('=======================================================')
        row += 1
output_file = ' FILE-0 Products Scrapped Data at ' + str(time.strftime("%m-%d-%YT%H-%M-%S")) + '.xls'
book.save(output_file)
print("Search Results Saved To File - ", output_file)


    
