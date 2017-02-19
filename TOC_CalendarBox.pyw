import tkinter
import TOC_Calendar
import TOC_DialogBox
import datetime

class CalendarDialog(TOC_DialogBox.Dialog):
    def body(self, master):
        self.calendar = TOC_Calendar.Calendar(master)
        self.calendar.pack()

    def apply(self):
        self.result = self.calendar.selection


class CalendarFrame(tkinter.LabelFrame):
    def __init__(self, master):
        global pick_date
        tkinter.LabelFrame.__init__(self, master)

        def getdate():
            try:
                cd = CalendarDialog(self)
                result = cd.result
                self.selected_date.set(result.strftime("%Y-%m-%d"))
            except: 
                pass
          
        self.pack(pady=(30,0))
        self.config(relief=tkinter.FLAT)
        self.selected_date = tkinter.StringVar()
        tkinter.Label(self, text="DATE OF FAULT ", font="TkFixedFont").pack(side=tkinter.LEFT, padx=(0,62))
        self.selected_date.set(datetime.date.today())
        tkinter.Entry(self, textvariable=self.selected_date, width=10).pack(side=tkinter.LEFT)
        tkinter.Button(self, text="∇", command=getdate).pack(side=tkinter.LEFT, padx=(0,560))
        pick_date = self.selected_date


class StartFrame(tkinter.LabelFrame):
    def __init__(self, master):
        global start_date
        tkinter.LabelFrame.__init__(self, master)

        def getdate():
            try:
                cd = CalendarDialog(self)
                result = cd.result
                self.selected_date.set(result.strftime("%Y-%m-%d"))
            except: 
                pass
          
        self.pack(pady=(30,0))
        self.config(relief=tkinter.FLAT)
        self.selected_date = tkinter.StringVar()
        tkinter.Label(self, text="START DATE ", font="TkFixedFont").pack(side=tkinter.LEFT)
        tkinter.Entry(self, textvariable=self.selected_date, width=10).pack(side=tkinter.LEFT)
        tkinter.Button(self, text="∇", command=getdate).pack(side=tkinter.LEFT)
        start_date = self.selected_date


class EndFrame(tkinter.LabelFrame):
    def __init__(self, master):
        global end_date
        tkinter.LabelFrame.__init__(self, master)

        def getdate():
            try:
                cd = CalendarDialog(self)
                result = cd.result
                self.selected_date.set(result.strftime("%Y-%m-%d"))
            except: 
                pass
          
        self.config(relief=tkinter.FLAT)
        self.selected_date = tkinter.StringVar()
        tkinter.Label(self, text="END DATE   ", font="TkFixedFont").pack(side=tkinter.LEFT)
        tkinter.Entry(self, textvariable=self.selected_date, width=10).pack(side=tkinter.LEFT)
        tkinter.Button(self, text="∇", command=getdate).pack(side=tkinter.LEFT)
        end_date = self.selected_date

        
def ReturnDate():
    return pick_date

def StartDate():
    return start_date

def EndDate():
    return end_date


