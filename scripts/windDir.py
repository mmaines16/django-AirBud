#!/usr/bin/python
import os
import time
import random
import redis
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
import Queue
import math


## Software SPI Setup
#CLK  = 18
#MISO = 23
#MOSI = 24
#CS   = 25
#mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)

#HARDWARE SPI
SPI_PORT = 0
SPI_DEVICE = 0
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))

store = redis.StrictRedis(host='localhost', port=6379, db=0)

windDirQueue = Queue.Queue(maxsize=20)

allowableDifference = 15

def findAVGandVariable(windDir):
        global windDirQueue
        totalxComponents = 0
        totalyComponents = 0
        leftmostValue = 0
        rightmostValue = 0
        if(windDirQueue.full()):
                windDirQueue.get()
        windDirQueue.put(windDir)
        if(windDirQueue.full()):
                i = 0
                lastReading = int(store.get('windDir'))
                leftmostValue = lastReading
                rightmostValue = lastReading
                
                while(i < 20):
                        value = windDirQueue.get()
                        print value
                        if(abs(lastReading - value) > allowableDifference):
                                if(abs(lastReading - value) > 180):
                                        if(abs(lastReading - value - 360) > allowableDifference):
                                                if(lastReading < 360 and lastReading > 180):
                                                        if((value + 360 - lastReading) > (rightmostValue - lastReading)):
                                                                rightmostValue = value + 360
                                                if(lastReading < 180):
                                                        if(leftmostValue < 180):
                                                                if((lastReading + 360 - value) > (lastReading - leftmostValue)):
                                                                        leftmostValue = value
                                                        if(leftmostValue > 180):
                                                                if(value > 180):
                                                                        if((lastReading + 360 - value) > (lastReading + 360 - leftmostValue)):
                                                                                leftmostValue = value
                                                                if(value < 180):
                                                                        if((lastReading + value - 360) > (lastReading + leftmostValue - 360)):
                                                                                leftmostValue = value
                                else:
                                        if(value < lastReading):
                                                if((lastReading - value) > (lastReading - leftmostValue)):
                                                        leftmostValue = value
                                        else:
                                                if((value - lastReading) > (rightmostValue - lastReading)):
                                                        rightmostValue = value
                        xComponent = math.sin(value*math.pi/180)
                        yComponent = math.cos(value*math.pi/180)
                        totalxComponents = totalxComponents + xComponent
                        totalyComponents = totalyComponents + yComponent
                        windDirQueue.put(value)
                        i = i + 1
        if(windDirQueue.full()):
                avgWindDir = int(round(math.atan2(totalxComponents, totalyComponents)*180/math.pi))
                if(avgWindDir < 0):
                        avgWindDir = avgWindDir + 360
                store.set("windDir", avgWindDir)
                store.set("leftmost", leftmostValue)
                store.set("rightmost", rightmostValue)
                print("Average Wind Direction: " + str(avgWindDir))
                print("leftmost Wind Direction: " + str(leftmostValue))
                print("rightmost Wind Direction: " + str(rightmostValue))
                print("")
        else:
                store.set("windDir", windDir)
                store.set("gustWindDiff", 0)

while(True):
	#windDir = int(store.get('programmedWindDir')) 
        windDir = int(mcp.read_adc(0)*360/1024)
        print windDir
        findAVGandVariable(windDir)
#	store.set('windDir', windDir)
	time.sleep(2)
