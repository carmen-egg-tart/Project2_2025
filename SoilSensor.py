#!/usr/bin/python3
import RPi.GPIO as GPIO
import time

# GPIO SETUP
channel = 4 
GPIO.setmode(GPIO.BCM)
GPIO.setup(channel, GPIO.IN)

def callback(channel):
    if GPIO.input(channel):
        print("No Water Detected!")
    else:
        print("Water Detected!")

GPIO.add_event_detect(channel, GPIO.BOTH, bouncetime=300)  # Detect both rising and falling edges
GPIO.add_event_callback(channel, callback)  # Assign the callback function

while True:
    time.sleep(0)
