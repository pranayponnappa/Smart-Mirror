import RPi.GPIO as GPIO
import time
import subprocess
import os

sensor = 4

GPIO.setmode(GPIO.BCM)
GPIO.setup(sensor, GPIO.IN,GPIO.PUD_DOWN)

current_state = False

while True:
	time.sleep(1)
	current_state = GPIO.input(sensor)
	if  current_state != False:
		subprocess.Popen('sudo /opt/vc/bin/tvservice -p',shell=True)
		time.sleep(15)

	else:
		subprocess.Popen('sudo /opt/vc/bin/tvservice -o',shell=True)
		
	# current_state = GPIO.input(sensor)


