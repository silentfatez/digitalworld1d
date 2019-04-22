# -*- coding: utf-8 -*-
"""
Created on Wed Apr 10 13:25:54 2019

@author: ato
"""
#firebase
from libdw import pyrebase

#kivy
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.dropdown import DropDown
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.clock import Clock

Window.clearcolor=(1,1,1,1)

Builder.load_string("""
#:import Factory kivy.factory.Factory                
<MyPopup@Popup>:
    auto_dismiss: False
    title: "Instructions"   
    title_size: 48
    Button:
        
        text: 'Check Availability >> Select Location: \
        \\n \
            \\n View availability of your room of choice and other possible locations\
            \\n \
        \\n Select button to change the availability of the table/room after you leave\
        \\n \\n \
        \\n Click anywhere to close'
        font_size: 20
        on_release: root.dismiss()
        
<Menu>:                         
    FloatLayout:
        Label:
            text: 'Menu'
            font_size: 48
            pos_hint: {'center_x': 0.5, 'center_y':0.9}
            size_hint: 0.3, 0.2
            color: 0.2,0.4,0.8,1
            
        Button:
            text: 'Check availability'
            font_size: 25
            pos_hint: {'center_x':0.5, 'center_y': 0.7}
            size_hint: 0.5, 0.15
            on_press: root.manager.current = "location"
            
        Button:
            text: 'Help'
            on_release: Factory.MyPopup().open()
            font_size: 25
            pos_hint: {'center_x':0.5, 'center_y': 0.5}
            size_hint: 0.5, 0.15    
        
        Button:
            text: 'Quit'
            font_size: 25
            pos_hint: {'center_x':0.5, 'center_y': 0.3}
            size_hint: 0.5, 0.15
            on_press: app.get_running_app().stop()

<Location>:
    
    FloatLayout:
        Label:
            text: 'Select Location'
            font_size: 48
            pos_hint: {'center_x': 0.5, 'center_y':0.9}
            size_hint: 0.3, 0.2
            color: 0.2,0.4,0.8,1
            
        Button:
            text: 'Block 55'
            font_size: 25
            pos_hint: {'center_x':0.5, 'center_y': 0.7}
            size_hint: 0.5, 0.15
        
        Button: 
            text: 'Block 57'
            font_size: 25
            pos_hint: {'center_x':0.5, 'center_y': 0.5}
            size_hint: 0.5, 0.15
            
        Button:
            text: 'Block 59'
            font_size: 25
            pos_hint: {'center_x':0.5, 'center_y': 0.3}
            size_hint: 0.5, 0.15
            
        Button:
            text: 'Others'
            font_size: 25
            pos_hint: {'center_x':0.5, 'center_y': 0.1}
            size_hint: 0.5, 0.15
            on_press: root.manager.current = "check_others"
            
        
        Button:
            text: '< Back'
            font_size: 25
            pos_hint: {'x':0, 'y': 0.9}
            size_hint: 0.2, 0.1
            background_color: (0,0,0,0.1)
            color: (0,0,0,1)
            on_press: root.manager.current = "menu"


<Check_others>:
    
    FloatLayout:
        
        Label: 
            text:'Cohort Classroom 7'
            font_size: 48
            pos_hint: {'center_x': 0.5, 'center_y':0.9}
            size_hint: 0.3, 0.2
            color: 0,0,0,1
            
        Label:
            text: 'Mini Think Tank'
            font_size: 25
            pos_hint: {'center_x':0.2, 'center_y': 0.5}
            size_hint: 0.3, 0.2
            color: 0,0,0,1
            
       
            
        Button: 
            id: others1
            text:root.db.child("table1").get().val()
            on_press: root.edit_others1()
            font_size: 25
            pos_hint: {'center_x':0.5, 'center_y': 0.5}
            size_hint: 0.3, 0.2
            background_normal: ''
            background_color: (0,1,0,0.8) if self.text == "Empty" else (1,0,0,0.8)
            
        Label: 
            id: others1_name
            text: root.db.child("name1").get().val()
            font_size: 25
            pos_hint: {'center_x':0.6, 'center_y': 0.44}
            size_hint: 0.15, 0.1
            color: 0,0,0,1
            
        Button: 
            id: others2
            text:root.db.child("table2").get().val()
            on_press: root.edit_others2()
            font_size: 25
            pos_hint: {'center_x':0.8, 'center_y': 0.5}
            size_hint: 0.3, 0.2
            background_normal: ''
            background_color: (0,1,0,0.8) if self.text == "Empty" else (1,0,0,0.8)
            
        Label: 
            id: others2_name
            text:root.db.child("name2").get().val()
            font_size: 25
            pos_hint: {'center_x':0.9, 'center_y': 0.44}
            size_hint: 0.15, 0.1
            color: 0,0,0,1
            
        Label:
            text: 'Table 1'
            font_size: 25
            pos_hint: {'center_x':0.41, 'center_y': 0.57}
            size_hint: 0.15, 0.1
            color: 0,0,0,1
            
        Label:
            text: 'Table 2'
            font_size: 25
            pos_hint: {'center_x':0.71, 'center_y': 0.57}
            size_hint: 0.15, 0.1
            color: 0,0,0,1
            
        Button:
            text: '< Back'
            font_size: 25
            pos_hint: {'x':0, 'y': 0.9}
            size_hint: 0.2, 0.1
            background_color: (0,0,0,0.1)
            color: (0,0,0,1)
            on_press: root.manager.current = "location"
            
        

       
            
    
            
""")
    
class Menu(Screen):
#    def to_location(self,instance):
#        self.root.current = "location"
    pass

class Location(Screen):
    pass

class Check_others(Screen):
    url = 'https://digital-world-7e769.firebaseio.com/' # URL to Firebase database
    apikey = 'AIzaSyCVVMEWalJspTvfx4fnWS2HTyZWSozb8Xo' # unique token used for authentication

    config={
            "apiKey":apikey,
            "databaseURL":url,
            }
    firebase = pyrebase.initialize_app(config)
    db = firebase.database()
    
    #Clock.schedule_interval(check_update(),5)
        
    def edit_others1(self):
        if self.ids.others1.text == "Occupied":
            self.ids.others1.text = "Empty"
            self.ids.others1_name.text = ""
            
        else:
            self.ids.others1.text = "Occupied"
            self.ids.others1_name.text = self.db.child("name1").get().val()
            
        self.db.child("table1").set(self.ids.others1.text)
        self.db.child("name1").set(self.ids.others1_name.text)
        
    def edit_others2(self):
        if self.ids.others2.text == "Occupied":
            self.ids.others2.text = "Empty"
            
        else:
            self.ids.others2.text = "Occupied"
            
        self.db.child("table2").set(self.ids.others2.text)
        
    def check_update(self,*args):
        self.ids.others1.text == self.db.child("table1").get().val()
        self.ids.others1_name.text == self.db.child("name1").get().val()
        
        
    #State= 'Available'
    

#class LocationDropDown(DropDown):
#    def build(self):
#        mainbutton=Button(text='text')
#        return mainbutton
#
#class DropDownScreen(Screen):
#    def buil(self):
#        return LocationDropDown
#    
#    def build(self):
#        mainbutton = Button(text='test')
#        dropdown = LocationDropDown()
#        mainbutton = Button(text='Hello', size_hint=(0.3, 0.1), pos_hint={'center_x': 0.5, 'center_y':0.9})
#        mainbutton.bind(on_release=dropdown.open)
#        dropdown.bind(on_select=lambda instance, x: setattr(mainbutton, 'text', x))
#        return mainbutton
        

#creating screen manager
sm = ScreenManager()
sm.add_widget(Menu(name='menu'))
sm.add_widget(Location(name='location'))
sm.add_widget(Check_others(name='check_others'))
#sm.add_widget(DropDownScreen(name='drop'))
sm.current = 'menu' #changes first screen for testing



class KivyApp (App):
    
    def build(self):
        Clock.schedule_interval(Check_others().check_update,5)
        return sm  
        
            
if __name__=='__main__':
    KivyApp().run()
        
        