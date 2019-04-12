from libdw import pyrebase
from libdw import sm
import datetime
from secrets import *
import datetime
import json

def default(o):
    if isinstance(o, (datetime.date, datetime.datetime)):
        return o.isoformat()

    return json.dumps(item,sort_keys=True,indent=1,default=default)



blocktime=0.5
blockbuffertime=0
class tableSM(sm.SM):

    def __init__(self):
        self.state = 'all clear'
    def get_next_values(self, state, inp):
            table1val= db.child("table1").get().val()
            table2val= db.child("table2").get().val()
            name1=db.child('name1').get().val()
            name2=db.child('name2').get().val()
            print(table1val)
            timenow=datetime.datetime.now()
            table1time,table2time=inp #get timings from previous inp
            if state=='all clear':
                if table1val=='Occupied':
                    next_state='table 1 occupied'
                    table1time = datetime.datetime.now()
                    table1time = table1time + datetime.timedelta(minutes = blocktime)
                    db.child('table1time').set(default(table1time))

                elif table2val=='Occupied':
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
                        if table1val=="Occupied":
                                table1time = datetime.datetime.now()
                                table1time = table1time + datetime.timedelta(minutes = blocktime)
                                db.child('table1time').set(default(table1time))
                    if table2val=='Occupied':
                        next_state='all tables occupied'
                        table2time = datetime.datetime.now()
                        table2time = table2time + datetime.timedelta(minutes = blocktime)
                        db.child('table2time').set(default(table2time))


                    else:
                        next_state=state
                else:
                    next_state='all clear'
                    db.child("name1").update('Empty')
                    db.child('table1time').set('Empty')



            elif state=='table 2 occupied':
                if timenow.time()<table2time.time():
                    if name2=='Empty':
                        db.child("name2").update('Unknown')
                    table2timebuffer = table2time - datetime.timedelta(minutes = blockbuffertime)


                    if timenow.time()<table2timebuffer.time():
                        if table2val=='Occupied':
                            table2time = datetime.datetime.now()
                            table2time = table2time + datetime.timedelta(minutes = blocktime)
                            db.child('table2time').set(default(table2time))


                    if table1val=='Occupied':
                        next_state='all tables occupied'
                        table1time = datetime.datetime.now()
                        table1time = table1time + datetime.timedelta(minutes = blocktime)
                        db.child('table1time').set(default(table1time))

                    else:
                        next_state=state
                else:
                    next_state='all clear'
                    db.child("name2").update('Empty')
                    db.child('table2time').set("Empty")


            elif state=='all tables occupied':
                if name1=='Empty':
                    db.child("name1").update('Unknown')
                if name2=='Empty':
                    db.child("name1").update('Unknown')
                table1timebuffer = table1time - datetime.timedelta(minutes = blockbuffertime)
                table2timebuffer = table2time - datetime.timedelta(minutes = blockbuffertime)
                if timenow.time()<table2timebuffer.time():
                    if table2val=="Occupied":
                            table2time = datetime.datetime.now()
                            table2time = table2time + datetime.timedelta(minutes = blocktime)
                            db.child('table2time').set(default(table2time))

                if timenow.time()<table1timebuffer.time():
                    if table1val=='Occupied':
                            table1time = datetime.datetime.now()
                            table1time = table1time + datetime.timedelta(minutes = blocktime)
                            db.child('table1time').set(default(table1time))

                if timenow.time()>table2time.time():
                    next_state='table 1 occupied'
                    db.child('table2time').set("Empty")
                    db.child("name2").update('Empty')
                elif timenow.time()>table1time.time():
                    next_state='table 2 occupied'
                    db.child('table1time').set("Empty")
                    db.child("name1").update('Empty')
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
tablesm=tableSM()
table1time=datetime.datetime.now()
table2time=datetime.datetime.now()

while 1:
    print(tablesm.state)
    (table1time,table2time)=tablesm.step((table1time,table2time))
