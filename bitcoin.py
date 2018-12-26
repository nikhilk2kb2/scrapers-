from lbcapi import api
import hmac
import json
import urllib
import hashlib
import requests
from urllib import urlencode
from datetime import datetime

class LocalBitcoin:

    def __init__(self, debug=False):
        self.hmac_auth_key = '54d89f67a8309783caf6cbe18cb2bc4a'
        self.hmac_auth_secret = '5fec1e38df953de2f23f7394d15ceea9c98548a489b184ea02e02bd6d42d1358'
        self.debug = debug
        self.conn = api.hmac(self.hmac_auth_key, self.hmac_auth_secret)
        self.baseurl = 'https://localbitcoins.com'
        self.setData()
        self.createAd()
    


    def setData(self):
        data = requests.get('https://localbitcoins.com/sell-bitcoins-online/IN/india/.json')
        if data.json():
            rank_one_data  = data.json()['data']['ad_list'][0]['data'].copy()
            self.adData = rank_one_data
        return


    def createAd(self):
        datas = self.adData
        myData = self.conn.call('GET', '/api/myself/').json()
        try:
            username = myData['data']['username']
            account_info = self.conn.call('GET', '/api/account_info/'+ 'niklhilthakur' + '/').json()['data']
        except:
            print "Error getting username !!"
        
        vals = {
            'price_equation' : '474615.90 ',
            'lat' : datas.get('lat') or 0.0,
            'lon' : datas.get('lon') or 0.0,
            'temp_price_usd':'10000.0',
            'city': datas.get('city'), 
            'location_string' : datas.get('location_string'),
            'countrycode':datas.get('countrycode'),
            'currency': datas.get('currency'),
            'account_info':account_info,
            'bank_name':datas.get('bank_name'),
            'msg': datas.get('msg'),
            'sms_verification_required': False,
            'track_max_amount': False , 
            'require_trusted_by_advertiser': False ,
            'require_identification': False ,
            'trade_type':'ONLINE_BUY',
            'online_provider':'NATIONAL_BANK',
            'max_amount':datas.get('max_amount'),
            'min_amount':datas.get('min_amount'),
            'floating':True,
        }

        # allAds = self.conn.call('GET','/api/ads/')
        # ad_list = []

        # try:
        #     ad_list = [x['data']['ad_id'] for x in allAds.json()['data']['ad_list']]
        #     for ad in ad_list:
        #         self.conn.call('POST','/api/ad-delete/'+str(ad)+'/')

        #     print ("All Previous Ads deleted", ad_list)
        # except:
        #     pass
        
        try:
            adCreate = self.conn.call('POST', '/api/ad-create/', vals).json()
            print (adCreate['data']['message'])
        except:
            print ("Error Creating Ad!!")
        
        adList = self.conn.call('POST','/api/ads/','')

# LocalBitcoin()

import threading

def run_job():
    print("Cron Called Again!!")
    print("==================================================")

    threading.Timer(30.0, run_job).start() # called every minute
    LocalBitcoin()
    print("Cron Executed !!")
    print("==================================================")

run_job()

