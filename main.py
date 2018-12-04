#!/usr/bin/env python3
#
# Developed by Philip Orand 
#
# Date:11/18/2018
#
# Version 1.1
#
#12/4/18 Fixed bug that reset checkcount number

import os
import time
from datetime import datetime
import picamera
import RPi.GPIO as GPIO
import ffmpeg
from weather import Weather, Unit
import smtplib
from time import sleep


#~~~~~~~~ Variables ~~~~~~~~~~#
photoTime = ['09:00:00', '09:30:00', '10:00:00', '10:30:00', '11:00:00','11:30:00', '12:00:00', '12:30:00', '13:00:00', '13:30:00', '14:00:00', '14:30:00', '15:00:00', '15:30:00', '16:00:00', '16:30:00', '17:00:00']
checkInterval = 3 #checks soil and weather every 3 hours
waterDuration = 10 # Amount of time in minutes to water garden if needsWater = True
chanceRain = False
reBoot = True
checkWeather_trys = 0
location = 'YOUR_CITY,YOUR STATE' #EXAMPLE: Tyler,TX
gmail_user = 'YOUR_GOOGLE_EMAIL'  # Change to your email
gmail_password = 'YOUR_EMAIL_PASSOWRD' #your gmail password
email_to = ['EMAIL_TO_SEND_TO'] #email to send alert to (change to equal gmail_user if you want to send to yourself)
cwd = os.getcwd()
gardenPath = (cwd + '/GardenPics')

# Set our GPIO numbering to BOARD
GPIO.setmode(GPIO.BOARD)
# Define the GPIO pin that we have our digital output from our soil sensor connected to and relay
soilPin = 40
waterPin = 38
# Set the GPIO pin to an input
GPIO.setup(soilPin, GPIO.IN) #Assing pin as input
GPIO.setup(waterPin,GPIO.OUT) #Assign as output

#Set waterPin GPIO pin to low (OFF)
GPIO.output(waterPin, GPIO.LOW)



#~~~~~~~~~ Functions ~~~~~~~~~~#
def waterInterval(): #Updates new time to check soil #############COMPLETE
	global waterTime
	timeDiff = (int(time.strftime('%H')) + checkInterval)
	waterTime = ('%d:00:00' %(timeDiff))

def checkSoil():#########################COMPLETE
	needsWater = GPIO.input(soilPin)
	if (needsWater == HIGH): #If it needs water
		checkWeather()
	else:
		waterInterval()


def checkWeather(): ###################COMPLETE
	conditionList = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '35', '37', '38', '39', '40', '41', '42', '43', '45', '46', '47']
	weather = Weather(unit=Unit.CELSIUS)

	lookup = weather.lookup_by_location(location) #checks conditions in current set location
	condition = lookup.condition
	currCondition = condition.code

	if currCondition in conditionList:
		chanceRain = True

	checkCount()



def checkCount(): ##############COMPLETE
	if (chanceRain == True):
		if (checkWeather_trys == 1):
			waterGarden()
		else:
			checkWeather_trys += 1
			waterInterval() 
	else:
		waterGarden()
		


def takePhoto(): ########################COMPLETE
	dt = datetime.now()
	
	# Creating Dictionary to store images
	if not os.path.exists(gardenPath): 
		os.mkdir(gardenPath)

	#Checking if naming file is there
	try:
		with open(cwd + '/imageNaming.txt', 'r') as f:
	 		textLines = f.readlines()
	 	lastNum = textLines[-1]
	 	currentNum = int(lastNum) + 1

	except:
		currentNum = 0
		
	#Initailizes Camera
	cam = picamera.PiCamera()
	#Setting camera resalution to Max
	cam.resolution = (2592, 1944)
	# Sets filename to current date and time 
	filename = ('Image_%04d.jpg' %(currentNum)) 
	cam.hflip = True
	cam.vflip = True
	cam.annotate_text = dt.strftime('%B %d %Y')
	# Saves image to folder
	cam.capture('%s/%s' %(gardenPath, filename))

	with open(cwd + '/imageNaming.txt', 'a') as f:
	 	f.write('%d\n' %(currentNum))


def makeVideo():#################COMPLETE
	# Using ffmpeg to compile images into an mp4 file a 6 frames per second
	os.chdir(gardenPath)
	os.system('ffmpeg -r 1 -f image2 -s 1920x1080 -i Image_%04d.jpg -vcodec libx264 -crf 15 -pix_fmt yuv420p Timelapse.mp4')


def waterGarden():
	waterInterval()
	chanceRain = False
	checkWeather_trys = 0
	GPIO.output(waterPin, GPIO.HIGH) #Water ON
	sleep(waterDuration * 60)  #Water for a set time
	GPIO.output(waterPin, GPIO.LOW) #Water OFF
	needsWater = GPIO.input(soilPin)

	if (needsWater == HIGH): #If soil is still dry after watering 
		message = 'Garden watered but soil remains DRY.'
		arument = 'Death is imminent!!'
		onError(message, arument)




def onError(message, arg):################COMPLETE
	dt1 = datetime.now()
	timeNow = dt1.strftime('%B %d %Y %H:%M')
	sent_from = gmail_user   
	email_text = ('ERROR! AUTO GARDEN ERROR!\n\n%s: %s %s' %(timeNow, message, arg))

	try:  
    	server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    	server.ehlo()
    	server.login(gmail_user, gmail_password)
    	server.sendmail(sent_from, to, email_text)
    	server.close()
	except:  
    	with open('onError.txt', 'a') as f:
    		f.write('%s: %s %s' %(timeNow, message, arg))




waterInterval()
while True:
	currentTime = time.strftime('%H:%M:%S')

	if(reBoot == True):
		try:
			checkSoil()
			firstBoot = False
		except Exception as e:
			onError(e.message, e.args)

	if(waterTime == currentTime):
		try:
			checkSoil()
		except Exception as e:
			onError(e.message, e.args)
	
	if (currentTime in photoTime):
		try:
			takePhoto()
		except Exception as e:
			onError(e.message, e.args)
			
	sleep(1) #Delay 1 second so code wont over command functions








