import tkinter as tk
from tkcalendar import Calendar
from tkinter import ttk,messagebox
import datetime,time
#import serial



#port='COM4'
#ser=serial.Serial(port,9600)

class MainWindow(tk.Frame):

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

        # Label widget
        speedLabel = tk.Label(self.master,text="Speed")
        speedLabel.place(x=390,y=508)
        starLabel = tk.Label(self.master,text="Stars")
        starLabel.place(x=50,y=340)
        constellationLabel = tk.Label(self.master,text="Constellation")
        constellationLabel.place(x=170,y=340)
        
        # create menu
        menu = Menu(self.master)
        menu.createStarsMenu()
        menu.createConstellationMenu()
        
        

class Menu():
    def __init__(self,master):
        self.master=master

    def createStarsMenu(self):
        
        self.starList = [
        "None",
        "Star1",
        "Star2",
        "Star3",
        "Star4"
        ] 

        self.stars = tk.StringVar(self.master)
        self.stars.set(self.starList[0])

        opt = tk.OptionMenu(self.master, self.stars, *self.starList)
        opt.config(width=8, font=('Helvetica', 12))
        opt.place(x=15,y=360)
        
        self.stars.trace("w", self.callback) # trace to attach observer on variable

    def createConstellationMenu(self):
        self.constellationList = [
        "None",
        "const1",
        "const2",
        "const3",
        "const4"
        ] 

        self.constellation = tk.StringVar(self.master)
        self.constellation.set(self.constellationList[0])

        opt = tk.OptionMenu(self.master, self.constellation, *self.constellationList)
        opt.config(width=8, font=('Helvetica', 12))
        opt.place(x=150,y=360)
        
        self.constellation.trace("w", self.callback) # trace to attach observer on variable

    def callback(self,*args):
        print(self.stars.get())
        print(self.constellation.get())
        

class windowLayout():
    def __init__(self,master):
        # Variable
        self.master=master

    def createWindowLayout(self):    # method to create the layout of the GUI
        self.windowLayout1= tk.Label(self.master,borderwidth=1,relief='solid',width=50,height=27)
        self.windowLayout1.place(x=10,y=330)
        self.windowLayout2= tk.Label(self.master,borderwidth=1,relief='solid',width=110,height=38)
        self.windowLayout2.place(x=380,y=10)
        self.windowLayout3= tk.Label(self.master,borderwidth=1,relief='solid',width=110,height=8)
        self.windowLayout3.place(x=380,y=600)
        self.windowLayout4= tk.Label(self.master,borderwidth=1,relief='solid',width=110,height=5)
        self.windowLayout4.place(x=380,y=505)


#global namespace
minuteEntry=None
calendar=None
hourEntry=None

class CalendarWindow():
   
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
        return date
     

    def timeSetting(self):
        global minuteEntry
        global hourEntry

        # create the Entries 
        hourEntry = tk.Entry( relief = "ridge", bd = 5, width = 4)
        hourEntry.place(x = 140, y = 250)
        hourEntry.insert(0, 0)
        minuteEntry = tk.Entry( relief = "ridge", bd = 5, width = 4)
        minuteEntry.place(x = 180, y = 250)
        minuteEntry.insert(0, 0)

        # button
        self.getDateTimeButton=tk.Button(text="confirm",width=10,command=self.getDateTime)
        self.getDateTimeButton.place(x=140,y=280) 

    def getDateTime(self):
        # print the date and time
        print(self.getCalendarValue())
        print(self.getTime())
      

    def getTime(self):
        try:
            return self._filterTimeEntry() # check if entry is a valid time
        except ValueError:
            #Handle the exception
            messagebox.showinfo("Error", "Time is not valid")
    
    def _addSpeed(self,speed):
        # add the value from the speed to the minuteEntry
        minuteValue=int(minuteEntry.get()) + speed
        self._updateEntry(minuteValue)


    def _updateEntry(self,minuteValue):
        
        if(minuteValue>=60 ):    # if minuteValue is over or equal to 60
            minutes=minuteValue-60            
            currentHours=int(hourEntry.get())+1 # add 1 to the hour
            hourEntry.delete(0,'end')       # delete the entry
            hourEntry.insert(0,currentHours)    # insert the currentHours into the entry

        elif(minuteValue<0 ):    # if minuteValue is under 0
            minutes = 60+minuteValue     
            currentHours=int(hourEntry.get())-1 # decrement hour by 1
            hourEntry.delete(0,'end')       # delete the entry
            hourEntry.insert(0,currentHours)    # insert the currentHours into the entry
        else: 
            minutes=minuteValue 

        

        if(int(hourEntry.get())<0 ):   

            # get the day,month and year from the calendar widget
            day=calendar.selection_get().day
            month=calendar.selection_get().month
            year=calendar.selection_get().year
            
            # get the previous date
            date = self.prevDate(year,month,day)
            
            # change String to datetime and update the calendar
            datetime_object = datetime.datetime.strptime(date, '%Y/%m/%d') 
            calendar.selection_set(datetime_object)

            #reset the hours
            hourEntry.delete(0,'end')
            hourEntry.insert(0,23)
        
        if(int(hourEntry.get())>=24 ):   #if hourEntry is above 24

            # get the day,month and year from the calendar widget
            day=calendar.selection_get().day
            month=calendar.selection_get().month
            year=calendar.selection_get().year
            
            # get the next date
            date = self.nextDate(year,month,day)
         
            # change String to datetime and update the calendar
            datetime_object = datetime.datetime.strptime(date, '%Y/%m/%d') 
            calendar.selection_set(datetime_object)

            #reset the hours
            hourEntry.delete(0,'end')
            hourEntry.insert(0,0)

        # update the minuteEntry
        minuteEntry.delete(0,'end') 
        minuteEntry.insert(0,minutes)

        self.getDateTime()

    def prevDate(self,year,month,day):

        if(day==1):
            if(month==1):
                month=12
                year-=1
            else:
                month-=1

            if(month == 1 or month == 3 or month == 5 or month == 7 or month == 8 or month == 10 or month == 12):
                day=31

            if(month == 4 or month == 6 or month == 9 or month == 11):
                day=30

            if(month==2):
                if(self._isLeap(year)):
                    day=29
                else:
                    day=28
        else:
            day-=1

        datetime_str = f'{year}/{str(month).zfill(2)}/{str(day).zfill(2)}'  # str().zfill(2) is to change from 1 digit to 2 digits
        return datetime_str  
       

    def nextDate(self,year,month,day): # algorithm to calculate the next date
        
        if(month == 1 or month == 3 or month == 5 or month == 7 or month == 8 or month == 10 or month == 12):
            maxDays=31
           
        if(month == 4 or month == 6 or month == 9 or month == 11):
            maxDays=30

        if(month==2):
            if(self._isLeap(year)):
                maxDays=29
            else:
                maxDays=28  
        
        if(day==maxDays):
            day = 1

            if(month == 12):
                month = 1
                year = year + 1   
                
            else:
                month = month + 1
        else:
            day = day + 1

        datetime_str = f'{year}/{str(month).zfill(2)}/{str(day).zfill(2)}'  # str().zfill(2) is to change from 1 digit to 2 digits
        return datetime_str   

    def _isLeap(self,year):
        
        if(year%4==0):
            return True
        else:
            return False

    def _filterTimeEntry(self): 
        # check if the hourEntry and minutes are integers
        i = int(hourEntry.get())
        i = int(minuteEntry.get()) 

        if(int(hourEntry.get()) <= 24 and int(hourEntry.get())>=0 ):    # check if hourEntry is between 0 and 24
            if(int(minuteEntry.get()) <=59 and int(minuteEntry.get())>=0):  # check if minuteEntry is between 0 and 60
                if( int( hourEntry.get()) == 24 and  int(minuteEntry.get ()) > 0):  # check if time is not above 24 hourEntry
                    messagebox.showinfo("Error", "Time is not valid")
                else:       # time is valid
                    time = f'{str(hourEntry.get()).zfill(2)}:{str(minuteEntry.get()).zfill(2)}' # change 1 digit to 2 digits. 3 -> 03.  
                    return time
            else:        
                messagebox.showinfo("Error", "Time is not valid")    
        else:
             messagebox.showinfo("Error", "Time is not valid")    
              

class Button():
    def __init__(self, master,controller=None): # we use controller to get the value from the spinBox widget from the MainWindow class
        # Variables
        self.controller=controller 
        self.master=master
        self.calendar= CalendarWindow()   
        
        # create Buttons and place it on the window
        playButton= tk.Button(self.master,text=">", width=5,command= self.play)
        playButton.place(x=690,y=530)
        pauseButton=tk.Button(self.master, text= " ||", width=5,command= self.pause)
        pauseButton.place(x=640,y=530)
        rewindButton=tk.Button(self.master, text= "<<", width= 5, command = self.rewind)
        rewindButton.place(x=590,y=530)
        fastforwardButton=tk.Button(self.master,text=">>",width=5,command=self.fastforward)
        fastforwardButton.place(x=740,y=530)

    def fastforward(self):          

      
        if(self.getSpinboxValue() == "0.1"):
            fastForwardSpeed=1
        if(self.getSpinboxValue() == "0.2"):
            fastForwardSpeed=2
        if(self.getSpinboxValue() == "0.3"):
            fastForwardSpeed=3
        if(self.getSpinboxValue() == "0.4"):
            fastForwardSpeed=4  
        
        self.calendar._addSpeed(fastForwardSpeed)   

    def rewind(self):
 
        if(self.getSpinboxValue() == "0.1"):
            rewindSpeed= -1
        if(self.getSpinboxValue() == "0.2"):
            rewindSpeed= -2
        if(self.getSpinboxValue() == "0.3"):
            rewindSpeed= -3
        if(self.getSpinboxValue() == "0.4"):
            rewindSpeed= -4  
                
        self.calendar._addSpeed(rewindSpeed)

    def play(self):
        pass
 
    def pause(self):
        print("pause")

    def getSpinboxValue(self):
        self.value=self.controller.get() # get the spinBox value
        return self.value
        
        
        

window = tk.Tk()
window.geometry("1200x750")
window.title("GUI")
window.resizable(False,False) #disable resizable
application = MainWindow(window)
application.createObject()
window.mainloop()

