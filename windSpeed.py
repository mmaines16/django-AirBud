
from __future__ import division #import the newest version of pythons division function to get decimal values
import time
import Queue
import django
import os

# Import SPI library (for hardware SPI) and MCP3008 library.
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
import time
import RPi.GPIO as GPIO

import redis
store = redis.StrictRedis(host='localhost', port=6379, db=0)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "air_bud.settings")
django.setup()

try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print("Error importing RPi.GPIO!  This is probably because you need superuser privileges.  You can achieve this by using 'sudo' to run your script")

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(22, GPIO.IN)

time_window = 5 # time in seconds becore stopping counter
time_stamp = time.time()


windSpeedQueue = Queue.Queue(maxsize=20)

store.set("counter", 0)
store.set("time_window", time_window)
store.set("time_stamp", time_stamp)
store.set("firstPulseTime", time.time())

def findAVGandGust(windSpeed):
    startTime = time.time()
    global windSpeedQueue
    windSpeedTotal = 0
    windSpeedMax = 0
    windSpeedMin = 100
    if(windSpeedQueue.full()):
        print("QUEUE FULL")
        windSpeedQueue.get()
    windSpeedQueue.put(windSpeed)
    if(windSpeedQueue.full()):
        i = 0
        while(i < 20):
            value = windSpeedQueue.get()
            windSpeedTotal = windSpeedTotal + value
            if(value > windSpeedMax):
                windSpeedMax = value
            if(value < windSpeedMin):
                windSpeedMin = value
            windSpeedQueue.put(value)
            i = i + 1
    if(windSpeedQueue.full()):
        avgWindSpeed = (windSpeedTotal-windSpeedMax-windSpeedMin)/18
        store.set("windSpeed", avgWindSpeed)
        store.set("gustWindSpeed", windSpeedMax)
        print("Average Wind Speed: " + str(avgWindSpeed))
        print("Gust Wind Speed: " + str(windSpeedMax))
    else:
        store.set("windSpeed", windSpeed)
        store.set("gustWindSpeed", 0)
        print("Current wind speed: " + str(windSpeed))

def pulse_callback(channel):
    store = redis.StrictRedis(host='localhost', port=6379, db=0)
    t_window = store.get("time_window")
    t_stamp = float(store.get("time_stamp"))
    time_now = time.time()

    store.set("time_stamp", time_now)
    counter = int(store.get("counter"))

    firstPulseTime = float(store.get("firstPulseTime"))
    timeDif = time_now-firstPulseTime
    if(timeDif >= 2.25):
        counter = counter*2.25
        counter = counter/timeDif
        windSpeed = counter/1.15
        findAVGandGust(windSpeed)
#        store.set("windSpeed", windSpeed)
        store.set("firstPulseTime", time.time() + 10)
        store.set("counter", 0)
        return

    if(t_window <= (time_now-t_stamp)):
        counter = 0
    else:
        if(counter == 0):
            store.set("firstPulseTime", time.time())
        counter = counter + 1
    store.set("counter", counter)
    
GPIO.add_event_detect(22, GPIO.FALLING, callback=pulse_callback)

while True:
    #Comment this out if you want to run with anemometer
   # while True:
   #     print "Getting programmed wind speed!"
   #     windSpeed = int(store.get('programmedWindSpeed'))
   #     findAVGandGust(windSpeed)
   #     time.sleep(2.25)
    time_now = time.time()
    time_stamp = float(store.get("time_stamp"))

    counter = int(store.get("counter"))
    firstPulseTime = float(store.get("firstPulseTime"))
    timeDif = time_now-firstPulseTime
    if(timeDif >= 2.25):
        counter = counter*2.25
        counter = counter/timeDif
        windSpeed = counter/1.15
	findAVGandGust(windSpeed)
#        store.set("windSpeed", windSpeed)
        store.set("firstPulseTime", time.time() + 10)
        store.set("counter", 0)
    
    if((time_now-time_stamp)>3):
        counter = int(store.get("counter"))
        windSpeed = counter/1.15
        store.set("windSpeed", windSpeed)
        store.set("counter", 0)
        store.set("time_stamp", time.time())
GPIO.cleanup()           # clean up GPIO on normal exit 
