#!/usr/bin/python                                                   # Tells the file where the python files are located

import subprocess
import os                                                           # Import os functionality that allow this file to run os commands like aplay
import time                                                         # Import time functions so this file can get current time
import random                                                       # Import random to generate random numbers for testing purposes
import redis                                                        # Import redis for the functionality of sharing variables between processes in RAM
import RPi.GPIO as GPIO                                             # Import GPIO to read from GPIO pins
GPIO.setmode(GPIO.BCM)                                              # Set mode of GPIO to BCM (refer to pins by their channel number, not actual pin number)

CarrierDetectPin = 27
PTTPin = 17

GPIO.setup(PTTPin, GPIO.OUT)
GPIO.setup(CarrierDetectPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)                   # Setup GPIO pin 18 as input to pull down mode
numOfClicks = 0                                                     # Initialize numOfClicks to 0
timeSinceLastReport = time.time()
updateMin = 5
updateTimer = updateMin * 60
r = redis.StrictRedis(host='localhost', port=6379, db=0)            # Initialize the redis server connection



#IMPORT FROM DJANGO
transmissionNumClicks = 3
weatherNumClicks = 4
carrierDwellTimeMin = 0.1
carrierDwellTimeMax = 2
carrierIntervalTimeMin = 0.1
carrierIntervalTimeMax = 2
reportGust = 3
reportVariableWinds = 15
updateSpeed = 5
updateDirection = 30
updateTimer = 5
crosswindLimitSpeed = 6
crosswindLimitDirection = 45
favorWindSpeed = 6
favorWindDirection = 44


def play(command):
    GPIO.output(PTTPin, GPIO.HIGH)
    os.system(command)                                              # Commands the os to play the transmitRadioCheck WAV file using aplay
    GPIO.output(PTTPin, GPIO.LOW)

# This function performs the Transmit Radio Check of the Auto FBO
def transmitRadioCheck():                                           # Function definition
    finishCheck = False                                             # Initialize boolean finishCheck variable to False
    play("aplay -D plughw:1,0 transmitRadioCheck.wav")              # Commands the os to play the transmitRadioCheck WAV file using aplay
    currentTime = time.time()                                       # Set variable currentTime to current time
    cutoffTime = time.time() + 2                                    # Set a cutoffTime to 2 seconds after the current time. This time amount can be changed
    while currentTime < cutoffTime:                                 # While the current time is less than the cut off time set above
        if(GPIO.input(CarrierDetectPin) == False):                                # If the pushbutton connected to pin 18 is pressed
            audioproc = subprocess.Popen(['arecord -c 2 -D hw:0,0 -f S16_LE -r48000 pilotTest.wav'], shell = True)        # Command system to record audio at 48000Hz for 5 seconds to pilotTest WAV file
            while(GPIO.input(CarrierDetectPin) == False):
                pass
            os.system("pkill arecord")
            finishCheck = True                                      # Set finishCheck to True. This means the pilot keyed their mic and recorded a test
        currentTime = time.time()                                   # Reset currentTime for the while loop
    if finishCheck:                                                 # If the finishCheck variable is true
        play("aplay -D plughw:1,0 pilotTest.wav")                            # Command the system to play the recorded WAV file
        play("aplay -D plughw:1,0 power.wav")                                # Command the system to play the power WAV file
        powerLevel = random.randrange(10) + 1                       # Assign a random powerLevel FOR TESTING PURPOSES
        if powerLevel == 0:                                         # If power level is 0
            print "Power level is zero"                             # Print a statement (no audio was given)
        elif powerLevel == 1:                                       # Else if power level is 1
            play("aplay -D plughw:1,0 plOne.wav")                            # Command the system to play the plOne WAV file
        elif powerLevel == 2:                                       # Else if power level is 2
            play("aplay -D plughw:1,0 plTwo.wav")                            # Command the system to play the plTwo WAV file
        elif powerLevel == 3:                                       # So on and so forth...
            play("aplay -D plughw:1,0 plThree.wav")                          # 
        elif powerLevel == 4:                                       # 
            play("aplay -D plughw:1,0 plFour.wav")                           # 
        elif powerLevel == 5:                                       # 
            play("aplay -D plughw:1,0 plFive.wav")                           # 
        elif powerLevel == 6:                                       # 
            play("aplay -D plughw:1,0 plSix.wav")                            # 
        elif powerLevel == 7:                                       # 
            play("aplay -D plughw:1,0 plSeven.wav")                          # 
        elif powerLevel == 8:                                       # 
            play("aplay -D plughw:1,0 plEight.wav")                          # 
        elif powerLevel == 9:                                       # 
            play("aplay -D plughw:1,0 plNine.wav")                           # 
        elif powerLevel == 10:                                      # 
            play("aplay -D plughw:1,0 plTen.wav")                            # 
        else:                                                       # If the powerlevel is out of the normal range for some reason
            print "Power level is out of range?"                    # Print a statement saying that

# This function broadcasts the current wind conditions (direction and speed)
def broadcastWinds():                                               # Function definition
    play("aplay -D plughw:1,0 OAA.wav")                              # Command system to play Apopka Winds WAV file
    play("aplay -D plughw:1,0 AWA.wav")                              # Command system to play Apopka Winds WAV file
    windDir = int(r.get('windDir'))                                   # Get the wind direction from the redis store as a string
    windSpeed = round(float(r.get('windSpeed')))                               # Get the wind speed from the redis store as a string
    gustWindSpeed = int(round(float(r.get('gustWindSpeed'))))
    windDirMin = r.get('leftmost')
    play("aplay -D plughw:1,0 winds.wav")                              # Command system to play Apopka Winds WAV file
    windDirMin = int(windDirMin)
    windDirMax = int(r.get('rightmost'))
    if(windSpeed <= 6):
        play("aplay -D plughw:1,0 LAV.wav")
        
    else:
        windDirHundred = windDir/100                                    # Get hundreds digit by dividing by 100
        windDirTen = (windDir - (windDirHundred * 100))/10              # Get tens digit by subtracting hundreds (times 100) from wind direction, then dividing by 10
        windDirOne = (windDir - (windDirHundred * 100) -                # Get ones digit by subtracting hundreds (times 100) 
                      (windDirTen * 10))                                # and tens (times 10) from wind direction
        print "Wind Direction : " + str(windDir)                        # Print wind direction FOR TESTING PURPOSES
        if(abs(windDirMax - windDir) > 15) or (abs(windDirMin - windDir) > 15):
            play("aplay -D plughw:1,0 windsVariable.wav")
            play("aplay -D plughw:1,0 between.wav")
            windDirMaxHundred = windDirMax/100                                    # Get hundreds digit by dividing by 100
            windDirMaxTen = (windDirMax - (windDirMaxHundred * 100))/10              # Get tens digit by subtracting hundreds (times 100) from wind direction, then dividing by 10
            windDirMaxOne = (windDirMax - (windDirMaxHundred * 100) -                # Get ones digit by subtracting hundreds (times 100) 
                          (windDirMaxTen * 10))                                # and tens (times 10) from wind direction
            windDirMinHundred = windDirMin/100                                    # Get hundreds digit by dividing by 100
            windDirMinTen = (windDirMin - (windDirMinHundred * 100))/10              # Get tens digit by subtracting hundreds (times 100) from wind direction, then dividing by 10
            windDirMinOne = (windDirMin - (windDirMinHundred * 100) -                # Get ones digit by subtracting hundreds (times 100) 
                          (windDirMinTen * 10))                                # and tens (times 10) from wind direction
            speakDigit(windDirMinHundred)                                      # Send hundreds digit to get spoken
            speakDigit(windDirMinTen)                                          # Send tens digit to get spoken
            speakDigit(windDirMinOne)                                          # Send ones digit to get spoken
            play("aplay -D plughw:1,0 and.wav")
            speakDigit(windDirMaxHundred)                                      # Send hundreds digit to get spoken
            speakDigit(windDirMaxTen)                                          # Send tens digit to get spoken
            speakDigit(windDirMaxOne)                                          # Send ones digit to get spoken
        else:
            speakDigit(windDirHundred)                                      # Send hundreds digit to get spoken
            speakDigit(windDirTen)                                          # Send tens digit to get spoken
            speakDigit(windDirOne)                                          # Send ones digit to get spoken
    play("aplay -D plughw:1,0 at.wav")                                       # Command the system to play At WAV file
    windSpeedOne = windSpeed%10                                     # Get the ones digit by mod10
    windSpeedTen = (windSpeed - windSpeedOne)/10                         # get the tens number by subtracting ones digit from wind speedG    print "Wind Speed : " + str(windSpeed)                          # 
    if(windSpeed == 0):
        speakDigit(0)
    if(windSpeed > 9):
        speakDigit(windSpeedTen)                                         # Send the tens number to get spoken
    speakDigit(windSpeedOne)                                    # If so, send ones digit to get spoken
    play("aplay -D plughw:1,0 knots.wav")                                    # Command the system to play Knots WAV file
    if((gustWindSpeed - windSpeed) > 3):
        print("GUSTING AT: " + str(gustWindSpeed) + "knots")
        play("aplay -D plughw:1,0 gusting.wav")
        windSpeedOne = gustWindSpeed%10                                     # Get the ones digit by mod10
        windSpeedTen = (gustWindSpeed - windSpeedOne)/10                         # get the tens number by subtracting ones digit from wind speedG    print "Wind Speed : " + str(windSpeed)                          # 
        if(gustWindSpeed == 0):
            speakDigit(0)
        speakDigit(windSpeedTen)                                         # Send the tens number to get spoken
        if(windSpeedOne >= 0):                                           # Check if ones digit is greater than 0 (if 0, we don't want to speak it. Then it would say "fifty zero!")
            speakDigit(windSpeedOne)                                    # If so, send ones digit to get spoken
        play("aplay -D plughw:1,0 knots.wav")
    if(windDir > 130):
        if(windDir < 170):
            if(windSpeed > 6):
                play("aplay -D plughw:1,0 recommendOneFive.wav")
    if(windDir > 300):
        if(windDir < 360):
            if(windSpeed > 6):
                play("aplay -D plughw:1,0 recommendThreeThree.wav")
    if((windDir > 220 and windDir < 260) or (windDir > 40 and windDir < 80)):
        if(windSpeed > 6):
            play("aplay -D plughw:1,0 crosswind.wav")
            play("aplay -D plughw:1,0 warning.wav")
    global timeSinceLastReport
    timeSinceLastReport = time.time()
        
# This function speaks any digit 0 through 9
def speakDigit(n):                                                  # Function definition
    if(n == 0):                                                     # If n is 0
        play("aplay -D plughw:1,0 zero.wav")                                 # Command system to play the Zero WAV file
    elif(n == 1):                                                   # if n is 1
        play("aplay -D plughw:1,0 one.wav")                                  # Command system to play the One WAV file
    elif(n == 2):                                                   # So on and so forth...
        play("aplay -D plughw:1,0 two.wav")                                  # 
    elif(n == 3):                                                   # 
        play("aplay -D plughw:1,0 three.wav")                                # 
    elif(n == 4):                                                   # 
        play("aplay -D plughw:1,0 four.wav")                                 # 
    elif(n == 5):                                                   # 
        play("aplay -D plughw:1,0 five.wav")                                 # 
    elif(n == 6):                                                   # 
        play("aplay -D plughw:1,0 six.wav")                                  # 
    elif(n == 7):                                                   # 
        play("aplay -D plughw:1,0 seven.wav")                                # 
    elif(n == 8):                                                   # 
        play("aplay -D plughw:1,0 eight.wav")                                # 
    elif(n == 9):                                                   # 
        play("aplay -D plughw:1,0 nine.wav")                                 # 
    else:                                                           # If all else fails and n is less than 0 or greater than 9 for some weird reason
        print "Invalid digit : " + str(n)                           # Print the invalid digit

# This function counts clicks from the pilot
def countClicks2():                                                 # Funtion definition
    keepGoing = True                                                # Initialize keepGoing to True
    currentTime = time.time()                                       # Set currentTiem to current time
    tooEarly = currentTime + 0.1                                    # Set tooEarly to .1 second after
    cutoffTime = currentTime + 2                                    # Set cutoffTime to 2 seconds after
    global numOfClicks                                              # Use numOfClicks as global variable so functions can share it
    numOfClicks = 0                                                 # Set numOfClicks to 0 since beginning of function
    while numOfClicks < 10:                                         # While numOfClicks is less than 10
        keepGoing = True                                            # Set keepGoing to True
        if(GPIO.input(CarrierDetectPin) == True):                                 # If the button is let go
            print "PRESSED"
            time.sleep(0.1)
            if(time.time() < tooEarly):                                 # Check if it was let go too early
                break                                                   # and break
            elif(time.time() > cutoffTime):                             # Check if it was let go too late
                break                                                   # and break
            else:                                                       # Otherwise button let go was good
                numOfClicks = numOfClicks + 1                           # Increment numOfClicks
                currentTime = time.time()                               # Reset currentTime
                tooEarly = currentTime + 0.1                            # Reset tooEarly
                cutoffTime = currentTime + 2                            # Reset cutoffTime
                while keepGoing:                                        # While keepGoing is true
                    if(GPIO.input(CarrierDetectPin) == False):                        # If button is pushed
                        print "LET GO"
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

# This is the MAIN portion of the file
while True:                                                         # Continuous loop using while true
    global timeSinceLastReport
    #if((timeSinceLastReport + updateTimer) > time.time()):
    #    play("aplay -D plughw:1,0 updatedAdvisory.wav")
    #    broadcastWinds()
    if(GPIO.input(CarrierDetectPin) == True):                                    # If the pushbutton connected to pin 18 is pressed
        countClicks2()                                              # start counting clicks
        global numOfClicks                                          # use numOfClicks as a global variable so the functions can share it
        print numOfClicks
        if numOfClicks == 3:                                        # if numOfClicks is 3
            broadcastWinds()                                        # run the broadcastWinds function
#            time.sleep(2)
        if numOfClicks == 4:                                        # if numOfClicks is 4
            transmitRadioCheck()                                    # run transmitRadioCheck function
        
