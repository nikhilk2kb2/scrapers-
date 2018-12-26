# -*- coding: utf-8 -*-
import os
import requests

#generate random integers from 1L to 99999
for index in range(900000, 1000000):
	url = 'https://www.e-churchbulletins.com/bulletins/%s.pdf' % (index)
	print "Trying  %s " % (url)
	#Try if the url is available 
	try: 
		response = requests.get(url, stream=True)
		if response.status_code == 200:

			script_path = os.getcwd()
			
			with open(script_path+'/'+str(index)+'.pdf', 'wb') as fd:
			    fd.write(response.content)
			print "Succesfully downloaded - %s" %(url)
	except:
		print "Not Found " , url
		pass

print "Scrapping Completed !!!"

# return
