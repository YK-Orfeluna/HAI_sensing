"""
import lxml.html
import requests as rq

target_url = "http://192.168.11.10/"
target_html = rq.get(target_url).text

root = lxml.html.fromstring(target_html)
print(root.text)
"""

txt = "sensorvalue=1023, 198"

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

print type(val1)
print val2
