import time

import lxml.html
import requests as rq

target_url = "http://192.168.11.10/"

for i in range(100) :
	target_html = rq.get(target_url).text
	root = lxml.html.fromstring(target_html)
	print(root.text)
	txt = root.text
	time.sleep(0.01)

	#txt = "sensorvalue=1023, 198"

	txt = txt.lstrip("sensorvalue=")

	val1 = ""
	val2 = ""
	flag = 1

	for i in txt :
		if i == "," :
			flag *= -1

		elif flag == 1 :
			val1 += i
		
		elif flag == -1 :
			val2 += i
	val1 = int(val1)
	val2 = int(val2)

	#print (val1)
	#print (val2)