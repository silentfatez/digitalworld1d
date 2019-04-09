
from libdw import pyrebase
from libdw import sm
import datetime
from secrets import firebasesecrets
blocktime=30
class RoomSM(sm.SM):
    start_state = 'all clear'
    def start(self):
        self.state = self.start_state
    def get_next_values(self, state, inp):
            irsensor1= db.child("irsensor1").get().val()
            ussensor1= db.child("distancesensor1").get().val()
            irsensor2= db.child("irsensor2").get().val()
            ussensor2= db.child("distancesensor2").get().val()
            name1=db.child("name1").get().val()
            name2=db.child("name2").get().val()
            timenow=datetime.datetime.now()
            table1time,table2time=inp #get timings from previous inp
            if state=='all clear':
                if irsensor1=='Occupied' and ussensor1=='Occupied':
                    if name1=='Empty':
                        db.child("name1").set('Unknown')
                    next_state='table 1 occupied'
                    table1time = datetime.datetime.now()
                    table1time = table1time + datetime.timedelta(minutes = blocktime)

                elif irsensor2=='Occupied' and ussensor2=='Occupied':
                    if name2=='Empty':
                        db.child("name2").set('Unknown')
                    next_state='table 2 occupied'
                    table2time = datetime.datetime.now()
                    table2time = table2time + datetime.timedelta(minutes = blocktime)
                else:
                    next_state=state
            elif state=='table 1 occupied':
                if timenow.time()<table1time.time():
                    if name2=='Empty':
                        db.child("name2").set('Unknown')
                    if irsensor2=='Occupied' and ussensor2=='Occupied':
                        next_state='all tables occupied'
                        table2time = datetime.datetime.now()
                        table2time = table2time + datetime.timedelta(minutes = blocktime)
                    else:
                        next_state=state
                else:

                    next_state='all clear'
                    db.child("name1").set('Empty')

            elif state=='table 2 occupied':
                if timenow.time()<table2time.time():
                    if irsensor1=='Occupied' and ussensor1=='Occupied':
                        if name2=='Empty':
                            db.child("name2").set('Unknown')
                        next_state='all tables occupied'
                        table1time = datetime.datetime.now()
                        table1time = table1time + datetime.timedelta(minutes = blocktime)
                    else:
                        next_state=state
                else:
                    next_state='all clear'


            elif state=='all tables occupied':
                if timenow.time()>table2time.time():
                    next_state='table 1 occupied'

                elif timenow.time()>table1time.time():
                    next_state='table 2 occupied'

            return next_state,(table1time,table2time)



url = firebasesecrets['url'] # URL to Firebase database
apikey = firebasesecrets['apikey'] # unique token used for authentication

config={
    "apiKey":apikey,
    "databaseURL":url,
}
firebase = pyrebase.initialize_app(config)
db = firebase.database()
roomsm=RoomSM()
roomsm.start()
table1time=datetime.datetime.now()
table2time=datetime.datetime.now()

while 1:
    (table1time,table2time)=roomsm.step((table1time,table2time))
