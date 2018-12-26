from bs4 import BeautifulSoup as BS


structure = open('1.txt', 'rb')
soup = BS(structure, "html.parser")

investorName = soup.findAll('div', {"data-id" : "investorName"})
print investorName
exit = soup.findAll('div', {"data-id" : "exits"})
print exit
phone = soup.findAll('div', {"data-id" : "hqPhone"})
print phone
Email = soup.findAll('div', {"data-id" : "hqEmail"})
print Email
investmentsInTheLast12Months = soup.findAll('div', {"data-id" : "investmentsInTheLast12Months"})
print investmentsInTheLast12Months
yearFounded = soup.findAll('div', {"data-id" : "yearFounded"})
print yearFounded
LastInvestmentCompany = soup.findAll('div', {"data-id" : "LastInvestmentCompany"})
print LastInvestmentCompany
lastInvestmentDate = soup.findAll('div', {"data-id" : "lastInvestmentDate"})
print lastInvestmentDate
lastInvestmentSize = soup.findAll('div', {"data-id" : "lastInvestmentSize"})
print lastInvestmentSize
preferredIndustry = soup.findAll('div', {"data-id" : "preferredIndustry"})
print preferredIndustry
preferredVerticals = soup.findAll('div', {"data-id" : "preferredVerticals"})
print preferredVerticals
preferredGeography = soup.findAll('div', {"data-id" : "preferredGeography"})
print preferredGeography
preferredInvestmentTypes = soup.findAll('div', {"data-id" : "preferredInvestmentTypes"})
print preferredInvestmentTypes
preferredInvestmentAmount = soup.findAll('div', {"data-id" : "preferredInvestmentAmount"})
print preferredInvestmentAmount
preferredInvestmentAmountLow = soup.findAll('div', {"data-id" : "preferredInvestmentAmountLow"})
print preferredInvestmentAmountLow
preferredInvestmentAmountHigh = soup.findAll('div', {"data-id" : "preferredInvestmentAmountHigh"})
print preferredInvestmentAmountHigh
preferredDealSize = soup.findAll('div', {"data-id" : "preferredDealSize"})
print preferredDealSize
preferredDealSizeLow = soup.findAll('div', {"data-id" : "preferredDealSizeLow"})
print preferredDealSizeLow
preferredDealSizeHigh = soup.findAll('div', {"data-id" : "preferredDealSizeHigh"})
print preferredDealSizeHigh
preferredCompanyValuation = soup.findAll('div', {"data-id" : "preferredCompanyValuation"})
print preferredCompanyValuation
hqRegion = soup.findAll('div', {"data-id" : "hqRegion"})
print hqRegion
description = soup.findAll('div', {"data-id" : "description"})
print description
investments = soup.findAll('div', {"data-id" : "investments"})
print investments
hqLocation = soup.findAll('div', {"data-id" : "hqLocation"})
print hqLocation
hqCountry = soup.findAll('div', {"data-id" : "hqCountry"})
print hqCountry
primaryInvestorType = soup.findAll('div', {"data-id" : "primaryInvestorType"})
print primaryInvestorType
primaryContact = soup.findAll('div', {"data-id" : "primaryContact"})
print primaryContact
primaryContactTitle = soup.findAll('div', {"data-id" : "primaryContactTitle"})
print primaryContactTitle
primaryContactEmail = soup.findAll('div', {"data-id" : "primaryContactEmail"})
print primaryContactEmail
capitalUnderManagement = soup.findAll('div', {"data-id" : "capitalUnderManagement"})
print capitalUnderManagement
primaryContactPhone = soup.findAll('div', {"data-id" : "primaryContactPhone"})
print primaryContactPhone
investorWebsite = soup.findAll('div', {"data-id" : "investorWebsite"})
print investorWebsite



