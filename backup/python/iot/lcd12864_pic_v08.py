# -*- coding: utf-8 -*-
#import urllib2
import datetime
import httplib
import urllib
import RPi.GPIO as GPIO 
import spidev
import sys
import Adafruit_DHT
import time
import os
import ntplib
from time import ctime

#Vairiable Declaration
humidity1 = 0.0
temperature1 = 0.0
temperature2 = 0.0
humidity2 = 0.0

#Sensor Constant Declaration
VALUE_HUMIDITY_MAX = 100.0
VALUE_HUMIDITY_MIN = 30.0
VALUE_TEMPERATURE_MAX = 40.0
VALUE_TEMPERATURE_MIN = 14.0
OFFSET_HUMIDITY1 = -16.5
OFFSET_HUMIDITY2 = -16.5
OFFSET_TEMPERATURE1 = 0.0
OFFSET_TEMPERATURE2 =0.0


webConnTimeout = 10#sec
uploadPeriod = 1#min
errorDataReport = 99
uploadTime = ""

#Reset LCD12864 when program start up
LCD12864_Reset_Pin = 11


#WebServer Config
WebServer_IP = "172.27.10.92"
WebAPURL =  "/TH_MON/TH_SAVE.PHP?"
ROOM_ID = "L1"
NTPServer = '172.27.16.253'

#Sensor Config
sensor_AM2302_01 = Adafruit_DHT.AM2302
sensor_AM2302_01_pin = 27
sensor_AM2302_02 = Adafruit_DHT.AM2302
sensor_AM2302_02_pin = 22

#HannStar Logo
hannstar=[
           0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
      0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
      0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x0F,
      0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFE,0xFC,
      0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x1F,
      0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFE,0xFC,
      0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x1F,
      0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFE,0xFC,
      0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x1F,
      0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFE,0xFC,
      0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x1F,
      0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFE,0xFC,
      0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x1F,
      0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFE,0xFC,
      0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x1F,
      0xFF,0xFF,0xFF,0xFF,0xFF,0xDF,0xFF,0xFC,
      0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x1F,
      0xFF,0xFF,0xFF,0xFF,0xFF,0xDF,0x83,0x80,
      0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x1F,
      0xFF,0xFF,0xFF,0xFF,0xFF,0xDF,0xFF,0xFC,
      0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x1F,
      0xFF,0xFF,0xFF,0xFF,0xFE,0x03,0xFE,0xFC,
      0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x1F,
      0xFF,0xFF,0xFF,0xFF,0xFF,0xDF,0xFE,0xFC,
      0x1E,0x03,0x80,0x00,0x00,0x00,0x00,0x1E,
      0x03,0xFF,0xFF,0xFF,0xFF,0xDF,0xFE,0xFC,
      0x1E,0x07,0x80,0x00,0x00,0x00,0x00,0x18,
      0x00,0xF8,0xFF,0xFF,0xFF,0xDF,0xFE,0xFC,
      0x1E,0x07,0x80,0x00,0x00,0x00,0x00,0x08,
      0x00,0x70,0xFF,0xFF,0xFF,0xFF,0x7E,0xFC,
      0x1E,0x07,0x80,0x00,0x00,0x00,0x00,0x00,
      0xF8,0x70,0xFF,0xFF,0xFF,0xFF,0x7F,0xFC,
      0x1E,0x07,0x80,0x00,0x00,0x00,0x00,0x01,
      0xFC,0x30,0xFF,0xFF,0xFF,0xFF,0x7F,0xFC,
      0x1E,0x07,0x87,0xF8,0xF7,0xE3,0xBF,0x01,
      0xFC,0x20,0x3C,0x07,0x88,0xFC,0x1F,0xFC,
      0x1E,0x07,0x8F,0xFC,0xFF,0xF3,0xFF,0x80,
      0xFF,0xE0,0x38,0x03,0x80,0xFF,0x7F,0xFC,
      0x1F,0xFF,0x9F,0xFC,0xFF,0xF3,0xFF,0xC0,
      0x1F,0xE0,0x30,0x01,0x80,0xFF,0x7F,0xFC,
      0x1F,0xFF,0x9E,0x1C,0xF0,0xF3,0xC3,0xC8,
      0x01,0xF0,0xF1,0xE1,0x83,0xFF,0x7F,0xFC,
      0x1F,0xFF,0x80,0x1C,0xF0,0x73,0xC3,0xCC,
      0x00,0x70,0xFF,0xE1,0x87,0xFF,0xFF,0xFC,
      0x1E,0x07,0x81,0xFC,0xF0,0x73,0xC3,0xCF,
      0x00,0x30,0xFF,0x01,0x8F,0xFF,0xFF,0xFC,
      0x1E,0x07,0x8F,0xFC,0xF0,0x73,0x83,0xCF,
      0xF0,0x30,0xF8,0x01,0x8F,0xFF,0xFF,0xFC,
      0x1E,0x07,0x9F,0xBC,0xF0,0x73,0xC3,0xCF,
      0xFC,0x30,0xF0,0x01,0x8F,0xFF,0xFF,0xFC,
      0x1E,0x07,0x9C,0x3C,0xF0,0x73,0xC3,0xC1,
      0xFE,0x30,0xE0,0xF1,0x8F,0xFF,0xFF,0xFC,
      0x1E,0x07,0x9C,0x3C,0xF0,0x73,0xC3,0xC0,
      0xFC,0x30,0xE1,0xE1,0x8F,0xFF,0xFF,0xFC,
      0x1E,0x07,0x9C,0x7C,0xF0,0x73,0xC3,0xC0,
      0x78,0x30,0xE1,0xE1,0x8F,0xFF,0xFF,0xFC,
      0x1E,0x07,0x9F,0xFC,0xF0,0x73,0x83,0xC0,
      0x00,0x78,0x20,0x01,0x8F,0xFF,0xFF,0xFC,
      0x1E,0x07,0x9F,0xFE,0xF0,0x73,0xC3,0xC8,
      0x00,0xF8,0x30,0x01,0x8F,0xFF,0xFF,0xFC,
      0x1C,0x03,0x87,0x9E,0xE0,0x73,0x81,0xCC,
      0x00,0xF8,0x10,0x00,0x0F,0xFF,0xFF,0xFC,
      0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
      0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
      0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
      0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
      0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
      0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
      0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
      0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
      0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
      0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
      0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
      0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
      0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
      0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
      0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
      0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
      0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
      0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
      0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
      0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
      0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
      0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
      0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
      0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
      0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
      0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
      0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
      0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
      0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
      0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
      0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
      0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
      0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
      0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
      0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
      0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
      0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
      0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
      0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
      0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
      0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
      0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
      0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
      0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
      0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
      0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
      0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
      0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
      0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
      0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
      0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
      0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
      0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
      0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
      0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
      0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
      0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
      0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
      0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
      0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
      0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
      0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
      0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
      0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
      0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
      0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00
      ]


########Class Area########################
#LCD12864 Driver Class
class LCD12864B:
    def __init__(self, port, cs):
        self.spi = spidev.SpiDev()
        self.spi.open(port, cs)
        self.spi.cshigh = True
         
    def writeCommand(self, cmd):
        self.spi.xfer2([0xf8, cmd & 0xf0, (cmd << 4) & 0xf0])
        time.sleep(0.001)
         
    def writeByte(self, byte):
        self.spi.xfer2([0xfa, byte & 0xf0, (byte << 4) & 0xf0])
         
    def writeData(self, data):
        bytes = [0xfa]
        for c in data:
            b = c.encode('big5')
            if len(b) == 1:
                bytes.append(ord(c) & 0xf0)
                bytes.append((ord(c) << 4) & 0xf0)
            elif len(b) == 2:
                bytes.append(ord(b[0]) & 0xf0)
                bytes.append((ord(b[0]) << 4) & 0xf0)
                bytes.append(ord(b[1]) & 0xf0)
                bytes.append((ord(b[1]) << 4) & 0xf0)
        self.spi.xfer2(bytes)
        time.sleep(0.001)

    def writeLogoData(self,data):
        #print("data")
        #print(data)
        #d3 = long(data)
        #print("data3")
        #print(d3)
        d4=[]
        d4.append(bytes(data))
        #print("data4")
        #print(d4)
        #self.spi.xfer2(d4)
        self.writeByte(data)
        time.sleep(0.001)

    def reset(self):
        self.writeCommand(0x30)
        self.writeCommand(0x0c)
        self.writeCommand(0x01)
        self.writeCommand(0x06)
         
    def close(self):
        self.spi.close()
         
    def position(self, row, col):
        addr = {
             0: 0x80,
             1: 0x90,
             2: 0x88,
             3: 0x98,
        }
        ac = addr.get(row) + col
        self.writeCommand(ac)
         
    def displayUnicode(self, row, col, data):
        self.position(row, col)
        self.writeLogoData(data)
        
    def display(self, row, col, str):
        self.position(row, col)
        self.writeData(str)    

    def displayLogo(self,data):
        #print(data)
        for ygroup in range(0,64):
            if(ygroup<32):
                x=0x80;
                y=ygroup+0x80
            else:
                x=0x88;
                y=ygroup-32+0x80        
            self.writeCommand(0x34)
            self.writeCommand(y)           
            self.writeCommand(x)  
            self.writeCommand(0x30)
            tmp=ygroup*16
            for i in range(0,16):
                #print(hannstar[tmp])
                temp=hannstar[tmp]
                #print("temp")
                #print(temp)
                self.writeLogoData(temp)
                tmp=tmp+1
        self.writeCommand(0x34)      
        self.writeCommand(0x36)
########Function Area End########################
        
        
########Function Area########################
#Hannstar NTP    
def getNTP():
    print "================aaaa===================="
    try:
        client = ntplib.NTPClient()
        #response = client.request('europe.pool.ntp.org', version=3)
        response = client.request(NTPServer, version=4)
        print "===================================="
        print "Offset : "+str(response.offset)
        print "Version : "+str(response.version)
        print "Date Time : "+str(ctime(response.tx_time))
        print "Leap : "+str(ntplib.leap_to_text(response.leap))
        print "Root Delay : "+str(response.root_delay)
        print "Ref Id : "+str(ntplib.ref_id_to_text(response.ref_id))
        print  str(ctime(response.tx_time))
        print  ("sudo date -s '"+str(ctime(response.tx_time))+"'")
        os.system("sudo date -s '"+str(ctime(response.tx_time))+"'")
        print "===================================="
        return "OK...",str(ntplib.leap_to_text(response.leap))
    except:
        os.system("sudo date")
        print "NTP Server Down Date Time NOT Set At The Startup"
        pass
        return "NG...",""
        
 

# LCD Hardware Reset function  
def Lcd12864_Reset():
        print("LCD Reset")
        GPIO.output(LCD12864_Reset_Pin,GPIO.LOW)  
        time.sleep(2)  
        GPIO.output(LCD12864_Reset_Pin,GPIO.HIGH)    
        return

#DataUpload to Web
def DataUpload():
    data = {}
    data['ROOM_NO'] = ROOM_ID
    data['TEMP1'] ="{0:0.1f}".format(temperature1) 
    data['TEMP2'] ="{0:0.1f}".format(temperature2) 
    data['HDY1'] = "{0:0.1f}".format(humidity1) 
    data['HDY2'] = "{0:0.1f}".format(humidity2)
    url_values = urllib.urlencode(data)
    #print (url_values)
    url=WebAPURL + url_values
    print(url)
    conn = httplib.HTTPConnection(WebServer_IP,timeout=webConnTimeout)
    try:
        print ("upload data start.")
        conn.request("GET", url)
        response = conn.getresponse()
        print (response.status, response.reason)
        conn.close()
        print ("upload data end.")
    except:
        print("Http Unexpected error:", sys.exc_info()[0])
        conn.close()
    return "uTime:"+time.strftime("%H:%M:%S", time.localtime())

#display humidity &  temperature1
def displayTH(lcd):
    displayData=[]
    
    DHT22_Disp_Msg=u"S1  溫度={0:0.1f}*C".format(temperature1)
    print(DHT22_Disp_Msg)
    displayData.append(DHT22_Disp_Msg)
    
    DHT22_Disp_Msg=u"S1  濕度={0:0.1f}%".format(humidity1)
    print(DHT22_Disp_Msg)
    displayData.append(DHT22_Disp_Msg)

    DHT22_Disp_Msg=u"S2  溫度={0:0.1f}*C".format(temperature2)
    print(DHT22_Disp_Msg)
    displayData.append(DHT22_Disp_Msg)

    DHT22_Disp_Msg=u"S2  濕度={0:0.1f}%".format(humidity2)
    print(DHT22_Disp_Msg)
    displayData.append(DHT22_Disp_Msg)

    DisplayLCD(lcd,displayData)


#AM2302_01 Read
def readS1(lcd):
    displayData=[]
    displayData.append("Data Reading...")
    DisplayLCD(lcd,displayData)
    humidity1, temperature1 = Adafruit_DHT.read_retry(sensor_AM2302_01, sensor_AM2302_01_pin)
    if temperature1  is not None and humidity1 is not None:
        if temperature1<VALUE_TEMPERATURE_MAX and temperature1>VALUE_TEMPERATURE_MIN and humidity1<VALUE_HUMIDITY_MAX and humidity1>VALUE_HUMIDITY_MIN:
            temperature1=temperature1+ OFFSET_TEMPERATURE1
            humidity1=humidity1+OFFSET_HUMIDITY1
            print('Temp1={0:0.1f}*  Humidity1={1:0.1f}%'.format(temperature1, humidity1))
            displayData.append("S01 OK")
    else:
        print('Failed to get reading. Try again!')
        displayData.append("S01 NG")
        temperature1=errorDataReport
        humidity1=errorDataReport        
    DisplayLCD(lcd,displayData)
    time.sleep(0.5)
    return humidity1, temperature1

#AM2302_02 Read
def readS2(lcd):
    displayData=[]
    displayData.append("Data Reading...")
    DisplayLCD(lcd,displayData)
    humidity2, temperature2 = Adafruit_DHT.read_retry(sensor_AM2302_02, sensor_AM2302_02_pin)
    if temperature2  is not None and humidity2 is not None:
        if temperature2<VALUE_TEMPERATURE_MAX and temperature2>VALUE_TEMPERATURE_MIN and humidity2<VALUE_HUMIDITY_MAX and humidity2>VALUE_HUMIDITY_MIN:
            temperature2=temperature2+ OFFSET_TEMPERATURE2
            humidity2=humidity2+OFFSET_HUMIDITY2
            print('Temp2={0:0.1f}*  Humidity2={1:0.1f}%'.format(temperature2, humidity2))
            displayData.append("S02 OK")
    else:
        print('Failed to get reading. Try again!')
        displayData.append("Sensor02 NG")
        temperature1=errorDataReport
        humidity1=errorDataReport        
    DisplayLCD(lcd,displayData)
    time.sleep(0.5)
    return humidity2, temperature2

#display system start
def systemStart(lcd):
    lcd.display(0, 0, u"系統開機中 ...")
    lcd.display(1, 0, "Data Reading ...")
    humidity1, temperature1 = Adafruit_DHT.read_retry(sensor_AM2302_01, sensor_AM2302_01_pin)
    if temperature1  is not None and humidity1 is not None:
        temperature1=temperature1+ OFFSET_TEMPERATURE1
        humidity1=humidity1+OFFSET_HUMIDITY1
        print('Temp1={0:0.1f}*  Humidity1={1:0.1f}%'.format(temperature1, humidity1))
        lcd.display(2, 0, "S1 OK.")
    else:
        print('Failed to get reading. Try again!')
        lcd.display(2, 0, "S1 NG.")
        temperature1=errorDataReport
        humidity1=errorDataReport

    humidity2, temperature2 = Adafruit_DHT.read_retry(sensor_AM2302_02, sensor_AM2302_02_pin)
    if temperature1  is not None and humidity1 is not None:
        temperature2=temperature2+ OFFSET_TEMPERATURE2
        humidity2=humidity2+OFFSET_HUMIDITY2
        print('Temp2={0:0.1f}*  Humidity2={1:0.1f}%'.format(temperature2, humidity2))
        lcd.display(3, 0, "S2 OK.")
    else:
        print('Failed to get reading. Try again!')
        lcd.display(3, 0, "S2 NG.")
        temperature1=errorDataReport
        humidity1=errorDataReport
    time.sleep(1)
    return humidity1, temperature1,humidity2, temperature2  

#urpose
def systemPurpose(lcd):
    displayData=[]
    displayData.append(u"**1 **房溫控")
    displayData.append(u"上傳系統....")
    DisplayLCD(lcd,displayData)
    time.sleep(2)
    
#Owner Department
def ownerDepart(lcd):
    displayData=[]
    displayData.append(u"開發單位:")
    displayData.append(u"**晶C**M")
    DisplayLCD(lcd,displayData)
    time.sleep(2)
    
#initial Finish
def initialFinish(lcd):
    displayData=[]
    displayData.append(u"工商服務結束..")
    displayData.append(u"開始監控了...")
    DisplayLCD(lcd,displayData)
    time.sleep(1)

#show Date Time
def showDateTime(lcd):
    i=0
    lcd.reset()
    lcd.display(0, 0, u"日期 -時間:")
    lcd.display(1,0,time.strftime("%Y-%m-%d ", time.localtime()) )
    lcd.display(3,0,uploadTime )
    uploadTime
    while(i<5):  
        lcd.display(2,0,time.strftime("%H:%M:%S", time.localtime()) )
        #lcd.display(3, 0, u"想睡覺..想兒子")
        time.sleep(1)
        i=i+1
        
#HannstarLogo
def HannstarLogo(lcd):
    lcd.displayLogo(hannstar)
    time.sleep(5)
    lcd.reset()

#ntp
def checkNTP(lcd):
    lcd.reset()
    lcd.display(0, 0, u"系統自動對時中..")
    checkResult1,checkResult2=getNTP()
    lcd.display(1, 0, checkResult1)
    lcd.display(2, 0, checkResult2)
    time.sleep(2)        

#Common LCD Display
def DisplayLCD(lcd,displayData):
    lcd.reset()
    for i in range(0, len(displayData)):        
        lcd.display(i, 0, displayData[i])
########Function End########################


    
    
###### Main Program Start ############################ 
#Reset LCD12864   
# to use Raspberry Pi board pin numbers
GPIO.cleanup()
GPIO.setmode(GPIO.BOARD)  
# set up GPIO output channel
GPIO.setup(LCD12864_Reset_Pin, GPIO.OUT)

#call LCD Reset Function
Lcd12864_Reset()
lcd = LCD12864B(0, 0)
lcd.reset()
#time.sleep(1)

#display Hannstar Logo
HannstarLogo(lcd)
#system Start and read sensor to check the health of sensor
humidity1, temperature1,humidity2, temperature2=systemStart(lcd)
#ntp
checkNTP(lcd)
#system purpose
systemPurpose(lcd)
#Owner Depart
ownerDepart(lcd)
#Inital finish
initialFinish(lcd)

#for switch sensor..
j=0
#for Upload period
nextReportTime=datetime.datetime.now()+datetime.timedelta(minutes=uploadPeriod)
while(True):
    #print(datetime.datetime.now())
    if (j==0):
        j=1
        print("Read S1")
        humidity1, temperature1=readS1(lcd)
    else:
        j=0
        print("Read S2")
        humidity2, temperature2=readS2(lcd)
#display current temperature & humidity
    displayTH(lcd)
#Upload Data to DB if the datetime over the setting period'
    if(datetime.datetime.now()>nextReportTime):
        nextReportTime=datetime.datetime.now()+datetime.timedelta(minutes=uploadPeriod)
        uploadTime=DataUpload()
    time.sleep(5)
    
#Display Date And Time#
    showDateTime(lcd)
    
lcd.close()
    

  
