from libdw import pyrebase
from libdw import sm
import datetime
from secrets import *
import gspread
from oauth2client.service_account import ServiceAccountCredentials
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)
sheet = client.open("Room Data").sheet1
row = ['Time','state']
index = 1
sheet.insert_row(row, index)
def update_next_row(state,n):
    row = [str(datetime.datetime.now()),str(state)]
    sheet.insert_row(row, n)



blocktime=1
blockbuffertime=0.5
class tableSM(sm.SM):

    def __init__(self):
        self.state = 'all clear'
        self.count=2
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
                    db.child('table1time').set(str(table1time))
                    update_next_row(next_state,self.count)
                    self.count+=1

                elif table2val=='Occupied':
                    next_state='table 2 occupied'
                    table2time = datetime.datetime.now()
                    table2time = table2time + datetime.timedelta(minutes = blocktime)
                    table2timebuffer = table2time - datetime.timedelta(minutes = blockbuffertime)
                    db.child('table2time').set(str(table2time))
                    update_next_row(next_state,self.count)
                    self.count+=1

                else:
                    next_state=state


            elif state=='table 1 occupied':
                if timenow.time()<table1time.time():
                    if name1=='':
                        db.child("name1").set('Unknown')
                    table1timebuffer = table1time - datetime.timedelta(minutes = blockbuffertime)
                    if timenow.time()<table1timebuffer.time():
                        if table1val=="Occupied":
                                table1time = datetime.datetime.now()
                                table1time = table1time + datetime.timedelta(minutes = blocktime)
                                db.child('table1time').set(str(table1time))
                    if table2val=='Occupied':
                        next_state='all tables occupied'
                        table2time = datetime.datetime.now()
                        table2time = table2time + datetime.timedelta(minutes = blocktime)
                        db.child('table2time').set(str(table2time))
                        update_next_row(next_state,self.count)
                        self.count+=1



                    else:
                        next_state=state
                else:
                    next_state='all clear'
                    db.child("name1").set('')
                    db.child('table1time').set('Empty')
                    update_next_row(next_state,self.count)
                    self.count+=1



            elif state=='table 2 occupied':
                if timenow.time()<table2time.time():
                    if name2=='':
                        db.child("name2").set('Unknown')
                    table2timebuffer = table2time - datetime.timedelta(minutes = blockbuffertime)


                    if timenow.time()<table2timebuffer.time():
                        if table2val=='Occupied':
                            table2time = datetime.datetime.now()
                            table2time = table2time + datetime.timedelta(minutes = blocktime)
                            db.child('table2time').set(str(table2time))


                    if table1val=='Occupied':
                        next_state='all tables occupied'
                        table1time = datetime.datetime.now()
                        table1time = table1time + datetime.timedelta(minutes = blocktime)
                        db.child('table1time').set(str(table1time))
                        update_next_row(next_state,self.count)
                        self.count+=1

                    else:
                        next_state=state
                else:
                    next_state='all clear'
                    db.child("name2").set('')
                    db.child('table2time').set("Empty")
                    update_next_row(next_state,self.count)
                    self.count+=1


            elif state=='all tables occupied':
                if name1=='':
                    db.child("name1").set('Unknown')
                if name2=='':
                    db.child("name1").set('Unknown')
                table1timebuffer = table1time - datetime.timedelta(minutes = blockbuffertime)
                table2timebuffer = table2time - datetime.timedelta(minutes = blockbuffertime)
                if timenow.time()<table2timebuffer.time():
                    if table2val=="Occupied":
                            table2time = datetime.datetime.now()
                            table2time = table2time + datetime.timedelta(minutes = blocktime)
                            db.child('table2time').set(str(table2time))

                if timenow.time()<table1timebuffer.time():
                    if table1val=='Occupied':
                            table1time = datetime.datetime.now()
                            table1time = table1time + datetime.timedelta(minutes = blocktime)
                            db.child('table1time').set(str(table1time))

                if timenow.time()>table2time.time():
                    next_state='table 1 occupied'
                    db.child('table2time').set("Empty")
                    db.child("name2").set('')
                    update_next_row(next_state,self.count)
                    self.count+=1

                elif timenow.time()>table1time.time():
                    next_state='table 2 occupied'
                    db.child('table1time').set("Empty")
                    db.child("name1").set('')
                    update_next_row(next_state,self.count)
                    self.count+=1
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
