"# digitalworld2d - F07 Group"

Background:

Singapore University of Technology and Design (SUTD) is gearing towards being the heart of Smart Nation by building a Smart Campus that utilises technology, networks and big data.

Problem Statement:
Students often find searching for empty common rooms tedious as they have to manually check all the individual rooms in the hostel. Not only time-consuming, it is often mentally draining when one has searched the entire block yet found no available room. Hence, our group identified THE INABILITY TO CHECK THE AVAILABILITY OF COMMON ROOMS IN SUTD HOUSING as our problem.

In this 1D project, we aim to develop an application which informs the student population of the availability status of common rooms in the hostel through the application of sensor technology.


1. card.py
This code allows table users to tap their cards on the RFID readers to automatically update their name in Firebase under the corresponding table's values.

2. usir.py
This code collates all the readings from both ultrasonic and infrared sensors, processes the data and updates it accordingly in Firebase.

3. checker.py
This code gathers all the data from firebase and handles the logic for it creating states such that the rooms will be emptied when there is a prolonged period where the sensors do not detect people. It also updates the data on google spreadsheet and firebase.

4. 1D code.py
This is our GUI script to display real-time data of the availability of tables and the name of the table occupants, retrieved from Firebase.

5. telegrambot.py
This is our script to run the SUTDROOMbot in Telegram. The application allows users to interact with it to check availability of room tables.

6. rfid write.py
This is an online code to write an RFID card.

7. Defunc Folder
This folder contains codes that was meant to combine usir.py and card.py however processes does not run well on rpi.


 To run our files: you will need to install modules
 1.libdw
 2.mfrc522
 3.gspread
 4.oauth2client
 5.telepot
 6.spidev
 7.kivy
 and have a file named secrets with your credentials for telegram bot and firebase.(provided for grading)
 We will als need a json file named client_secret for the credentials of google spreadsheet(also provided for grading)

to run bash script ,use command line interface
1. cd to directory of bash file, eg.(~/ $ cd digitalworld1d)
2. run chmod +x install.sh(eg. ~/ $ chmod +x install.sh)
3. run ./install.sh(eg. ~/ $ ./install.sh)
this is to install all dependencies together(except libdw and kivy)

4. enable spi using raspi-config(eg. ~/ $ sudo raspi-config)
5. go to option 5 - Interfacing Options
6. go to option P5 - spi and select 'yes' to enable spi
7. reboot rpi (eg. ~/ $ sudo reboot)
