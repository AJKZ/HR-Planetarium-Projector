import tkinter as tk
from tkcalendar import Calendar #
from tkinter import ttk,messagebox
import datetime,time 
from ttkwidgets import CheckboxTreeview #
import numpy as n #
import pandas as p #
from pyopengltk import OpenGLFrame #
from OpenGL import GL, GLU #
import math

def sexagesimalToDecimalDegrees(degrees, minutes, seconds):
    decimalDegrees = degrees + (minutes / 60) + (seconds / 3600)
    return decimalDegrees
def cartesianCoordinates(RA,declination, distance): # calculate the cartesianCoordinates
    x = round((distance * math.cos(declination) * math.cos(RA)), 3)
    y = round((distance * math.cos(declination) * math.sin(RA)), 3)
    z = round((distance * math.sin(declination)), 3)
    return (x, y, z)

def calculateRA(rhours,rminutes,rseconds):
    return math.radians(sexagesimalToDecimalDegrees((rhours * 15), (rminutes * 15), (rseconds * 15)))
    
def calculateDec(ddegrees,dminutes,dseconds):
    return math.radians(sexagesimalToDecimalDegrees(ddegrees, dminutes, dseconds))


oGLWindow = None
class MainWindow(tk.Frame):
   
    def __init__(self, master): 
        # Variable
        self.master = master

    def createObject(self):
        # organize the window
        windowLayout= tk.Label(self.master,borderwidth=1,relief='solid',width=110,height=6)
        windowLayout.place(x=380,y=540)
        
        # CalendarWindow object
        openCalendar = CalendarWindow()
        openCalendar.calendarSetting()
        openCalendar.timeSetting()

        # Label widget
        label = tk.Label(self.master,text="Speed")
        label.place(x=390,y=543)
        
        f = tk.Frame(self.master) # create a frame 
        f.place(x=380,y=15)
        global oGLWindow
        oGLWindow = OpenGLWindow(f,width=775, height=523)  # put the OpenGLWindow in the frame from tkinter
        oGLWindow.animate=1 #without this, simulation doesnt work
        oGLWindow.pack() # pack it

        # treeview object
        tree = Treeview(self.master)
        tree.createTreeview()
        tree.getChecked()

        # Button objects
        button = Button(self.master)
        button.createButtons()
        
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
    colorList = []
    dotSizeList = []
    laserPositionList = []

    # opengl perspective range
    infinit = 1000000000
    minX=-infinit
    maxX= infinit
    minY=-infinit
    maxY= infinit
    zoomValue=0

    def initgl(self):

        GL.glViewport(0, 0, self.width, self.height)    
        GL.glClearColor(0.0, 0.0, 0.0, 0.0) # clear the background color
        
        #enable it
        GL.glEnable(GL.GL_PROGRAM_POINT_SIZE);
        GL.glEnable(GL.GL_POINT_SMOOTH);
        GL.glEnable( GL.GL_BLEND )
        GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA); 
        GL.glMatrixMode(GL.GL_PROJECTION) # specify which matrix is the current matrix
        GL.glLoadIdentity() # reset matrix
        GLU.gluOrtho2D(self.minX, self.maxX, self.minY,self.maxY) # perspective
        # bind the mouse movements
        self.bind("<Button-1>",self.mousePress)
        self.bind('<ButtonRelease-1>', self.mouseRelease)
        self.bind('<Double-Button-1>',self.doublePressLeftMouseButton)
        self.bind('<Double-Button-3>',self.doublePressRightMouseButton)
        self.start = time.time()
        self.nframes = 0

    def doublePressLeftMouseButton(self,event): # press 2 times to zoom in and out
        self.zoomIn()

    def doublePressRightMouseButton(self,event):
        self.zoomOut()

    def mousePress(self,event):
        self.mousePressX = event.x
        self.mousePressY = event.y
        
    def mouseRelease(self,event):
        self.mouseReleaseX = event.x
        self.mouseReleaseY = event.y
        self.dragMovement()

    def dragMovement(self):
        deltaX = self.mouseReleaseX-self.mousePressX
        deltaY = self.mouseReleaseY-self.mousePressY
        # pos deltaX = mouse drag from left to right
        # neg deltaX = mouse drag from right to left
        # pos deltaY = mouse drag from down to up
        # neg deltaY = mouse drag from up to down

        if(deltaX > 0 and deltaX > deltaY):
            self.moveLeft()
        elif(deltaY > 0):
            self.moveUp()
        if(deltaX < 0 and deltaX < deltaY):
            self.moveRight()
        elif(deltaY < 0):
            self.moveDown()

    def addToList(self,x,y,z,color,magnitude): 
        # add the values to the lists
        self.xList.append(x)
        self.yList.append(y)
        self.colorList.append(color)

        # point size varies from magnitude 
        # bigger magnitude = smaller pointsize
        if(magnitude >= 0 and magnitude <0.5):
            pointsize = 10
        elif(magnitude >= 0.5 and magnitude <1):
            pointsize = 9
        elif(magnitude >=1 and magnitude < 1.5):
            pointsize = 8
        elif(magnitude >=1.5 and magnitude <2):
            pointsize =7
        elif(magnitude >=2 and magnitude < 2.5):
            pointsize = 6
        elif(magnitude >=2.5 and magnitude < 3):
            pointsize = 5
        elif(magnitude >=3 and magnitude < 3.5):
            pointsize = 4
        elif(magnitude >=3.5):
            pointsize = 3
        self.dotSizeList.append(pointsize) # add it to the list

    def zoomOut(self):
        if(self.zoomValue <= -15): # only 3 times zoom out
            self.zoomValue = -15
        else:  
            self.minY*= 1.5
            self.maxY*= 1.5
            self.minX*= 1.5
            self.maxX*= 1.5  
            GL.glLoadIdentity()
            GLU.gluOrtho2D(self.minX,self.maxX,self.minY,self.maxY) #change perspective
            self.zoomValue-=5
        
    def zoomIn(self):
        if(self.zoomValue >=15): # only 3 times zoom in
            self.zoomValue = 15
        else:
            self.minY/= 1.5
            self.maxY/= 1.5
            self.minX/= 1.5
            self.maxX/= 1.5  
            GL.glLoadIdentity()
            GLU.gluOrtho2D(self.minX,self.maxX,self.minY,self.maxY) #change perspective
            self.zoomValue+=5
      
    def moveUp(self):
        self.maxY+= self.infinit/4
        self.minY+= self.infinit/4
        GL.glLoadIdentity()
        GLU.gluOrtho2D(self.minX,self.maxX,self.minY,self.maxY) #change perspective
        
    def moveDown(self):
        self.minY-= self.infinit/4
        self.maxY-= self.infinit/4
        GL.glLoadIdentity()
        GLU.gluOrtho2D(self.minX,self.maxX,self.minY,self.maxY) #change perspective

    def moveLeft(self):
        self.minX-= self.infinit/4
        self.maxX-= self.infinit/4
        GL.glLoadIdentity()
        GLU.gluOrtho2D(self.minX,self.maxX,self.minY,self.maxY) #change perspective

    def moveRight(self):
        self.maxX+= self.infinit/4
        self.minX+= self.infinit/4
        GL.glLoadIdentity()
        GLU.gluOrtho2D(self.minX,self.maxX,self.minY,self.maxY) #change perspective

    def redraw(self):
        GL.glClear(GL.GL_COLOR_BUFFER_BIT)
        
        for i in range(len(self.xList)): # get the length of the list
            size = self.dotSizeList[i]
            
            # change the point size which depends on the zoomValue
            if(self.zoomValue > 0):
                size = size + self.zoomValue
                GL.glPointSize(size) #change the point size
            else:
                size = size + self.zoomValue
                if(size <= 1):
                    size = 1
                GL.glPointSize(size)
            GL.glBegin(GL.GL_POINTS)
            GL.glColor4f(self.colorList[i][0],self.colorList[i][1],self.colorList[i][2],self.colorList[i][3]) # get the colors
            GL.glVertex2f(self.xList[i] ,self.yList[i]  )   # get the x and y coordinates
            
            GL.glEnd()

        GL.glFlush()
        self.nframes += 1
        tm = time.time() - self.start
        

starList = []

class Treeview():
    def __init__(self,master):
        self.master=master
        self.mw=MainWindow(self.master)
        self.openGLWindow = self.mw.getOpenGLWindow()
        
        # create textBox to insert the data from the stars
        self.textBox = TextBox(self.master)
        self.textBox.createTextBoxAndScrollbar()     
        
    def setValuesToTextBox(self,name,XYZ):
        # insert the value in the text box
        self.textBox.tb.insert(tk.END, f"Name : {name}\n")
        self.textBox.tb.insert(tk.END, f"X : {XYZ[0]}\n")
        self.textBox.tb.insert(tk.END, f"y : {XYZ[1]}\n")
        self.textBox.tb.insert(tk.END, f"z : {XYZ[2]}\n")

    def setStarData(self,row):
        # get the data 
        h = Handler() 
        self.name = h._getRow(3,row)
        RAHour = h._getRow(4, row)
        RAMinutes = h._getRow(5, row)
        RASec = h._getRow(6, row)
        decDegree = h._getRow(7, row)
        decMin = h._getRow(8, row)
        decSec = h._getRow(9, row)
        self.RA = calculateRA(RAHour,RAMinutes,RASec)
        self.dec = calculateDec(decDegree,decMin,decSec)
        self.XYZ = cartesianCoordinates(self.RA,self.dec,1000000000)
        self.magnitude = h._getRow(0, row)

    def getXYZ(self):
        return self.XYZ

    def getName(self):
        return self.name

    def getMagnitude(self):
        return self.magnitude

    def findNameOfStar(self,name):
        checkedList = self.tree.get_checked()   # get all the checked values from the children checkboxes
        whiteColor = [1,1,1,1]
        grayColor = [1,1,1,0.2]

        h = Handler()
        length = len(h._getCol(0)) 
        for i in range(length):
            
            if(h._getRow(3,i) == name):  # loops through all the data from the column and find the name
                if(checkedList.count(name) > 0): # if name of the star is checked in the checkbox, highlight the star.
                    self.setStarData(i) # give the row number to read the data from the data set
                    self.openGLWindow.addToList(self.getXYZ()[0],self.getXYZ()[1],self.getXYZ()[2],whiteColor,self.getMagnitude()) # add the xyz and color data to the lists
                    self.setValuesToTextBox(self.getName(),self.getXYZ()) #add the values to the textBox
                    self.openGLWindow.laserPositionList.append([self.getXYZ()[0],self.getXYZ()[1]]) # add the XY position in the list for the projector
                else:  # name of the star is not checked in the checkbox change the color to gray 
                    self.setStarData(i)
                    self.openGLWindow.addToList(self.getXYZ()[0],self.getXYZ()[1],self.getXYZ()[2],grayColor,self.getMagnitude()) 

    def getChecked(self):
            # clear the list
            self.openGLWindow.xList.clear() 
            self.openGLWindow.yList.clear() 
            self.openGLWindow.colorList.clear()
            self.openGLWindow.dotSizeList.clear()
            self.openGLWindow.laserPositionList.clear()
 
            #clear the text box
            self.textBox.tb.delete('1.0', tk.END)
            
            for i in range(len(starList)): # loop through all the stars in the list
                self.findNameOfStar(starList[i]) # find the name
            
            #print (self.openGLWindow.laserPositionList)
                
    def createTreeview(self):
        # create a checkbox treeview
        self.tree=CheckboxTreeview(self.master)
        self.tree.place(x=0,y=320,height=400)
        scrollbar = tk.Scrollbar(self.master) # create a scrollbar
        scrollbar.place(x=200,y=330,relheight=0.5)
        scrollbar.config(command=self.tree.yview)    
        self.tree.config(yscrollcommand=scrollbar.set) # attach the scrollbar to the textbox
        self.tree.bind("<ButtonRelease-1>", self.callBack) # bind an mouse event to the checkbox.

        h = Handler()
        length = len(h._getCol(1))  # get the length to loop through the whole data file
        constellations = []

        for i in range(length):
            cname = h._getRow(1, i) # get all the cname
            
            similarityfound = False
            for i in range(len(constellations)): # loop though the constellations list
                if cname == constellations[i]:  # the cname is already in the list
                    similarityfound = True
            if not similarityfound: # the cname is not in the list
                constellations.append(cname) # add the cname to the list
                self.tree.insert("", "end", cname, text=cname) # add the cname in the treeview
                
        for i in range(length): # get all the cname and sname and insert it in the treeview
            sname = h._getRow(3, i)
            cname = h._getRow(1, i)
            self.tree.insert(cname, "end", sname, text=sname)
            starList.append(sname) # add sname in starList
        
    def callBack(self, event): # checkbox event handler
        item = self.tree.identify('item',event.x,event.y)
        self.getChecked()
        
class Handler:
    # Initialize with data file
    def __init__(self):
        self._data = p.read_csv('stars.dat')

    def _getCol(self, col):
        return self._data.iloc[:, col]

    def _getRow(self, col, row):
        return self._getCol(col)[row]


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
        date = calendar.selection_get().strftime("%d-%m-%Y") #change datetime to string and get the date
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

    def getDateTime(self):
        # print the date and time
        print(self.getCalendarValue())
        print(self.getTime())
      
    def getTime(self):
        try:
            return self.filterTimeEntry() # check if entry is a valid time
        except ZeroDivisionError:
            #Handle the exception
            messagebox.showinfo("Error", "Time is not valid")
    
    def addSpeed(self,speed):
        # add the value from the speed to the minuteEntry
        minuteValue=int(minuteEntry.get()) + speed
        self.update(minuteValue) 

    def update(self,minuteValue): # function to update the hour,minute entries and the calendar
        
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

        
        if(int(hourEntry.get())<0 ):   # hour is under 0

            # get the day,month and year from the calendar widget
            day=calendar.selection_get().day
            month=calendar.selection_get().month
            year=calendar.selection_get().year
            
            # get the previous date
            date = self.prevDate(year,month,day)
            
            # change String to datetime and update the calendar
            datetimeObject = datetime.datetime.strptime(date, '%Y/%m/%d') 
            calendar.selection_set(datetimeObject)

            #reset the hours
            hourEntry.delete(0,'end')
            hourEntry.insert(0,23)
        
        if(int(hourEntry.get())>=24 ):   #if hour is above 24

            # get the day,month and year from the calendar widget
            day=calendar.selection_get().day
            month=calendar.selection_get().month
            year=calendar.selection_get().year
            
            # get the next date
            date = self.nextDate(year,month,day)
         
            # change String to datetime and update the calendar
            datetimeObject = datetime.datetime.strptime(date, '%Y/%m/%d') 
            calendar.selection_set(datetimeObject)

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

    def filterTimeEntry(self): 
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
    def __init__(self, master): # we use controller to get the value from the spinBox widget from the MainWindow class
        self.master=master

        #references
        self.calendar= CalendarWindow()     
        self.mw=MainWindow(self.master)
        self.openGLWindow = self.mw.getOpenGLWindow() # get the openGLFrame object

    def createButtons(self):
        # create Buttons and place it on the window
        moveToTopButton= tk.Button(self.master,text="↑",width=5,relief = "groove",command= self.moveToTop)
        moveToTopButton.place(x=1000,y=545)
        moveToBottomButton=tk.Button(self.master, text= "↓", width=5,relief = "groove",command= self.moveToBottom)
        moveToBottomButton.place(x=1000,y=575)
        moveToLeftButton=tk.Button(self.master, text= "←", width=5,relief = "groove",command= self.moveToLeft)
        moveToLeftButton.place(x=950,y=560)
        moveToRightButton=tk.Button(self.master, text= "→", width=5,relief = "groove",command= self.moveToRight)
        moveToRightButton.place(x=1050,y=560)
        zoomInButton = tk.Button(self.master,text="➕",width=5,relief = "groove",command = self.zoomIn)
        zoomInButton.place( x= 880, y = 560)
        zoomOutButton = tk.Button(self.master,text="➖",width=5,relief = "groove",command = self.zoomOut)
        zoomOutButton.place( x= 830, y = 560)
        rewindButton=tk.Button(self.master, text= "<<", width= 5,relief = "groove", command = self.rewind)
        rewindButton.place(x=590,y=560)
        fastforwardButton=tk.Button(self.master,text=">>",width=5,relief = "groove",command=self.fastforward)
        fastforwardButton.place(x=705,y=560)
        getDateTimeButton=tk.Button(self.master,text="confirm",relief = "groove",width=10,command=self.calendar.getDateTime)
        getDateTimeButton.place(x=140,y=280)   

        # spinBox widget
        self.spinBox= tk.Spinbox(self.master,from_=0.1, to=0.4,state="readonly" ,increment=0.1)    #spinBox value only from 0.1 to 0.4
        self.spinBox.place(x=390,y=562)

    def fastforward(self):       
        for i in range(1,5): # from 1 to 4
            if(self.getSpinboxValue() == (f'0.{i}')): # from 0.1 to 0.4
                fastForwardSpeed = i # from 1 to 4

        self.sentSpeed(fastForwardSpeed)
       
    def rewind(self):
        for i in range(1,5): # from 1 to 4
            if(self.getSpinboxValue() == (f'0.{i}')): # from 0.1 to 0.4
                rewindSpeed= (int) (f'-{i}') # from -1 to -4

        self.sentSpeed(rewindSpeed)
     
    def sentSpeed(self,speed):
        try:
            self.calendar.filterTimeEntry() #check if the current Time is valid
        except ZeroDivisionError:
            #Handle the exception
            messagebox.showinfo("Error", "Time is not valid")
        else:   #time is valid
            self.calendar.addSpeed(speed)

    def zoomIn(self):
        self.openGLWindow.zoomIn()

    def zoomOut(self):
        self.openGLWindow.zoomOut()

    def moveToTop(self):
        self.openGLWindow.moveUp()

    def moveToBottom(self):
        self.openGLWindow.moveDown()

    def moveToLeft(self):
        self.openGLWindow.moveLeft()

    def moveToRight(self):
        self.openGLWindow.moveRight()

    def getSpinboxValue(self):
        self.value=self.spinBox.get() # get the spinBox value
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
