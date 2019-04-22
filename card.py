import RPi.GPIO as GPIO
from libdw import pyrebase
from mfrc522 import SimpleMFRC522
from secrets import firebasesecrets

url = firebasesecrets['url'] # URL to Firebase database
apikey = firebasesecrets['apikey'] # unique token used for authentication

config={
    "apiKey":apikey,
    "databaseURL":url,
}
reader = SimpleMFRC522()
while True:
    id, text = reader.read()
    db.child("name"+str(tablenumber)).update(text)
