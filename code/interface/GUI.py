import tkinter as tk
from tkcalendar import Calendar
from tkinter import ttk
import datetime,time


class MainWindow(tk.Frame):

    def __init__(self, master): 
        self.master = master

        # Button widgets
        #self.quitButton= Button(self.master)
        self.confirmButton= Button(self.master)

        # Calendar widget
        self.calendarButton = Button(self.master)

        # spinBox widget
        self.spinBox= tk.Spinbox(self.master ,from_=1, to=4)    #spinBox value only from 1 to 4
        self.spinBox.place(x=300,y=500)
        self.spinBox= Button(self.master,self.spinBox)

        # checkbox widget
        self.checkBox1 = Checkbox(self.master)
        self.checkBox2 = Checkbox(self.master)
        self.checkBox3 = Checkbox(self.master)

        # Label widget
        self.label = tk.Label(self.master,text="Speed")
        self.label.place(x=300,y=480)
       
class Checkbox():
    def __init__(self,master):
            # checkBox hold a Boolean
            self.checkValue1 = tk.BooleanVar()
            self.checkValue2 = tk.BooleanVar()
            self.checkValue3 = tk.BooleanVar()
            # initialise the checkboxes
            self.checkBox1 = tk.Checkbutton(master,text = "HighLight 1",var=self.checkValue1,command= self.checkValue)
            self.checkBox2 = tk.Checkbutton(master,text = "HighLight 2",var=self.checkValue2,command= self.checkValue)
            self.checkBox3 = tk.Checkbutton(master,text = "HighLight 3",var=self.checkValue3,command= self.checkValue)
            # place the checkboxes on the MainWindow
            self.checkBox1.place(x=100,y=100)
            self.checkBox2.place(x=100,y=120)
            self.checkBox3.place(x=100,y=140)
            
    def checkValue(self): # check the checkBox value
        if(self.checkValue1.get()==True):
            print("1 is true")
        if(self.checkValue2.get()==True):
            print("2 is true")
        if(self.checkValue3.get()==True):
            print("3 is true")
           
class Button():
    def __init__(self, master,controller=None): # we use controller to get the value from the spinBox widget from the MainWindow class
            self.spinBox=controller 
            #self.quitButton=tk.Button(master, text = 'X', width = 4 ,bg="red", command= quit) # quit the program if button is pressed
            #self.quitButton.place(x=1500,y=0)
            self.confirmButton=tk.Button(master, text = 'Confirm', width = 8,command=self.getSpinboxValue)#call the sendAcceleration function if button is pressed.
            self.confirmButton.place(x=340,y=520)
            self.calendarButton=tk.Button(master,text = "Calendar", width = 10,command=self.openCalendar)
            self.calendarButton.place(x=600,y=600)
    
    def getSpinboxValue(self):
        value=self.spinBox.get() # get the spinBox value
        print(value)

    def confirmCalendarButton(self):
            date = self.calendar.selection_get().strftime("%d-%m-%Y") #change datetime to string
            print (date)
            if(date=="01-01-2020"):
                print("Nice its a string")
            
            
    def openCalendar(self):       
        top = tk.Toplevel()

        # min and max date
        mindate = datetime.date(year=2000, month=1, day=21)
        maxdate = datetime.date(year=3000, month=12, day=30)
        
        # calendar settings
        self.calendar = Calendar(top, font="Arial 14", selectmode='day', locale='en_US',
                    mindate=mindate, maxdate=maxdate, 
                    cursor="hand2", year=2020, month=1, day=1)
        self.calendar.pack(fill="both", expand=True)

        button=tk.Button(top,text="ok", command=self.confirmCalendarButton).pack()
        
        
        
def main(): 
    # settings for the MainWindow
    window = tk.Tk()
    window.geometry("1400x750")
    window.title("GUI")
    window.configure(background="blue") 
    window.resizable(False,False) #disable resizable
    #window.attributes("-fullscreen", True)
    application = MainWindow(window)
    window.mainloop()

if __name__ == '__main__':
        main()

# class Demo2:
#     def __init__(self, master):
#         self.master = master
#         self.frame = tk.Frame(self.master)
#         self.quitButton = tk.Button(self.frame, text = 'Quit', width = 25, command = self.close_windowss)
#         self.quitButton.pack()
#         self.frame.pack()
#     def close_windows(self):
#         self.master.destroy()