import httplib
import urllib

data = {}
data['ROOM_NO'] = "L1234"
data['TEMP1'] = 1.0
data['TEMP2'] = 2.0
data['HDY1'] = 2.0
data['HDY2'] = 4.0
url_values = urllib.urlencode(data)
print (url_values)
#name=Somebody+Here&language=Python&location=Northampton
#url = "http://172.27.10.92/TH_MON/TH_SAVE.PHP?"
#full_url = url  + url_values
#print (full_url)
#data = urllib2.open(full_url)
#print(data)
#params = urllib.urlencode({'@ROOM_NO': 'L13', '@TEMP1': temperature1,'@TEMP2':temperature2,'@HDY1':humidity1,'@HDY2':humidity1})
headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
url="/TH_MON/TH_SAVE.PHP?" +url_values
print(url)
#conn = httplib.HTTPConnection("http://172.27.10.92/TH_MON/TH_SAVE.PHP?")
conn = httplib.HTTPConnection("172.27.10.92")
#conn.request("POST", url, url_values, headers)
conn.request("GET", url)
response = conn.getresponse()
print response.status, response.reason
conn.close()

