import RPi.GPIO as GPIO
import time
from libdw import pyrebase
from secrets import firebasesecrets
from libdw import sm
tablenumber=1
GPIO.setwarnings(False)
distancelimit=100
GPIO.setmode(GPIO.BCM)


url = firebasesecrets['url'] # URL to Firebase database
apikey = firebasesecrets['apikey'] # unique token used for authentication

config={
    "apiKey":apikey,
    "databaseURL":url,
}
class Sensors(sm.SM):
    start_state = 'Empty'
    def start(self):
        self.state = self.start_state
    def get_next_values(self, state, inp):
            dist = distance()
            iroutput=GPIO.input(IR)
            if state=='Empty':
                if dist<distancelimit or iroutput==True:
                    next_state='Occupied'
                    db.child("table"+str(tablenumber)).set(next_state)
                else:
                    state=state
            else:
                if dist>distancelimit and iroutput==False:
                    next_state='Empty'
                    db.child('table'+str(tablenumber)).set(next_state)
                else:
                    next_state=state

            return next_state,next_state

firebase = pyrebase.initialize_app(config)
db = firebase.database()
TRIG = 13
ECHO = 19
IR=20
GPIO.setup(TRIG,GPIO.OUT)# Trig pin of Ultrasonic setup
GPIO.setup(ECHO,GPIO.IN)
GPIO.setup(IR,GPIO.IN) #GPIO 14 -> IR sensor as input

def distance():
    # set Trigger to HIGH
    GPIO.output(TRIG, True)

    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    StartTime = time.time()
    StopTime = time.time()

    # save StartTime
    while GPIO.input(ECHO) == 0:
        StartTime = time.time()

    # save time of arrival
    while GPIO.input(ECHO) == 1:
        StopTime = time.time()

    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2

    return distance


sensor=Sensors()
sensor.start()
next_state='Empty'


try:
        while True:
            dist = distance()
            next_state=sensor.step(next_state)
            time.sleep(1)
        # Reset by pressing CTRL + C
except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()
