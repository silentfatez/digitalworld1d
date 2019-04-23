import RPi.GPIO as GPIO
from libdw import pyrebase
from mfrc522 import SimpleMFRC522
from secrets import firebasesecrets
tablenumber=1
url = firebasesecrets['url'] # URL to Firebase database
apikey = firebasesecrets['apikey'] # unique token used for authentication
firebase = pyrebase.initialize_app(config)
db = firebase.database()
config={
    "apiKey":apikey,
    "databaseURL":url,
}
reader = SimpleMFRC522()
try:
    while True:
        id, text = reader.read()
        db.child("name"+str(tablenumber)).set(text)
except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()
