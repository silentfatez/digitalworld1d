import time
import random
import datetime
import telepot
from telepot.loop import MessageLoop
from libdw import pyrebase
from secrets import *

"""
url = firebasesecrets['url'] # URL to Firebase database
apikey = firebasesecrets['apikey'] # unique token used for authentication

config={
    "apiKey":apikey,
    "databaseURL":url,
}
firebase = pyrebase.initialize_app(config)
db = firebase.database()


def handle(msg):
    chat_id = msg['chat']['id']
    command = msg['text']
    alert='Got Command '+command

    print (alert)
    if command=='/help':
        Message='Hi,welcome to table checker. You can type /help for some help.'
    elif command=='/start':
         Message='Looks like you need some help. You can check the status of table 1 using /table1 and table 2 using /table2. You can also use /alltables to get an update on all tables available.'

    elif command=='/alltables':
        name1=db.child('name1').get().val()
        name2=db.child('name2').get().val()
        if name1 != '':
            submessage1='Table 1 is Occupied by '+name1
        else:
            submessage1='Table 1 is Empty'
        if name2 !="":
            submessage2='Table 2 is Occupied by '+name2
        else:
            submessage2='Table 2 is Empty'
        Message=submessage1+' and '+submessage2
    elif command == '/table1':
        name1=db.child('name1').get().val()
        if name1 != '':
            Message='Table 1 is Occupied by '+name1
        else:
            Message='Table 1 is Empty'
    elif command == '/table2':
        name2=db.child('name2').get().val()
        if name2 != '':
            Message='Table 2 is Occupied by '+name2
        else:
            Message='Table 2 is Empty'

    bot.sendMessage(chat_id, str(Message))

bot = telepot.Bot(TOKEN)

MessageLoop(bot, handle).run_as_thread()
print ('I am listening ...')

while 1:
    time.sleep(10)
