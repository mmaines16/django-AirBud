#!/usr/bin/python                                                   # Tells the file where the python files are located

import subprocess
import os                                                           # Import os functionality that allow this file to run os commands like aplay
import django
import time                                                         # Import time functions so this file can get current time
import random                                                       # Import random to generate random numbers for testing purposes
import redis                                                        # Import redis for the functionality of sharing variables between processes in RAM
import RPi.GPIO as GPIO                                             # Import GPIO to read from GPIO pins
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008

## Software SPI Setup
CLK  = 11
MISO = 9
MOSI = 10
CS   = 8
mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)

#HARDWARE SPI
#SPI_PORT = 0
#SPI_DEVICE = 0
#mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))

#Configure Django (Allows for this script to be able to grab objects from the database)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "air_bud.settings")
django.setup()

#import the settings model and methods from Django
from settings.models import AirBudConfiguration

#get the Settings object from the database
conf = AirBudConfiguration.get_solo()


GPIO.setmode(GPIO.BCM)                                              # Set mode of GPIO to BCM (refer to pins by their channel number, not actual pin number)

CarrierDetectPin = 27
PTTPin = 17

GPIO.setup(PTTPin, GPIO.OUT)
GPIO.setup(CarrierDetectPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)                   # Setup GPIO pin 18 as input to pull down mode
numOfClicks = 0                                                     # Initialize numOfClicks to 0 
lastDirReading = 0
lastSpeedReading = 0
timeSinceLastReport = time.time()

r = redis.StrictRedis(host='localhost', port=6379, db=0)            # Initialize the redis server connection



#IMPORT FROM DJANGO
transmissionNumClicks = conf.transmission_check_clicks #3
weatherNumClicks = conf.weather_check_clicks #4
carrierDwellTimeMin = conf.carrier_dwell_time_min.total_seconds() #0.1
carrierDwellTimeMax = conf.carrier_dwell_time_max.total_seconds() #2
carrierIntervalTimeMin = conf.carrier_interval_time_min.total_seconds() #0.1
carrierIntervalTimeMax = conf.carrier_interval_time_max.total_seconds() #2
reportGust = conf.report_gust #3
reportVariableWinds = conf.report_variable_winds #15
updateSpeed = conf.update_speed #5
updateDirection = conf.update_direction #30
updateMin = conf.update_timer #5
crosswindLimitSpeed = conf.cross_wind_limit_speed #6
crosswindLimitDirection = conf.cross_wind_limit_direction #45
favorWindSpeed = conf.favor_wind_speed #6
favorWindDirection = conf.favor_wind_direction #44
updateTimer = updateMin*60


def play(command):
    if(GPIO.input(CarrierDetectPin) == True):
        while(GPIO.input(CarrierDetectPin) == True):
            pass
    if(GPIO.input(CarrierDetectPin) == False):
        GPIO.output(PTTPin, GPIO.HIGH)
        os.system(command)                                              # Commands the os to play the transmitRadioCheck WAV file using aplay
        GPIO.output(PTTPin, GPIO.LOW)

# This function performs the Transmit Radio Check of the Auto FBO
def transmitRadioCheck():                                           # Function definition
    finishCheck = False                                             # Initialize boolean finishCheck variable to False
    play("aplay transmitRadioCheck.wav")              # Commands the os to play the transmitRadioCheck WAV file using aplay
    currentTime = time.time()                                       # Set variable currentTime to current time
    cutoffTime = time.time() + 2                                    # Set a cutoffTime to 2 seconds after the current time. This time amount can be changed
    while currentTime < cutoffTime:                                 # While the current time is less than the cut off time set above
        if(GPIO.input(CarrierDetectPin) == True):                                # If the pushbutton connected to pin 18 is pressed
            audioproc = subprocess.Popen(['arecord -D hw:1,0 -f S16_LE -r48000 pilotTest.wav'], shell = True)        # Command system to record audio at 48000Hz for 5 seconds to pilotTest WAV file
            while(GPIO.input(CarrierDetectPin) == False):
                pass
            os.system("sudo pkill arecord")
            finishCheck = True                                      # Set finishCheck to True. This means the pilot keyed their mic and recorded a test
        currentTime = time.time()                                   # Reset currentTime for the while loop
    if finishCheck:                                                 # If the finishCheck variable is true
        play("aplay pilotTest.wav")                            # Command the system to play the recorded WAV file
        play("aplay power.wav")                                # Command the system to play the power WAV file
        #powerLevel = 10                       # Assign a random powerLevel FOR TESTING PURPOSES
        powerLevel = int(mcp.read_adc(1)/60)
        if powerLevel == 0:                                         # If power level is 0
            play("aplay 0of10.wav")                             # Print a statement (no audio was given)
        elif powerLevel == 1:                                       # Else if power level is 1
            play("aplay 1of10.wav")                            # Command the system to play the plOne WAV file
        elif powerLevel == 2:                                       # Else if power level is 2
            play("aplay 2of10.wav")                            # Command the system to play the plTwo WAV file
        elif powerLevel == 3:                                       # So on and so forth...
            play("aplay 3of10.wav")                          # 
        elif powerLevel == 4:                                       # 
            play("aplay 4of10.wav")                           # 
        elif powerLevel == 5:                                       # 
            play("aplay 5of10.wav")                           # 
        elif powerLevel == 6:                                       # 
            play("aplay 6of10.wav")                            # 
        elif powerLevel == 7:                                       # 
            play("aplay 7of10.wav")                          # 
        elif powerLevel == 8:                                       # 
            play("aplay 8of10.wav")                          # 
        elif powerLevel == 9:                                       # 
            play("aplay 9of10.wav")                           # 
        elif powerLevel >= 10:                                      # 
            play("aplay 10of10.wav")                            # 
        else:                                                       # If the powerlevel is out of the normal range for some reason
            print "Power level is out of range?"                    # Print a statement saying that

# This function broadcasts the current wind conditions (direction and speed)
def broadcastWinds():                                               # Function definition
    play("aplay apopkaAirport.wav")                              # Command system to play Apopka Winds WAV file
    play("aplay automatedWindAdvisory.wav")                              # Command system to play Apopka Winds WAV file
    windDir = int(r.get('windDir'))                                   # Get the wind direction from the redis store as a string
    windSpeed = round(float(r.get('windSpeed')))                               # Get the wind speed from the redis store as a string
    gustWindSpeed = int(round(float(r.get('gustWindSpeed'))))
    windDirMin = r.get('leftmost')
    play("aplay winds.wav")                              # Command system to play Apopka Winds WAV file
    windDirMin = int(windDirMin)
    windDirMax = int(r.get('rightmost'))

    if(windSpeed <= 4):
        play("aplay lightAndVariable.wav")
        
    else:
        print "Wind Direction : " + str(windDir)                        # Print wind direction FOR TESTING PURPOSES
        if(abs(windDirMax - windDir) > reportVariableWinds) or (abs(windDirMin - windDir) > reportVariableWinds):
            play("aplay variable.wav")
            play("aplay between.wav")
            speakDir(int(10*round(float(windDirMin)/10)))
            play("aplay and.wav")
            speakDir(int(10*round(float(windDirMax)/10)))
        else:
            speakDir(int(10*round(float(windDir)/10)))

    play("aplay at.wav")                                       # Command the system to play At WAV file
    if(windSpeed > 9):
        speakUp((windSpeed - (windSpeed%10))/10)                                         # Send the tens number to get spoken
    speakDown(windSpeed%10)                                    # If so, send ones digit to get spoken
    play("aplay knots.wav")                                    # Command the system to play Knots WAV file

    if((gustWindSpeed - windSpeed) > reportGust):
        print("GUSTING AT: " + str(gustWindSpeed) + "knots")
        play("aplay peakGust.wav")
        if(gustWindSpeed > 9):
            speakUp((gustWindSpeed - (gustWindSpeed%10))/10)                                         # Send the tens number to get spoken
        speakDown(gustWindSpeed%10)                                    # If so, send ones digit to get spoken
        play("aplay knots.wav")

    if(windDir > 130 and windDir < 170 and windSpeed > 6):
                play("aplay recommend15.wav")

    if(windDir > 300 and windDir < 360 and windSpeed > 6):
                play("aplay recommend33.wav")

    if((windDir > 220 and windDir < 260) or (windDir > 40 and windDir < 80)):
        if(windSpeed > 6):
            r.set("crossWindFlag", "true")
            play("aplay warningCrosswind.wav")
    else:
        r.set("crossWindFlag", "false")

    global timeSinceLastReport
    global lastDirReading
    global lastSpeedReading
    timeSinceLastReport = time.time()
    lastDirReading = windDir
    lastSpeedReading = windSpeed
        
def speakDir(dir):
    if(dir == 0):
        play("aplay 360.wav")
    elif(dir == 10):
        play("aplay 010.wav")
    elif(dir == 20):
        play("aplay 020.wav")
    elif(dir == 30):
        play("aplay 030.wav")
    elif(dir == 40):
        play("aplay 040.wav")
    elif(dir == 50):
        play("aplay 050.wav")
    elif(dir == 60):
        play("aplay 060.wav")
    elif(dir == 70):
        play("aplay 070.wav")
    elif(dir == 80):
        play("aplay 080.wav")
    elif(dir == 90):
        play("aplay 090.wav")
    elif(dir == 100):
        play("aplay 100.wav")
    elif(dir == 110):
        play("aplay 110.wav")
    elif(dir == 120):
        play("aplay 120.wav")
    elif(dir == 130):
        play("aplay 130.wav")
    elif(dir == 140):
        play("aplay 140.wav")
    elif(dir == 150):
        play("aplay 150.wav")
    elif(dir == 160):
        play("aplay 160.wav")
    elif(dir == 170):
        play("aplay 170.wav")
    elif(dir == 180):
        play("aplay 180.wav")
    elif(dir == 190):
        play("aplay 190.wav")
    elif(dir == 200):
        play("aplay 200.wav")
    elif(dir == 210):
        play("aplay 210.wav")
    elif(dir == 220):
        play("aplay 220.wav")
    elif(dir == 230):
        play("aplay 230.wav")
    elif(dir == 240):
        play("aplay 240.wav")
    elif(dir == 250):
        play("aplay 250.wav")
    elif(dir == 260):
        play("aplay 260.wav")
    elif(dir == 270):
        play("aplay 270.wav")
    elif(dir == 280):
        play("aplay 280.wav")
    elif(dir == 290):
        play("aplay 290.wav")
    elif(dir == 300):
        play("aplay 300.wav")
    elif(dir == 310):
        play("aplay 310.wav")
    elif(dir == 320):
        play("aplay 320.wav")
    elif(dir == 330):
        play("aplay 330.wav")
    elif(dir == 340):
        play("aplay 340.wav")
    elif(dir == 350):
        play("aplay 350.wav")
    elif(dir == 360):
        play("aplay 360.wav")
    else:
        print("WRONG DIRECTION" + str(dir))
    
# This function speaks any digit 0 through 9
def speakUp(n):                                                  # Function definition
    if(n == 0):                                                     # If n is 0
        play("aplay zeroUp.wav")                                 # Command system to play the Zero WAV file
    elif(n == 1):                                                   # if n is 1
        play("aplay oneUp.wav")                                  # Command system to play the One WAV file
    elif(n == 2):                                                   # So on and so forth...
        play("aplay twoUp.wav")                                  # 
    elif(n == 3):                                                   # 
        play("aplay threeUp.wav")                                # 
    elif(n == 4):                                                   # 
        play("aplay fourUp.wav")                                 # 
    elif(n == 5):                                                   # 
        play("aplay fiveUp.wav")                                 # 
    elif(n == 6):                                                   # 
        play("aplay sixUp.wav")                                  # 
    elif(n == 7):                                                   # 
        play("aplay sevenUp.wav")                                # 
    elif(n == 8):                                                   # 
        play("aplay eightUp.wav")                                # 
    elif(n == 9):                                                   # 
        play("aplay nineUp.wav")                                 # 
    else:                                                           # If all else fails and n is less than 0 or greater than 9 for some weird reason
        print "Invalid digit : " + str(n)                           # Print the invalid digit

# This function speaks any digit 0 through 9
def speakDown(n):                                                  # Function definition
    if(n == 0):                                                     # If n is 0
        play("aplay zeroDown.wav")                                 # Command system to play the Zero WAV file
    elif(n == 1):                                                   # if n is 1
        play("aplay oneDown.wav")                                  # Command system to play the One WAV file
    elif(n == 2):                                                   # So on and so forth...
        play("aplay twoDown.wav")                                  # 
    elif(n == 3):                                                   # 
        play("aplay threeDown.wav")                                # 
    elif(n == 4):                                                   # 
        play("aplay fourDown.wav")                                 # 
    elif(n == 5):                                                   # 
        play("aplay fiveDown.wav")                                 # 
    elif(n == 6):                                                   # 
        play("aplay sixDown.wav")                                  # 
    elif(n == 7):                                                   # 
        play("aplay sevenDown.wav")                                # 
    elif(n == 8):                                                   # 
        play("aplay eightDown.wav")                                # 
    elif(n == 9):                                                   # 
        play("aplay nineDown.wav")                                 # 
    else:                                                           # If all else fails and n is less than 0 or greater than 9 for some weird reason
        print "Invalid digit : " + str(n)                           # Print the invalid digit

# This function counts clicks from the pilot
def countClicks():                                                 # Funtion definition
    keepGoing = True                                                # Initialize keepGoing to True
    currentTime = time.time()                                       # Set currentTiem to current time
    tooEarly = currentTime + carrierDwellTimeMin                                    # Set tooEarly to .1 second after
    cutoffTime = currentTime + carrierDwellTimeMax                                    # Set cutoffTime to 2 seconds after
    global numOfClicks                                              # Use numOfClicks as global variable so functions can share it
    numOfClicks = 0                                                 # Set numOfClicks to 0 since beginning of function
    while numOfClicks < 10:                                         # While numOfClicks is less than 10
        keepGoing = True                                            # Set keepGoing to True
        if(GPIO.input(CarrierDetectPin) == False):                                 # If the button is let go
            print "LET GO"
            time.sleep(0.1)
            if(time.time() < tooEarly):                                 # Check if it was let go too early
                break                                                   # and break
            elif(time.time() > cutoffTime):                             # Check if it was let go too late
                break                                                   # and break
            else:                                                       # Otherwise button let go was good
                numOfClicks = numOfClicks + 1                           # Increment numOfClicks
                currentTime = time.time()                               # Reset currentTime
                tooEarly = currentTime + carrierDwellTimeMin                            # Reset tooEarly
                cutoffTime = currentTime + carrierDwellTimeMax                            # Reset cutoffTime
                while keepGoing:                                        # While keepGoing is true
                    if(GPIO.input(CarrierDetectPin) == True):                        # If button is pushed
                        print "PRESSED"
                        time.sleep(0.1)
                        if(time.time() < tooEarly):                         # Check if it was pushed too early
                            break                                           # and break
                        elif(time.time() > cutoffTime):                     # Check if it was pushed too kate
                            break                                           # and break
                        else:                                               # Otherwise button push was good
                            keepGoing = False                               # Set keepGoing to false to exit the while loop
                    elif(time.time() > cutoffTime):                     # If too much time goes by and button hasn't been pushed
                        break                                           # and break
        elif(time.time() > cutoffTime):                             # If too much time goes by and button hasn't been released
            break                                                   # and break

def sayHello(hour):
    print "HOUR - " + str(hour)
    if(hour >= 5 and hour < 17):
        play("aplay goodMorning.wav")
    elif(hour >= 17 and hour < 23):
        play("aplay goodAfternoon.wav")
    elif(hour >= 23 or hour < 5):
        play("aplay goodEvening.wav")

# This is the MAIN portion of the script
while True:                                                         # Continuous loop using while true
    timeNow = time.time()
    currentDirReading = int(r.get('windDir'))                                   # Get the wind direction from the redis store as a string
    currentSpeedReading = round(float(r.get('windSpeed')))
    global lastDirReading
    global lastSpeedReading
    global timeSinceLastReport
    if(abs(lastDirReading-currentDirReading)>updateDirection):
        print("2")
        play("aplay updatedAdvisory.wav")
        broadcastWinds()
    if(abs(lastSpeedReading-currentSpeedReading)>updateSpeed):
        print("3")
        play("aplay updatedAdvisory.wav")
        broadcastWinds()
    if(GPIO.input(CarrierDetectPin) == True):                                    # If the pushbutton connected to pin 18 is pressed
        print "START COUNTING CLICKS"
        countClicks()                                              # start counting clicks
        global numOfClicks                                          # use numOfClicks as a global variable so the functions can share it
        print numOfClicks
        if numOfClicks == weatherNumClicks:                                        # if numOfClicks is 3
            sayHello(int(time.strftime("%H")))
            broadcastWinds()                                        # run the broadcastWinds function
        if numOfClicks == transmissionNumClicks:                                        # if numOfClicks is 4
            sayHello(int(time.strftime("%H")))
            transmitRadioCheck()                                    # run transmitRadioCheck function
