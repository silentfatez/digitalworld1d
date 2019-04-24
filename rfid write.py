# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 19:12:03 2019

@author: Gus

Retrieved from
https://pimylifeup.com/raspberry-pi-rfid-rc522/
"""

import RPi.GPIO as GPIO

#imports in SimpleMFRC522 library, this is what we will use actually to talk with the RFID RC522
from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522()

try:
        text = input('New data:')
        print("Now place your tag to write")
        reader.write(text)
        print("Written")
finally:
        GPIO.cleanup()
