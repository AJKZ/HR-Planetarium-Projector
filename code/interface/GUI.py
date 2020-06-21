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
        
        # Button objects
        confirmButton= Button(self.master)
        playButton= Button(self.master)
        pauseButton= Button(self.master)
        rewindButton= Button(self.master)

        # CalendarWindow object
        openCalendar = CalendarWindow()
        openCalendar.calendarSetting()
        openCalendar.timeSetting()

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
    def calendarSetting(self):
        # min and max date
        mindate = datetime.date(year=2000, month=1, day=21)
        maxdate = datetime.date(year=3000, month=12, day=30)
        
        # calendar settings
        self.calendar = Calendar( font="Arial 14", selectmode='day', locale='en_US',
                    mindate=mindate, maxdate=maxdate, 
                    cursor="hand2", year=2020, month=1, day=1)    
        self.calendar.place(x=0,y=0)
   
        
    def getCalendarValue(self):
            
        date = self.calendar.selection_get().strftime("%d-%m-%Y") #change datetime to string
        print (date)
        if(date=="01-01-2020"):
            print("Nice its a string")

    def timeSetting(self):
        self.hour = tk.Entry( relief = "ridge", bd = 5, width = 4)
        self.hour.place(x = 140, y = 250)
        self.hour.insert(0, 0)
        self.minute = tk.Entry( relief = "ridge", bd = 5, width = 4)
        self.minute.place(x = 180, y = 250)
        self.minute.insert(0, 0)

        self.getTimebutton=tk.Button(text="confirm",width=10,command=lambda:[self.getTime(),self.getCalendarValue()])# a command that calls 2 methods
        self.getTimebutton.place(x=140,y=280)

    def getTime(self):
        
        try:
            self._filterTimeEntry() # check if entry is a valid time
        except ValueError:
            #Handle the exception
            messagebox.showinfo("Error", "Time is not valid")

    def _filterTimeEntry(self): 
        # check if the hour and minutes are integers
        i = int(self.hour.get())
        i = int(self.minute.get())


        if(int(self.hour.get()) <= 24 and int(self.hour.get())>=0 ):    # check if hour is between 0 and 24
            if(int(self.minute.get()) <=59 and int(self.minute.get())>=0):  # check if minute is between 0 and 60
                if( int( self.hour.get()) == 24 and  int(self.minute.get ()) > 0):  # check if time is not above 24 hour
                    messagebox.showinfo("Error", "Time is not valid")
                else:       # time is valid
                    print(self.hour.get().zfill(2)+":"+ self.minute.get().zfill(2))  # change 1 digit to 2 digits. 3 -> 03.  
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
            
            print("1 is true")
            #ser.write(str.encode('1'))
            #print(ser.read())
            
        if(self.checkValue2.get()==True):
            print("2 is true")
            #ser.write(str.encode('2'))
            
        if(self.checkValue3.get()==True):
            print("3 is true")


class Button():
    def __init__(self, master,controller=None): # we use controller to get the value from the spinBox widget from the MainWindow class
        # Variables
        self.controller=controller 
        self.master=master
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
        print("fast forward")        
    def rewind(self):
        print("rewind")

    def play(self):
        print("playing")
 
    def pause(self):
        print("pause")

    def getSpinboxValue(self):
        value=self.controller.get() # get the spinBox value
        print(value)
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
