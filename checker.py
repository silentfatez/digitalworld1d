from libdw import pyrebase
from libdw import sm
import datetime
from secrets import *
import datetime
import json

def default(o):
    if isinstance(o, (datetime.date, datetime.datetime)):
        return o.isoformat()

    return json.dumps(\
      item,\
      sort_keys=True,\
      indent=1,\
      default=default)


blocktime=10
blockbuffertime=5
class RoomSM(sm.SM):
    start_state = 'all clear'
    
    def start(self):
        self.state = self.start_state
    def get_next_values(self, state, inp):
            room1val= db.child("room1").get().val()
            room2val= db.child("room2").get().val()
            name1=db.child('name1').get().val()
            name2=db.child('name2').get().val()
            print(room1val)
            timenow=datetime.datetime.now()
            table1time,table2time=inp #get timings from previous inp
            if state=='all clear':
                if room1val=='Occupied':
                    next_state='table 1 occupied'
                    table1time = datetime.datetime.now()
                    table1time = table1time + datetime.timedelta(minutes = blocktime)
                    db.child('table1time').set(default(table1time))

                elif room2val=='Occupied':
                    next_state='table 2 occupied'
                    table2time = datetime.datetime.now()
                    table2time = table2time + datetime.timedelta(minutes = blocktime)
                    table2timebuffer = table2time - datetime.timedelta(minutes = blockbuffertime)
                    db.child('table2time').set(default(table2time))

                else:
                    next_state=state


            elif state=='table 1 occupied':
                if timenow.time()<table1time.time():
                    if name1=='Empty':
                        db.child("name1").set('Unknown')
                    table1timebuffer = table1time - datetime.timedelta(minutes = blockbuffertime)
                    if timenow.time()<table1timebuffer.time():
                        if room1val=="Occupied":
                                table1time = datetime.datetime.now()
                                table1time = table1time + datetime.timedelta(minutes = blocktime)
                                db.child('table1time').set(default(table1time))
                    if room2val=='Occupied':
                        next_state='all tables occupied'
                        table2time = datetime.datetime.now()
                        table2time = table2time + datetime.timedelta(minutes = blocktime)
                        db.child('table2time').set(default(table2time))


                    else:
                        next_state=state
                else:
                    next_state='all clear'
                    db.child("name1").set('Empty')
                    db.child('table1time').set('Empty')



            elif state=='table 2 occupied':
                if timenow.time()<table2time.time():
                    if name2=='Empty':
                        db.child("name2").set('Unknown')
                    table2timebuffer = table2time - datetime.timedelta(minutes = blockbuffertime)


                    if timenow.time()<table2timebuffer.time():
                        if room2val=='Occupied':
                            table2time = datetime.datetime.now()
                            table2time = table2time + datetime.timedelta(minutes = blocktime)
                            db.child('table2time').set(default(table2time))


                    if room1val=='Occupied':
                        next_state='all tables occupied'
                        table1time = datetime.datetime.now()
                        table1time = table1time + datetime.timedelta(minutes = blocktime)
                        db.child('table1time').set(default(table1time))

                    else:
                        next_state=state
                else:
                    next_state='all clear'
                    db.child("name2").set('Empty')
                    db.child('table2time').set("Empty")


            elif state=='all tables occupied':
                if name1=='Empty':
                    db.child("name1").set('Unknown')
                if name2=='Empty':
                    db.child("name1").set('Unknown')
                table1timebuffer = table1time - datetime.timedelta(minutes = blockbuffertime)
                table2timebuffer = table2time - datetime.timedelta(minutes = blockbuffertime)
                if timenow.time()<table2timebuffer.time():
                    if room2val=="Occupied":
                            table2time = datetime.datetime.now()
                            table2time = table2time + datetime.timedelta(minutes = blocktime)
                            db.child('table2time').set(default(table2time))

                if timenow.time()<table1timebuffer.time():
                    if room1val=='Occupied':
                            table1time = datetime.datetime.now()
                            table1time = table1time + datetime.timedelta(minutes = blocktime)
                            db.child('table1time').set(default(table1time))

                if timenow.time()>table2time.time():
                    next_state='table 1 occupied'
                    db.child('table2time').set("Empty")
                    db.child("name2").set('Empty')
                elif timenow.time()>table1time.time():
                    next_state='table 2 occupied'
                    db.child('table1time').set("Empty")
                    db.child("name1").set('Empty')
                else:
                    next_state=state

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
    print(roomsm.state)
    (table1time,table2time)=roomsm.step((table1time,table2time))
