# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 19:12:03 2019

@author: silentfatez
"""

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522()

try:
        text = input('New data:')
        print("Now place your tag to write")
        reader.write(text)
        print("Written")
finally:
        GPIO.cleanup()