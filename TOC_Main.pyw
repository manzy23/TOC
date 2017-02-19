from tkinter import *
from tkinter import ttk
import time
import datetime
import sqlite3
from operator import itemgetter
import TOC_CalendarBox
import TOC_Report
import TOC_Start
import tkinter.messagebox as tm


openList = []

db = sqlite3.connect('TOC.db')
c = db.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS records
            (TICKET_NO             INTEGER,
             DATE_OF_FAULT         TEXT,
             TIME_OF_FAULT         TEXT,
             FAULT_INFORMED_BY     TEXT,
             SITE_ID               TEXT,
             CATEGORY_1            TEXT,
             CATEGORY_2            TEXT,
             CATEGORY_3            TEXT,
             FAULT_DESCRIPTION     TEXT, 
             TWO_G                 INTEGER,
             THREE_G               INTEGER,
             LTE                   INTEGER,
             WIFI                  INTEGER,
             FAULT_INFORMED_TO     TEXT,
             FAULT_RESPONSIBILITY  TEXT,
             FAULT_DETAILS         TEXT,
             FAULT_CAUSE           TEXT,
             TICKET_STATUS         TEXT)''')
db.commit()


# Retrieving already present open tickets from database
c.execute("SELECT * FROM records WHERE TICKET_STATUS LIKE 'Opened:%' OR TICKET_STATUS LIKE 'Updated:%'")
while True:
    row = c.fetchone()
    if (row == None):
        break
    else:
        openList.append(row)

        
# Function to identify selected record from list
def whichSelected():
    try:
        selected = (tree.selection()[0]).split('I')
        return (int(selected[1],16)-1)
    except:
        pass


# Function for adding a new entry    
def addEntry():
    try:
        openList.append ([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
        c.execute('''INSERT INTO records(TICKET_NO, DATE_OF_FAULT, TIME_OF_FAULT, FAULT_INFORMED_BY, SITE_ID, CATEGORY_1, CATEGORY_2, CATEGORY_3, FAULT_DESCRIPTION, TWO_G,
                     THREE_G, LTE, WIFI, FAULT_INFORMED_TO, FAULT_RESPONSIBILITY, FAULT_DETAILS, FAULT_CAUSE, TICKET_STATUS) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',(openList[-1]))
        db.commit()
        ticketNo = c.lastrowid
        del openList[-1]
        c.execute("DELETE FROM records WHERE TICKET_NO=0")
        openList.append ([ticketNo, dateOfFault.get(), time_stamp(), faultInformedBy.get(), siteID.get(), category1.get(), category2.get(), category3.get(), faultDescription.get(), twoG.get(), threeG.get(), lte.get(), wifi.get(), user, faultResponsibility.get(), faultDetails.get(), faultCause.get(), "Opened: " + time_stamp()])
        c.execute('''INSERT INTO records(TICKET_NO, DATE_OF_FAULT, TIME_OF_FAULT, FAULT_INFORMED_BY, SITE_ID, CATEGORY_1, CATEGORY_2, CATEGORY_3, FAULT_DESCRIPTION, TWO_G,
                     THREE_G, LTE, WIFI, FAULT_INFORMED_TO, FAULT_RESPONSIBILITY, FAULT_DETAILS, FAULT_CAUSE, TICKET_STATUS) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',(openList[-1]))
        db.commit()
        win_refresh("main")
        
    except ValueError:
        tm.showerror("ERROR", "Please Enter A Number For Sites Affected")


def win_refresh(reftype):
    date_of_fault_f.forget()
    frame1.forget()
    frame2.forget()
    frame3.forget()
    frame4.forget()
    frame5.forget()
    frame6.forget()
    frame7.forget()
    if (str(reftype)=="main"):
        mainWindow("main")
    else:
        mainWindow("full")


# Function for deleting(closing) a ticket
def deleteEntry():
    try:
        del openList[whichSelected()]
    except:
        pass


# Function for displaying information about an open ticket
def showEntry(event):
    try:
        if (whichSelected() >= 0):
            selectedRecord = whichSelected()
            selectedID = tree.selection()
            win_refresh("full")
            b1.config(state=DISABLED)
        
            ticket_no, date_of_fault, time_of_fault, fault_informed_by, site_id, cat_1, cat_2, cat_3, fault_description, two_g, three_g, l_t_e, wi_fi, system_user, fault_responsibility, fault_details, fault_cause, ticket_status = openList[selectedRecord]
            dateOfFault.set(date_of_fault)
            timeOfFault.set(time_of_fault)
            faultInformedBy.set(fault_informed_by)
            siteID.set(site_id)
            category1.set(cat_1)
            category2.set(cat_2)
            category3.set(cat_3)
            faultDescription.set(fault_description)
            twoG.set(two_g)
            threeG.set(three_g)
            lte.set(l_t_e)
            wifi.set(wi_fi)
            faultResponsibility.set(fault_responsibility)
            faultDetails.set(fault_details)
            faultCause.set(fault_cause)
            
            tree.selection_set(selectedID)
            
            if (str(passer) == "user"):
                for widget in frame1.winfo_children():
                    widget.configure(state="disabled")
                for widget in frame2.winfo_children():
                    widget.configure(state="disabled")
                for widget in frame3.winfo_children():
                    widget.configure(state="disabled")
                for widget in date_of_fault_f.winfo_children():
                    widget.configure(state="disabled")
            else:
                time_of_fault_f.configure(state='normal')

    except:
        pass


# Function for updating and closing existing record    
def updateEntry():
    try:
        if (status.get() == 1):
            openList[whichSelected()] = [openList[whichSelected()][0], dateOfFault.get(), timeOfFault.get(), faultInformedBy.get(), siteID.get(), category1.get(), category2.get(), category3.get(), faultDescription.get(), twoG.get(), threeG.get(), lte.get(), wifi.get(), openList[whichSelected()][13], faultResponsibility.get(), faultDetails.get(), faultCause.get(), "Closed: " +time_stamp()]
            c.execute('''UPDATE records
                         SET TICKET_NO=?, DATE_OF_FAULT=?, TIME_OF_FAULT=?, FAULT_INFORMED_BY=?, SITE_ID=?, CATEGORY_1=?, CATEGORY_2=?, CATEGORY_3=?, FAULT_DESCRIPTION=?, TWO_G=?, THREE_G=?, LTE=?, WIFI=?, FAULT_INFORMED_TO=?, FAULT_RESPONSIBILITY=?, FAULT_DETAILS=?, FAULT_CAUSE=?, TICKET_STATUS=?
                         WHERE TICKET_NO=?;''', (openList[whichSelected()][0], openList[whichSelected()][1], openList[whichSelected()][2], openList[whichSelected()][3],
                                                 openList[whichSelected()][4], openList[whichSelected()][5], openList[whichSelected()][6], openList[whichSelected()][7],
                                                 openList[whichSelected()][8], openList[whichSelected()][9], openList[whichSelected()][10], openList[whichSelected()][11],
                                                 openList[whichSelected()][12], openList[whichSelected()][13], openList[whichSelected()][14], openList[whichSelected()][15],
                                                 openList[whichSelected()][16], openList[whichSelected()][17], openList[whichSelected()][0]))
            deleteEntry()
        else:
            openList[whichSelected()] = [openList[whichSelected()][0], dateOfFault.get(), timeOfFault.get(), faultInformedBy.get(), siteID.get(), category1.get(), category2.get(), category3.get(), faultDescription.get(), twoG.get(), threeG.get(), lte.get(), wifi.get(), openList[whichSelected()][13], faultResponsibility.get(), faultDetails.get(), faultCause.get(), "Updated: " +time_stamp()]
            c.execute('''UPDATE records
                         SET TICKET_NO=?, DATE_OF_FAULT=?, TIME_OF_FAULT=?, FAULT_INFORMED_BY=?, SITE_ID=?, CATEGORY_1=?, CATEGORY_2=?, CATEGORY_3=?, FAULT_DESCRIPTION=?, TWO_G=?, THREE_G=?, LTE=?, WIFI=?, FAULT_INFORMED_TO=?, FAULT_RESPONSIBILITY=?, FAULT_DETAILS=?, FAULT_CAUSE=?, TICKET_STATUS=?
                         WHERE TICKET_NO=?;''', (openList[whichSelected()][0], openList[whichSelected()][1], openList[whichSelected()][2], openList[whichSelected()][3],
                                                 openList[whichSelected()][4], openList[whichSelected()][5], openList[whichSelected()][6], openList[whichSelected()][7],
                                                 openList[whichSelected()][8], openList[whichSelected()][9], openList[whichSelected()][10], openList[whichSelected()][11],
                                                 openList[whichSelected()][12], openList[whichSelected()][13], openList[whichSelected()][14], openList[whichSelected()][15],
                                                 openList[whichSelected()][16], openList[whichSelected()][17], openList[whichSelected()][0]))
        db.commit()
        win_refresh("main")
        b1.config(state=NORMAL)
        center_window(main_win)

    except ValueError:
        tm.showerror("ERROR", "Please Enter A Number For Sites Affected")
    except IndexError:
        tm.showerror("ERROR", "Please Select An Item From The List")


def showReports():
    main_win.destroy()
    TOC_Report.setup(user,passer)


def logout():
    main_win.destroy()
    TOC_Start.setup()
    
    
# Function for returning to main window
def returnMain():
    win_refresh("main")
    b1.config(state=NORMAL)
    center_window(main_win)


# Main window design     
def mainWindow(wintype):
    global dateOfFault, timeOfFault, faultInformedBy, siteID, faultDescription, twoG, threeG, lte, wifi, faultResponsibility, faultDetails, faultCause, status, category1, category2, category3  
    global date_of_fault_f, time_of_fault_f, tree, ticketStatus, frame1, frame2, frame3, frame4, frame5, frame6, frame7, b1, category1_f, category2_f, category3_f, scroll
    
    headerList = ["TICKET #","FAULT DATE","INFORMED AT","INFORMED BY","SITE ID","CATEGORY 1","CATEGORY 2","CATEGORY 3","FAULT DESCRIPTION","2G","3G","LTE","WiFi", "FAULT RECEIVER"]
    
    frame1 = Frame(main_win)
    frame1.config(relief=FLAT)

    date_of_fault_f = TOC_CalendarBox.CalendarFrame(main_win)
    date_of_fault_f.pack()
    dateOfFault = TOC_CalendarBox.ReturnDate()

    Label(frame1, text="FAULT INFORMED AT", font="TkFixedFont").grid(row=0, column=0, sticky=W, padx=(0,40))         
    timeOfFault = StringVar()
    time_of_fault_f = Entry(frame1, width=18, textvariable=timeOfFault)
    time_of_fault_f.grid(row=0, column=1, sticky=W, padx=(0,534))
    time_of_fault_f.configure(state='readonly')

    Label(frame1, text="FAULT INFORMED BY ", font="TkFixedFont").grid(row=1, column=0, sticky=W)
    faultInformedBy = StringVar()
    fault_informed_by_f = ttk.Combobox(frame1, textvariable=faultInformedBy, values=("","INOC", "Regional OP", "Dialog", "SLT"), state="readonly", width=11)
    fault_informed_by_f.current(1)
    fault_informed_by_f.grid(row=1, column=1, sticky=W)

    Label(frame1, text="SITE ID ", font="TkFixedFont").grid(row=2, column=0, sticky=W)
    siteID = StringVar()
    site_ID_f = Entry(frame1, width=106, textvariable=siteID)
    site_ID_f.grid(row=2, column=1, sticky=W, padx=(0,2))
    
    frame1.pack()

    frame2 = Frame(main_win)
    Label(frame2, text="FAULT CATEGORY ", font="TkFixedFont").grid(row=0, column=0, sticky=W, padx=(0,56))
    
    category1 = StringVar()
    category1_f = ttk.Combobox(frame2, textvariable=category1, values=("","SLT Tx","Mobitel Tx","Other Tx"), state="readonly", width=11)
    category1_f.grid(row=0, column=1, sticky=W, padx=(0,2))
    category1_f.bind('<<ComboboxSelected>>', update_list2)
    
    category2 = StringVar()
    category2_f = ttk.Combobox(frame2, textvariable=category2, state="readonly", width=16)
    category2_f.grid(row=0, column=2, sticky=W, padx=(0,2))
    category2_f.bind('<<ComboboxSelected>>', update_list3)
    
    category3 = StringVar()
    category3_f = ttk.Combobox(frame2, textvariable=category3, state="readonly", width=11)
    category3_f.grid(row=0, column=3, sticky=W, padx=(0,345))

    frame2.pack()
    
    frame3 = Frame(main_win)
    Label(frame3, text="FAULT DESCRIPTION ", font="TkFixedFont").grid(row=0, column=0, sticky=W)
    faultDescription = StringVar()
    fault_description_f = Entry(frame3, width=106, textvariable=faultDescription)
    fault_description_f.grid(row=0, column=1, sticky=W, padx=(0,6))

    twoG = IntVar()
    Label(frame3, text="SITES AFFECTED: •2G", font="TkFixedFont").grid(row=1, column=0, sticky=W)
    two_g_f = Entry(frame3, width=4, textvariable=twoG)
    two_g_f.grid(row=1, column=1, sticky=W)

    threeG = IntVar()
    Label(frame3, text=""+16*' '+"•3G ", font="TkFixedFont").grid(row=2, column=0, sticky=W)
    three_g_f = Entry(frame3, width=4, textvariable=threeG)
    three_g_f.grid(row=2, column=1, sticky=W)
    
    lte = IntVar()
    Label(frame3, text=""+16*' '+"•LTE ", font="TkFixedFont").grid(row=3, column=0, sticky=W)
    l_t_e_f = Entry(frame3, width=4, textvariable=lte)
    l_t_e_f.grid(row=3, column=1, sticky=W)

    wifi = IntVar()
    Label(frame3, text=""+16*' '+"•WiFi ", font="TkFixedFont").grid(row=4, column=0, sticky=W)
    wi_fi_f = Entry(frame3, width=4, textvariable=wifi)
    wi_fi_f.grid(row=4, column=1, sticky=W)
    frame3.pack()
    
    frame4 = Frame(main_win)
    frame4.configure(background='light slate gray')
    b1 = Button(frame4, width=10, text="ADD", command=addEntry, font="TkFixedFont")
    b1.pack(padx=10)
    b1.pack(side=LEFT)
    frame4.pack(pady=20)
    
    frame5 = Frame(main_win)
    openItems = Label(frame5, text="OPEN TICKETS", font=("TkFixedFont",12))
    openItems.config(relief=FLAT)
    openItems.pack()
    
    tree = ttk.Treeview(frame5,height=10,columns=headerList)
    tree['show'] = 'headings'
    i=0
    for item in headerList:
        tree.heading(str(i), text=item)
        i+=1
        
    tree.column("#0", width=0)
    tree.column("#1", width=60)
    tree.column("#2", width=80, anchor=CENTER)
    tree.column("#3", width=120, anchor=CENTER)
    tree.column("#4", width=95, anchor=CENTER)
    tree.column("#5", width=250)
    tree.column("#6", width=80, anchor=CENTER)
    tree.column("#7", width=100, anchor=CENTER)
    tree.column("#8", width=80, anchor=CENTER)
    tree.column("#9", width=300)
    tree.column("#10", width=40)
    tree.column("#11", width=40)
    tree.column("#12", width=40)
    tree.column("#13", width=40)
    tree.column("#14", width=96, anchor=CENTER)
    
    for item in openList:
        tree.insert("",'end',values=(item))

    tree.bind('<Double-1>', showEntry)
    scroll_y = Scrollbar(frame5, orient=VERTICAL)
    scroll_y.pack(side=RIGHT,fill=Y)  
    scroll_y.config(command=tree.yview)
    tree.configure(yscrollcommand=scroll_y.set)

    scroll_x = Scrollbar(frame5, orient=HORIZONTAL)
    scroll_x.pack(side=BOTTOM,fill=X)  
    scroll_x.config(command=tree.xview)
    tree.configure(xscrollcommand=scroll_x.set)
    
    tree.pack()
    frame5.pack(pady=(10,25))
    
    frame6 = Frame(main_win) 
    frame6.pack(pady=15)
    frame6.config(relief=FLAT)
    Label(frame6, text="FAULT RESPONSIBILITY  ", font="TkFixedFont").grid(row=0, column=0, sticky=W)
    faultResponsibility = StringVar()
    fault_responsibility_f = ttk.Combobox(frame6, textvariable=faultResponsibility, values=("","TxOP", "Regional OP", "SLT", "Dialog"), state="readonly", width=11)
    fault_responsibility_f.grid(row=0, column=1, sticky=W)

    Label(frame6, text="FAULT DETAILS ", font="TkFixedFont").grid(row=1, column=0, sticky=W)
    faultDetails = StringVar()
    fault_details_f = Entry(frame6, width=80, textvariable=faultDetails)
    fault_details_f.grid(row=1, column=1, sticky=W)

    Label(frame6, text="FAULT CAUSE  ", font="TkFixedFont").grid(row=2, column=0, sticky=W)
    faultCause = StringVar()
    fault_cause_f = ttk.Combobox(frame6, textvariable=faultCause, values=("","Annexure"), state="readonly", width=11)
    fault_cause_f.grid(row=2, column=1, sticky=W)

    Label(frame6, text="  TICKET STATUS ", font="TkFixedFont").grid(row=1, column=2, sticky=W)
    ticketStatus = "Open"
    ticket_status_f = Entry(frame6, width=5, textvariable=ticketStatus, relief=GROOVE)
    ticket_status_f.delete(0, END)
    ticket_status_f.insert(0, "Open")
    ticket_status_f.configure(state='readonly')
    ticket_status_f.grid(row=1, column=3, sticky=W)
    frame6.pack(pady=10)

    frame7 = Frame(main_win)
    frame7.configure(background='light slate gray')
    frame5.pack(pady=10)
    b2 = Button(frame7, width=10, text="← BACK", command=returnMain, font="TkFixedFont")
    b2.pack(padx=10)
    b3 = Button(frame7, width=10, text="UPDATE", command=updateEntry, font="TkFixedFont")
    b3.pack(padx=10)
    status = IntVar()
    check = Checkbutton(frame7, text="CLOSE TICKET", variable=status, font="TkFixedFont")
    check.pack(padx=10, pady=10)
    b2.pack(side=LEFT)
    b3.pack(side=LEFT)
    check.pack(side=LEFT)
    frame7.pack()

    if (str(passer) == "admin"):
        b4 = Button(frame4, width=10, text="REPORTS", command=showReports, font="TkFixedFont")
        b4.pack(padx=10)
        b4.pack(side=LEFT)

    b5 = Button(frame4, width=10, text="LOGOUT", command=logout, font="TkFixedFont")
    b5.pack(padx=10,side=LEFT)

    if (str(wintype) == "main"):
        frame6.forget()
        frame7.forget()


def update_list2(event):
    if (category1.get()=="SLT Tx"):
        category2_f['values'] = ["","Fiber Damage","Other"]
    elif (category1.get()=="Mobitel Tx"):
        category2_f['values'] = ["","MW Link Failure","E1 Failure","Eth Path Failure","Other"]
    elif (category1.get()=="Other Tx"):
        category2_f['values'] = ["","Etisalat","Dialog","Hutch","Airtel"]
    else:
        category2_f['values'] = [""]

    category3_f['values'] = [""]    
    category2_f.current(0)
    category3_f.current(0)


def update_list3(event):
    if (category2.get()=="Fiber Damage"):
        category3_f['values'] = ["","Linear","Non-Linear"]
    elif (category2.get()=="MW Link Failure"):
        category3_f['values'] = ["","Huawei","ZTE","NEC","Ericsson"]
    else:
        category3_f['values'] = [""]
    category3_f.current(0)

                              
def system_clock():
    main_win.after(1000, update_clock)


# Function for handling live clock and escalation notifications
def update_clock():
    site_count = 0
    system_clock()
    
    if (len(openList) == 0):
        return

    for item in openList:
        site_count += int(item[9]) + int(item[10]) + int(item[11]) + int(item[12])
    
    current_time = time_stamp()
    for item in openList:
        oldest_time = item[2]
        time_diff = time_between(oldest_time, current_time)/60

        if ((time_diff==15) and (site_count>20)):
            tm.showinfo("ESCALATION NOTICE", "CAUSE: Ticket "+ str(item[0]) +" (15 Minutes)\rContact Manager / Senior Engineer / Senior Manager")
                               
        elif ((time_diff==60) and (site_count>10) and (site_count<21)):
            tm.showinfo("ESCALATION NOTICE", "CAUSE: Ticket "+ str(item[0]) +" (1 Hour)\rContact Manager / Senior Engineer")
        
        elif ((time_diff==180) and (site_count>1) and (site_count<11)):
            tm.showinfo("ESCALATION NOTICE", "CAUSE: Ticket "+ str(item[0]) +" (3 Hours)\rContact Manager / Senior Engineer")
        elif ((time_diff==180) and (site_count>10) and (site_count<21)):
            tm.showinfo("ESCALATION NOTICE", "CAUSE: Ticket "+ str(item[0]) +" (3 Hours)\rContact Senior Manager")
        
        elif ((time_diff==360) and (site_count==1)):
            tm.showinfo("ESCALATION NOTICE", "CAUSE: Ticket "+ str(item[0]) +" (6 Hours)\rContact Manager / Senior Engineer")
        elif ((time_diff==360) and (site_count>1) and (site_count<11)):
            tm.showinfo("ESCALATION NOTICE", "CAUSE: Ticket "+ str(item[0]) +" (6 Hours)\rContact Senior Manager")
        
        elif ((time_diff==720) and (site_count==1)):
            tm.showinfo("ESCALATION NOTICE", "CAUSE: Ticket "+ str(item[0]) +" (12 Hours)\rContact Senior Manager")


# Function for finding difference between 2 timestamps
def time_between(date1, date2):
    d1 = datetime.datetime.strptime(date1, '%Y-%m-%d  %H:%M:%S')
    d2 = datetime.datetime.strptime(date2, '%Y-%m-%d  %H:%M:%S')
    return (d2 - d1).total_seconds()


# Function for obtaining current timestamp
def time_stamp():
    return datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d  %H:%M:%S')


# Function for centering window position on the screen    
def center_window(window):
    window.wm_state('zoomed')

        
#Initialisation conditions
def setup(using, passing):
    global main_win, user, passer
    user = using
    passer  = passing
    
    main_win = Tk()
    mainWindow("main")
    main_win.title("TOC")
    main_win.configure(background='light slate gray')
    center_window(main_win)
    main_win.focus_force()
    update_clock()
    main_win.mainloop()


