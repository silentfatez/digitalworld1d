import time
import random
import datetime
import telepot
from telepot.loop import MessageLoop
from libdw import pyrebase
from secrets import *

"""
After **inserting token** in the source code, run it:
```
$ python2.7 diceyclock.py
```
[Here is a tutorial](http://www.instructables.com/id/Set-up-Telegram-Bot-on-Raspberry-Pi/)
teaching you how to setup a bot on Raspberry Pi. This simple bot does nothing
but accepts two commands:
- `/roll` - reply with a random integer between 1 and 6, like rolling a dice.
- `/time` - reply with the current time, like a clock.
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

    print ('Got command')

    if command == '/table1':
        table1time=db.child('table1time').get().val()
        name1=db.child('name1').get().val()

        bot.sendMessage(chat_id, str((table1time,name1)))
    elif command == '/table2':
        table2time=db.child('table2time').get().val()
        name2=db.child('name2').get().val()


        bot.sendMessage(chat_id, str((table2time,name2)))
bot = telepot.Bot(TOKEN)

MessageLoop(bot, handle).run_as_thread()
print ('I am listening ...')

while 1:
    time.sleep(10)
