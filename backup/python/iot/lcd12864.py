# -*- coding: utf-8 -*-
import spidev
import time
 
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
                print("test start")
                print(c)
                print("End")
                bytes.append(ord(c) & 0xf0)
                bytes.append((ord(c) << 4) & 0xf0)
            elif len(b) == 2:
                print("test start2")
                print(c)
                print("End")
                bytes.append(ord(b[0]) & 0xf0)
                bytes.append((ord(b[0]) << 4) & 0xf0)
                bytes.append(ord(b[1]) & 0xf0)
                bytes.append((ord(b[1]) << 4) & 0xf0)
        self.spi.xfer2(bytes)
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
         
    def display(self, row, col, str):
        self.position(row, col)
        self.writeData(str)
 
while (True): 
    lcd = LCD12864B(0, 0)
    lcd.reset()
    #lcd.display(0, 0, "I want to go Home")
    #time.sleep( 5 )
    lcd.display(0, 0, u"溫度:20.9 濕度:50.1 ")
    time.sleep( 5 )
    lcd.display(0, 0, u"別人沒比較厲害")
    time.sleep( 5 )
    lcd.display(1, 0, u'我們沒比較差')
    time.sleep( 5 )
    lcd.display(2, 0, u"只是別人先學")
    time.sleep( 5 )
    lcd.display(3, 0, u"我們一樣也完成.")
    time.sleep( 5 )
    lcd.reset()
    lcd.close()
