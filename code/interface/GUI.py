import tkinter as tk
from tkcalendar import Calendar
from tkinter import ttk,messagebox
import datetime,time
from ttkwidgets import CheckboxTreeview
import numpy as n
import pandas as p
from pyopengltk import OpenGLFrame
from OpenGL import GL, GLU
import sys, math


# Helper functions used to convert coordinates
# Source: https://github.com/numpy/numpy/issues/5228
def cart2sph(self,x, y, z):
    hxy = n.hypot(x, y)
    r = n.hypot(hxy, z)
    el = n.arctan2(z, hxy)
    az = n.arctan2(y, x)
    return az, el, r

def sph2cart(az, el, r):
    rcos_theta = r * n.cos(el)
    x = rcos_theta * n.cos(az)
    y = rcos_theta * n.sin(az)
    z = r * n.sin(el)
    return x, y, z
# End helper function section (a.k.a. only this part is copy/pasted)

# Convert climb/right ascension to degrees
# Time has to be formatted in "HH MM SS"
def time2deg(time):
    time = str(time)
    RA, rs = '', 1
    H, M = [float(i) for i in time.split('.')]

    if str(H)[0] == '-':
        rs, H = -1, abs(H)
    
    deg = (H*15) + (M/4)# + (S/240)
    RA = '{0}'.format(deg*rs)

    return RA


oGLWindow = None
class MainWindow(tk.Frame):
   
    def __init__(self, master): 
        # Variable
        self.master = master

    def createObject(self):

        # organize the window
        windowLayout1= tk.Label(self.master,borderwidth=1,relief='solid',width=110,height=6)
        windowLayout1.place(x=380,y=540)
        
        # CalendarWindow object
        openCalendar = CalendarWindow()
        openCalendar._calendarSetting()
        openCalendar._timeSetting()

        # Button objects
        confirmButton= Button(self.master)
        playButton= Button(self.master)
        pauseButton= Button(self.master)
        rewindButton= Button(self.master)

        # spinBox widget
        spinBox= tk.Spinbox(self.master,from_=0.1, to=0.4,state="readonly" ,increment=0.1)    #spinBox value only from 0.1 to 0.4
        spinBox.place(x=390,y=562)
        spinBox= Button(self.master,spinBox)

        # Label widget
        label = tk.Label(self.master,text="Speed")
        label.place(x=390,y=543)
        
        # treeview object
        tree = Treeview(self.master)
        tree._createTreeview()
        tree._createSimulateButton()

        f = tk.Frame(self.master) # create a frame 
        f.place(x=380,y=15)
        global oGLWindow
        oGLWindow = OpenGLWindow(f,width=775, height=523)  # put the OpenGLWindow in the frame from tkinter
        oGLWindow.animate=1 #without this, simulation doesnt work
        oGLWindow.pack() # pack it

        
    def getOpenGLWindow(self): # return the openGLWindow object
        return oGLWindow


class TextBox():

    def __init__(self,master):
        self.master = master
        
    def createTextBoxAndScrollbar(self):
       
        #create a textbox
        self.tb = tk.Text(self.master, height=40, width=35)
        self.tb.place(x=1170,y=10)

        #create a scrollbar
        scrollbar = tk.Scrollbar(self.master)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)    # place the scrollbar on the right side
        scrollbar.config(command=self.tb.yview)    
        self.tb.config(yscrollcommand=scrollbar.set) # attach the scrollbar to the textbox
        
        


class OpenGLWindow(OpenGLFrame):
    # list to save the data
    xList = []
    yList = []

    minX=-1000000
    maxX= 1000000
    minY=-1000000
    maxY= 1000000
    zoomedOut=True

    def initgl(self):
        GL.glViewport(0, 0, self.width, self.height)    
        GL.glClearColor(0.0, 0.0, 0.0, 0.0) # clear the background color
        
        GL.glPointSize(10.0)            # point size
        GL.glEnable(GL.GL_PROGRAM_POINT_SIZE);
        GL.glEnable(GL.GL_POINT_SMOOTH); # make the points round
        GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA);
        GL.glEnable( GL.GL_BLEND )
        GL.glMatrixMode(GL.GL_PROJECTION)
        GL.glLoadIdentity()
        GLU.gluOrtho2D(self.minX, self.maxX, self.minY,self.maxY) # perspective
        self.start = time.time()
        self.nframes = 0

    def addToList(self,x,y,z): # add the values to the lists
        self.xList.append(x)
        self.yList.append(y)
        
    def zoom(self):
   
        if(self.zoomedOut): 
            self.zoomIn()
            self.zoomedOut = False
        else:
            self.zoomOut()
            self.zoomedOut = True
    
    def zoomOut(self):
        self.minY*= 1.5
        self.maxY*= 1.5
        self.minX*= 1.5
        self.maxX*= 1.5  
        GL.glLoadIdentity()
        GLU.gluOrtho2D(self.minX,self.maxX,self.minY,self.maxY) #change perspective
        GL.glPointSize(10.0) #change the point size

    def zoomIn(self):
        self.minY/= 1.5
        self.maxY/= 1.5
        self.minX/= 1.5
        self.maxX/= 1.5  
        GL.glLoadIdentity()
        GLU.gluOrtho2D(self.minX,self.maxX,self.minY,self.maxY) #change perspective
        GL.glPointSize(20.0) #change the point size
         
    def moveUp(self):
        self.maxY+= 500000
        self.minY+= 500000
        GL.glLoadIdentity()
        GLU.gluOrtho2D(self.minX,self.maxX,self.minY,self.maxY) #change perspective
        
    def moveDown(self):
        self.minY-= 500000
        self.maxY-= 500000
        GL.glLoadIdentity()
        GLU.gluOrtho2D(self.minX,self.maxX,self.minY,self.maxY) #change perspective

    def moveLeft(self):
        self.minX-= 500000
        self.maxX-= 500000
        GL.glLoadIdentity()
        GLU.gluOrtho2D(self.minX,self.maxX,self.minY,self.maxY) #change perspective

    def moveRight(self):
        self.maxX+= 500000
        self.minX+= 500000
        GL.glLoadIdentity()
        GLU.gluOrtho2D(self.minX,self.maxX,self.minY,self.maxY) #change perspective

    def redraw(self):
        GL.glClear(GL.GL_COLOR_BUFFER_BIT)
        GL.glBegin(GL.GL_POINTS)
        
        for i in range(len(self.xList)): # get the length of the list
            GL.glVertex2f(self.xList[i] ,self.yList[i]  )   #get the x and y coordinates
            
        GL.glEnd()
        GL.glFlush()
        self.nframes += 1
        tm = time.time() - self.start
        


class Treeview():
    def __init__(self,master):
        self.master=master
        self.mw=MainWindow(self.master)

        # create textBox to insert the data from the stars
        self.textBox = TextBox(self.master)
        self.textBox.createTextBoxAndScrollbar()     
        
    def setValuesToTextBox(self,name,XYZ):
        # insert the value in the text box
        self.textBox.tb.insert(tk.END, f"Name : {name}\n")
        self.textBox.tb.insert(tk.END, f"X coordinate : {XYZ[0]}\n")
        self.textBox.tb.insert(tk.END, f"y coordinate : {XYZ[1]}\n")
        self.textBox.tb.insert(tk.END, f"z coordinate : {XYZ[2]}\n")

    def getChecked(self):
            checkedList = self.tree.get_checked()   # get all the checked values from the children checkboxes
            openGLWindow = self.mw.getOpenGLWindow() # get the openGLWindow object

            # clear the list
            openGLWindow.xList.clear() 
            openGLWindow.yList.clear() 

            #clear the text box
            self.textBox.tb.delete('1.0', tk.END)

            h = Handler() 
            if checkedList.count("Sirrah") > 0: 
                
                name = h._getRow(5,0)
                RA = float(time2deg(h._getRow(0, 0)))  
                XYZ = sph2cart(29, RA, 1000000)
                openGLWindow.addToList(XYZ[0],XYZ[1],XYZ[2]) # add the xyz data to the lists
                self.setValuesToTextBox(name,XYZ)

            if checkedList.count("Mirach") > 0: 
                
                name = h._getRow(5,6)
                RA = float(time2deg(h._getRow(0, 6))) 
                XYZ = sph2cart(35, RA, 1000000)
                openGLWindow.addToList(XYZ[0],XYZ[1],XYZ[2])
                self.setValuesToTextBox(name,XYZ)

            if checkedList.count("Alamak") > 0: 
                
                name = h._getRow(5,11)
                RA = float(time2deg(h._getRow(0,11))) 
                XYZ = sph2cart(42, RA, 1000000)
                openGLWindow.addToList(XYZ[0],XYZ[1],XYZ[2]) 
                self.setValuesToTextBox(name,XYZ)

            if checkedList.count("Hamal") > 0: 
                
                name = h._getRow(5,12)
                RA = float(time2deg(h._getRow(0,12))) 
                XYZ = sph2cart(23, RA, 1000000)
                openGLWindow.addToList(XYZ[0],XYZ[1],XYZ[2])
                self.setValuesToTextBox(name,XYZ)

            if checkedList.count("Colure_star") > 0: 
                
                name = h._getRow(5,1)
                RA = float(time2deg(h._getRow(0,1))) 
                XYZ = sph2cart(59, RA, 1000000)
                openGLWindow.addToList(XYZ[0],XYZ[1],XYZ[2])
                self.setValuesToTextBox(name,XYZ)

            if checkedList.count("Schedir") > 0: 
                
                name = h._getRow(5,3)
                RA = float(time2deg(h._getRow(0,3))) 
                XYZ = sph2cart(56, RA, 1000000)
                openGLWindow.addToList(XYZ[0],XYZ[1],XYZ[2])
                self.setValuesToTextBox(name,XYZ)

            if(checkedList.count("Deneb_Kaitos") > 0):
                name = h._getRow(5,4)
                RA = float(time2deg(h._getRow(0,4))) 
                XYZ = sph2cart(-19, RA, 1000000)
                openGLWindow.addToList(XYZ[0],XYZ[1],XYZ[2])
                self.setValuesToTextBox(name,XYZ)

            if(checkedList.count("Mira") > 0):
                name = h._getRow(5,13)
                RA = float(time2deg(h._getRow(0,13))) 
                XYZ = sph2cart(-3, RA, 1000000)
   
                openGLWindow.addToList(XYZ[0],XYZ[1],XYZ[2])
                self.setValuesToTextBox(name,XYZ)
            
            if(checkedList.count("Polaris") > 0):
                name = h._getRow(5,7)
                RA = float(time2deg(h._getRow(0,7))) 
                XYZ = sph2cart(-89, RA, 1000000)
                openGLWindow.addToList(XYZ[0],XYZ[1],XYZ[2])
                self.setValuesToTextBox(name,XYZ)

            if(checkedList.count("Kochab") > 0):
                name = h._getRow(5,65)
                RA = float(time2deg(h._getRow(0,65))) 
                XYZ = sph2cart(75, RA, 1000000)
                openGLWindow.addToList(XYZ[0],XYZ[1],XYZ[2])
                self.setValuesToTextBox(name,XYZ)

    def _createTreeview(self):
        # create a checkbox treeview
        self.tree=CheckboxTreeview(self.master)
        self.tree.place(x=40,y=320,height=400);
        
        '''
        parameters: 
        - parent: identifier of the parent item
        - index: where in the list of parent’s children to insert the new item
        - iid: item identifier
        - text
        '''
        self.tree.insert("", "end", "And", text="Andromeda")
        self.tree.insert("And","end","Sirrah",text="Sirrah")
        self.tree.insert("And","end","Mirach",text="Mirach")
        self.tree.insert("And","end","Alamak",text="Alamak")
        self.tree.insert("","end","Ari",text="Aries")
        self.tree.insert("Ari","end","Hamal",text="Hamal")
        self.tree.insert("","end","Cas",text="Cassiopeia")
        self.tree.insert("Cas","end","Colure_star",text="Colure_star")
        self.tree.insert("Cas","end","Schedir",text="Schedir")
        self.tree.insert("","end","Cet",text="Cetus")
        self.tree.insert("Cet","end","Deneb_Kaitos",text="Deneb_Kaitos")
        self.tree.insert("Cet","end","Mira",text="Mira")
        self.tree.insert("","end","UMi",text="Ursae Minoris")
        self.tree.insert("UMi","end","Polaris",text="Polaris")
        self.tree.insert("UMi","end","Kochab",text="Kochab")
        

    def _createSimulateButton(self):     
        simulateButton= tk.Button(self.master,text="Simulate", width=7,relief = "groove",command= self.getChecked)
        simulateButton.place(x=640,y=560)

  


class Handler:
    # Initialize with data file
    def __init__(self):
        self._data = p.read_csv('data.dat')

    def _getCol(self, col):
        return self._data.iloc[:, col]

    def _getRow(self, col, row):
        return self._getCol(col)[row]


#global namespace
minuteEntry=None
calendar=None
hourEntry=None

class CalendarWindow():
   
    def _calendarSetting(self):
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
     
    def _timeSetting(self):
        global minuteEntry
        global hourEntry

        # create the Entries 
        hourEntry = tk.Entry( relief = "ridge", bd = 5, width = 4)
        hourEntry.place(x = 140, y = 250)
        hourEntry.insert(0, 0)
        minuteEntry = tk.Entry( relief = "ridge", bd = 5, width = 4)
        minuteEntry.place(x = 180, y = 250)
        minuteEntry.insert(0, 0)

    def getDateTime(self):
        # print the date and time
        print(self.getCalendarValue())
        print(self.getTime())
      

    def getTime(self):
        try:
            return self._filterTimeEntry() # check if entry is a valid time
        except ZeroDivisionError:
            #Handle the exception
            messagebox.showinfo("Error", "Time is not valid")
    
    def _addSpeed(self,speed):
        # add the value from the speed to the minuteEntry
        minuteValue=int(minuteEntry.get()) + speed
        self._update(minuteValue) 


    def _update(self,minuteValue): # function to update the hour,minute entries and the calendar
        
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

    def prevDate(self,year,month,day): #calculate previous date

        if(day==1): # its the first day of the month

            if(month==1): # its Januari. go back to December and decrement the year
                month=12
                year-=1
            else: # not the first month of the year
                month-=1

            # check how many days the month has
            if(month == 1 or month == 3 or month == 5 or month == 7 or month == 8 or month == 10 or month == 12):
                day=31

            if(month == 4 or month == 6 or month == 9 or month == 11):
                day=30

            # check the days of the leap month
            if(month==2):
                if(self.isLeap(year)):
                    day=29
                else:
                    day=28
        else:
            day-=1

        datetime_str = f'{year}/{str(month).zfill(2)}/{str(day).zfill(2)}'  # str().zfill(2) is to change from 1 digit to 2 digits
        return datetime_str  
       

    def nextDate(self,year,month,day): # alculate the next date
        
        # check how many days the month has
        if(month == 1 or month == 3 or month == 5 or month == 7 or month == 8 or month == 10 or month == 12):
            maxDays=31
        if(month == 4 or month == 6 or month == 9 or month == 11):
            maxDays=30

        #Februari has 28 or 29 days. it depends on the leap year
        if(month==2):
            if(self.isLeap(year)):
                maxDays=29
            else:
                maxDays=28  

        if(day==maxDays): # its the last day of the month
            day = 1

            if(month == 12): # last month of the year
                month = 1
                year = year + 1   
            else: # not last month of the year
                month = month + 1
        else: # its not the last day
            day = day + 1

        datetime_str = f'{year}/{str(month).zfill(2)}/{str(day).zfill(2)}'  # str().zfill(2) is to change from 1 digit to 2 digits
        return datetime_str   

    def isLeap(self,year):
        
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
                    return 1/0 # return error 
                else:       # time is valid
                    time = f'{str(hourEntry.get()).zfill(2)}:{str(minuteEntry.get()).zfill(2)}' # change 1 digit to 2 digits. 3 -> 03.  
                    return time
            else:        
                return 1/0 # return error 
        else:
             return 1/0 # return error 
              

class Button():
    def __init__(self, master,controller=None): # we use controller to get the value from the spinBox widget from the MainWindow class
        # Variables
        self.controller=controller 
        self.master=master
        #references
        self.calendar= CalendarWindow()     
        self.mw=MainWindow(self.master)

        # create Buttons and place it on the window
        moveToTopButton= tk.Button(self.master,text="↑",width=5,relief = "groove",command= self._moveToTop)
        moveToTopButton.place(x=1000,y=545)
        moveToBottomButton=tk.Button(self.master, text= "↓", width=5,relief = "groove",command= self._moveToBottom)
        moveToBottomButton.place(x=1000,y=575)
        moveToLeftButton=tk.Button(self.master, text= "←", width=5,relief = "groove",command= self._moveToLeft)
        moveToLeftButton.place(x=950,y=560)
        moveToRightButton=tk.Button(self.master, text= "→", width=5,relief = "groove",command= self._moveToRight)
        moveToRightButton.place(x=1050,y=560)
        zoomButton = tk.Button(self.master,text="🔍",width=5,relief = "groove",command = self._zoom)
        zoomButton.place( x= 880, y = 560)
        rewindButton=tk.Button(self.master, text= "<<", width= 5,relief = "groove", command = self._rewind)
        rewindButton.place(x=590,y=560)
        fastforwardButton=tk.Button(self.master,text=">>",width=5,relief = "groove",command=self._fastforward)
        fastforwardButton.place(x=705,y=560)
        getDateTimeButton=tk.Button(self.master,text="confirm",relief = "groove",width=10,command=self.calendar.getDateTime)
        getDateTimeButton.place(x=140,y=280)   

 
    def _fastforward(self):          
        if(self.getSpinboxValue() == "0.1"):
            fastForwardSpeed=1
        if(self.getSpinboxValue() == "0.2"):
            fastForwardSpeed=2
        if(self.getSpinboxValue() == "0.3"):
            fastForwardSpeed=3
        if(self.getSpinboxValue() == "0.4"):
            fastForwardSpeed=4  

        try:
            self.calendar._filterTimeEntry() #check if the current time is valid
        except ZeroDivisionError: 
            #Handle the exception
            messagebox.showinfo("Error", "Time is not valid")
        else:   #time is valid
            self.calendar._addSpeed(fastForwardSpeed)   
       

    def _rewind(self):
        if(self.getSpinboxValue() == "0.1"):
            rewindSpeed= -1
        if(self.getSpinboxValue() == "0.2"):
            rewindSpeed= -2
        if(self.getSpinboxValue() == "0.3"):
            rewindSpeed= -3
        if(self.getSpinboxValue() == "0.4"):
            rewindSpeed= -4  
        
        try:
            self.calendar._filterTimeEntry() #check if the current Time is valid
        except ZeroDivisionError:
            #Handle the exception
            messagebox.showinfo("Error", "Time is not valid")
        else:   #time is valid
            self.calendar._addSpeed(rewindSpeed)

    def _zoom(self):
        openGLWindow = self.mw.getOpenGLWindow() # get the openGLFrame object
        openGLWindow.zoom()

    def _moveToTop(self):
        openGlWindow = self.mw.getOpenGLWindow() # get the openGLFrame object
        openGlWindow.moveUp()

    def _moveToBottom(self):
        openGLWindow = self.mw.getOpenGLWindow()
        openGLWindow.moveDown()

    def _moveToLeft(self):
        openGLWindow = self.mw.getOpenGLWindow()
        openGLWindow.moveLeft()

    def _moveToRight(self):
        openGLWindow = self.mw.getOpenGLWindow()
        openGLWindow.moveRight()

    def getSpinboxValue(self):
        self.value=self.controller.get() # get the spinBox value
        return self.value
        


window = tk.Tk()
window.geometry("1500x750")
window.title("GUI")
window.resizable(False,False) #disable resizable
icon = tk.PhotoImage(file = "IconImage.png")
window.iconphoto(False, icon) # change the icon from the gui
application = MainWindow(window)
application.createObject()
window.mainloop()

