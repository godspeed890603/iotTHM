# -*- coding: utf-8 -*-
import spidev
import sys
import Adafruit_DHT
import time
import os
import ntplib
from time import ctime

#Vairiable Declaration
humidity1=0.0
temperature1=0.0
temperature2=0.0
humidity2=0.0


sensor_AM2302_01 = Adafruit_DHT.AM2302
sensor_AM2302_01_pin = 27
sensor_AM2302_02 = Adafruit_DHT.AM2302
sensor_AM2302_02_pin = 22
#humidity1, temperature1 = Adafruit_DHT.read_retry(sensor_AM2302_01, sensor_AM2302_01_pin)
#humidity2, temperature2 = Adafruit_DHT.read_retry(sensor_AM2302_02, sensor_AM2302_02_pin)


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

#Variable Declaration End


# Class Declaration
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
        print(data)
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
        
#Class Declaration End
def getDHT22_01():
    lcd = LCD12864B(0, 0)
    time.sleep(4)
    lcd.reset()
    DHT22_Disp_Msg='Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(35, 50)
    lcd.display(0, 0, DHT22_Disp_Msg)
    lcd.close()

    
def getNTP():
    print "================aaaa===================="
    try:
        client = ntplib.NTPClient()
        #response = client.request('europe.pool.ntp.org', version=3)
        response = client.request('172.27.16.253', version=4)
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
    except:
        os.system("sudo date")
        print "NTP Server Down Date Time NOT Set At The Startup"
        pass    
 

lcd = LCD12864B(0, 0)
time.sleep(4)
lcd.reset()
lcd.display(0, 0, u"系統開機中......")
humidity1, temperature1 = Adafruit_DHT.read_retry(sensor_AM2302_01, sensor_AM2302_01_pin)
humidity2, temperature2 = Adafruit_DHT.read_retry(sensor_AM2302_02, sensor_AM2302_02_pin)
time.sleep(3)

lcd.reset()
lcd.display(0, 0, u"系統自動對時中..")
getNTP()
time.sleep(3)

lcd.reset()
lcd.displayLogo(hannstar)
time.sleep(5)
lcd.reset()

lcd.display(0, 0, u"**1 **房溫控")
lcd.display(1, 0, u"上傳系統....")
time.sleep(5)
lcd.reset()

lcd.display(0, 0, u"開發單位:")
lcd.display(1, 0, u"**晶C**M")
time.sleep(5)
lcd.reset()

lcd.display(0, 0, u"工商服務結束..")
lcd.display(1, 0, u"開始監控了...")

#humidity1, temperature1 = Adafruit_DHT.read_retry(sensor_AM2302_01, sensor_AM2302_01_pin)
#humidity2, temperature2 = Adafruit_DHT.read_retry(sensor_AM2302_02, sensor_AM2302_02_pin)

j=0
while(True):
    if (j==0):
        j=1
        humidity1, temperature1 = Adafruit_DHT.read_retry(sensor_AM2302_01, sensor_AM2302_01_pin)
        if temperature1  is not None and humidity1 is not None:
            print('Temp1={0:0.1f}*  Humidity1={0:0.1f}%'.format(temperature1, humidity1))
        else:
            print('Failed to get reading. Try again!')
    else:
        j=0
        humidity2, temperature2 = Adafruit_DHT.read_retry(sensor_AM2302_02, sensor_AM2302_02_pin)
        if temperature1  is not None and humidity1 is not None:
            print('Temp2={0:0.1f}*  Humidity2={0:0.1f}%'.format(temperature2, humidity2))
        else:
            print('Failed to get reading. Try again!')

    print(j)

    lcd.reset()
    DHT22_Disp_Msg=u"S1  溫度={0:0.1f}*C".format(temperature1)
    print(DHT22_Disp_Msg)
    lcd.display(0, 0, DHT22_Disp_Msg)

    DHT22_Disp_Msg1=u"S1  濕度={0:0.1f}%".format(humidity1)
    print(DHT22_Disp_Msg1)
    lcd.display(1, 0, DHT22_Disp_Msg1)

    DHT22_Disp_Msg=u"S2  溫度={0:0.1f}*C".format(temperature2)
    print(DHT22_Disp_Msg)
    lcd.display(2, 0, DHT22_Disp_Msg)

    DHT22_Disp_Msg=u"S2  濕度={0:0.1f}%".format(humidity2)
    print(DHT22_Disp_Msg)
    lcd.display(3, 0, DHT22_Disp_Msg)
    time.sleep(3)
    i=0
    
    lcd.reset()
    lcd.display(0, 0, u"日期 -時間:")
    lcd.display(1,0,time.strftime("%Y-%m-%d ", time.localtime()) )
    while(i<5):  
        lcd.display(2,0,time.strftime("%H:%M:%S", time.localtime()) )
        lcd.display(3, 0, u"想睡覺..想兒子")
        time.sleep(1)
        i=i+1


lcd.close()
    

  
