# new: function from fastforward button works.


import tkinter as tk
from tkcalendar import Calendar
from tkinter import ttk,messagebox
import datetime,time
import serial


port='COM4'
#ser=serial.Serial(port,9600)

class MainWindow():

    def __init__(self, master): 
        
        # Variable
        self.master = master

    def createObject(self):

        # these objects are used to organize the windows
        WindowLayout = windowLayout(self.master)
        WindowLayout.createWindowLayout()
        
        # CalendarWindow object
        openCalendar = CalendarWindow()
        openCalendar.calendarSetting()
        openCalendar.timeSetting()


        # Button objects
        confirmButton= Button(self.master)
        playButton= Button(self.master)
        pauseButton= Button(self.master)
        rewindButton= Button(self.master)

        # spinBox widget
        spinBox= tk.Spinbox(self.master,from_=0.1, to=0.4,state="readonly" ,increment=0.1)    #spinBox value only from 0.1 to 0.4
        spinBox.place(x=390,y=527)
        spinBox= Button(self.master,spinBox)

        # Checkbox objects
        checkBox = Checkbox(self.master)
        checkBox.createCheckbox()

        # Label widget
        label = tk.Label(self.master,text="Speed")
        label.place(x=390,y=508)

class windowLayout():
    def __init__(self,master):
        # Variable
        self.master=master

    def createWindowLayout(self):    # method to create the layout of the GUI
        self.windowLayout1= tk.Label(self.master,borderwidth=1,relief='solid',width=50,height=25)
        self.windowLayout1.place(x=10,y=330)
        self.windowLayout2= tk.Label(self.master,borderwidth=1,relief='solid',width=110,height=38)
        self.windowLayout2.place(x=380,y=10)
        self.windowLayout3= tk.Label(self.master,borderwidth=1,relief='solid',width=110,height=8)
        self.windowLayout3.place(x=380,y=600)
        self.windowLayout4= tk.Label(self.master,borderwidth=1,relief='solid',width=110,height=5)
        self.windowLayout4.place(x=380,y=505)



class CalendarWindow():
    def __init__(self):
        pass

    def calendarSetting(self):

        
        # min and max date
        mindate = datetime.date(year=2000, month=1, day=21)
        maxdate = datetime.date(year=3000, month=12, day=30)
        
        # calendar settings
        global calendar
        calendar = Calendar( font="Arial 14", selectmode='day', locale='en_US',
                    mindate=mindate, maxdate=maxdate ,
                    cursor="hand2", year=2020, month=1, day=1)    
        calendar.place(x=0,y=0)
    
    

        
    def getCalendarValue(self):
         
        date = calendar.selection_get().strftime("%d-%m-%Y") #change datetime to string
        print(date)
        #if(date=="01-01-2020"):
        #    print("Nice its a string")

    

    def timeSetting(self):
        global minuteEntry
        global hourEntry

        hourEntry = tk.Entry( relief = "ridge", bd = 5, width = 4)
        hourEntry.place(x = 140, y = 250)
        hourEntry.insert(0, 0)

        minuteEntry = tk.Entry( relief = "ridge", bd = 5, width = 4)
        minuteEntry.place(x = 180, y = 250)
        minuteEntry.insert(0, 0)

        self.getDateTimeButton=tk.Button(text="confirm",width=10,command=lambda:[self.getTime(),self.getCalendarValue()])# a command that calls 2 methods
        self.getDateTimeButton.place(x=140,y=280) 

    def getTime(self):
        
        try:
            self._filterTimeEntry() # check if entry is a valid time
        except ValueError:
            #Handle the exception
            messagebox.showinfo("Error", "Time is not valid")
    
    def forward(self,fastForwardSpeed):
        # add the value from the fastForwardSpeed to the minuteEntry
        minuteValue=int(minuteEntry.get())+fastForwardSpeed
        self._updateEntry(minuteValue)
        self.getCalendarValue()
        self.getTime()


    def _updateEntry(self,minuteValue):
    
        if(minuteValue>=60):    # if minuteValue is over the 60
            minutes=minuteValue-60      
            currentHours=int(hourEntry.get())+1 # add 1 to the hour
            hourEntry.delete(0,'end')       # delete the entry
            hourEntry.insert(0,currentHours)    # insert the currentHours into the entry
        else: 
            minutes=minuteValue

        if(int(hourEntry.get())>=24):   #if hourEntry is above 24
            # get the day,month and year from the calendar widget
            day=calendar.selection_get().day
            month=calendar.selection_get().month
            year=calendar.selection_get().year
            
            # get the next date
            date = self.nextDate(year,month,day)
            print(date)

            # change String to datetime and update the calendar
            datetime_object = datetime.datetime.strptime(date, '%Y/%m/%d') 
            calendar.selection_set(datetime_object)

            #reset the hours
            hourEntry.delete(0,'end')
            hourEntry.insert(0,0)    
        
        # update the minuteEntry
        minuteEntry.delete(0,'end') 
        minuteEntry.insert(0,minutes)

        
    def nextDate(self,year, month, day):# calculate the next date
            
        day = day + 1 if day < 30 else 1

        if day == 1:
            if month == 12:
               month = 1
            else:
                month = month + 1
    
        year = year + 1 if month == 1 and day == 1 else year
        datetime_str = f'{year}/{str(month).zfill(2)}/{str(day).zfill(2)}'  # str().zfill(2) is to change from 1 digit to 2 digits
        return datetime_str   


    def _filterTimeEntry(self): 
        # check if the hourEntry and minutes are integers
        i = int(hourEntry.get())
        i = int(minuteEntry.get()) 


        if(int(hourEntry.get()) <= 24 and int(hourEntry.get())>=0 ):    # check if hourEntry is between 0 and 24
            if(int(minuteEntry.get()) <=59 and int(minuteEntry.get())>=0):  # check if minuteEntry is between 0 and 60
                if( int( hourEntry.get()) == 24 and  int(minuteEntry.get ()) > 0):  # check if time is not above 24 hourEntry
                    messagebox.showinfo("Error", "Time is not valid")
                else:       # time is valid
                    print(hourEntry.get().zfill(2)+":"+ minuteEntry.get().zfill(2))  # change 1 digit to 2 digits. 3 -> 03.  
            else:        
                messagebox.showinfo("Error", "Time is not valid")    
        else:
             messagebox.showinfo("Error", "Time is not valid")    
              
            

class Checkbox():
    def __init__(self,master):
        # Variable
        self.master=master

    def createCheckbox(self):
        # checkBox hold a Boolean
        self.checkValue1 = tk.BooleanVar()
        self.checkValue2 = tk.BooleanVar()
        self.checkValue3 = tk.BooleanVar()
        # initialise the checkboxes
        self.checkBox1 = tk.Checkbutton(self.master,text = "HighLight 1",var=self.checkValue1,command= self.checkValue)
        self.checkBox2 = tk.Checkbutton(self.master,text = "HighLight 2",var=self.checkValue2,command= self.checkValue)
        self.checkBox3 = tk.Checkbutton(self.master,text = "HighLight 3",var=self.checkValue3,command= self.checkValue)
        # place the checkboxes on the MainWindow
        self.checkBox1.place(x=13,y=340)
        self.checkBox2.place(x=13,y=360)
        self.checkBox3.place(x=13,y=380)
            
    def checkValue(self): # check the checkBox value
        if(self.checkValue1.get()==True):
        #    ser.write(str.encode('1'))
            pass
        else:
         #   ser.write(str.encode('2'))
            pass
            
        if(self.checkValue2.get()==True):
         #   ser.write(str.encode('3'))
            pass
        else:
         #   ser.write(str.encode('4'))
            pass
        if(self.checkValue3.get()==True):
           pass


class Button():
    def __init__(self, master,controller=None): # we use controller to get the value from the spinBox widget from the MainWindow class
        # Variables
        self.controller=controller 
        self.master=master
        self.calendar= CalendarWindow()   
        

        # create Buttons and place it on the window
        confirmButton=tk.Button(self.master, text = 'Confirm', width = 8,command=self.getSpinboxValue)
        confirmButton.place(x=390,y=550)
        playButton= tk.Button(self.master,text=">", width=5,command= self.play)
        playButton.place(x=690,y=530)
        pauseButton=tk.Button(self.master, text= " ||", width=5,command= self.pause)
        pauseButton.place(x=640,y=530)
        rewindButton=tk.Button(self.master, text= "<<", width= 5, command = self.rewind)
        rewindButton.place(x=590,y=530)
        fastforwardButton=tk.Button(self.master,text=">>",width=5,command=self.fastforward)
        fastforwardButton.place(x=740,y=530)

    def fastforward(self):          

        if(self.controller.get() == "0.1"):
            fastForwardSpeed=1
        if(self.controller.get() == "0.2"):
            fastForwardSpeed=2
        if(self.controller.get() == "0.3"):
            fastForwardSpeed=3
        if(self.controller.get() == "0.4"):
            fastForwardSpeed=4  
                
        self.calendar.forward(fastForwardSpeed)    # calls the _updateEntry from the calendarWindow class

        

    def rewind(self):
        print("rewind")

    def play(self):
        pass
 
    def pause(self):
        print("pause")

    def getSpinboxValue(self):
        self.value=self.controller.get() # get the spinBox value
        print(self.value)
        #ser.write(str.encode(value))
        
        
        
# def GUI(): 
    # settings for the MainWindow
window = tk.Tk()
window.geometry("1200x750")
window.title("GUI")
window.resizable(False,False) #disable resizable
application = MainWindow(window)
application.createObject()
window.mainloop()

# if __name__ == '__main__':
#         GUI()
