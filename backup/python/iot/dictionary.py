# encoding: utf-8
import sys

sys.path.append('/home/pi/user_project/python/iot/lib')

import Adafruit_DHT

sensor = Adafruit_DHT.DHT22

pin = 'P8_11'


humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)


passwd={'Mars':00000,'Mark':56680}
passwd['Happy']=9999     
passwd['Smile']=123456

del passwd['Mars']
passwd['Mark']=passwd['Mark']+1

print (passwd)
print (passwd.keys())
print (passwd.get('Tony')) 
