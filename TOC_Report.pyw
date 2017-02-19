from tkinter import *
import TOC_Main
import TOC_CalendarBox
import sqlite3
import csv
import tkinter.messagebox as tm

recordList = []

db = sqlite3.connect('TOC.db')
c = db.cursor()

headerList = ["TICKET #","FAULT DATE","INFORMED AT","INFORMED BY","SITE ID","CATEGORY 1","CATEGORY 2","CATEGORY 3","FAULT DESCRIPTION", "2G", "3G", "LTE", "WiFi", "FAULT RECEIVER", "RESPONSIBILITY", "FAULT DETAILS", "FAULT CAUSE", "TICKET STATUS"]


def show():
    filtering = "SELECT * FROM records WHERE DATE(TIME_OF_FAULT) >= ? AND DATE(TIME_OF_FAULT) <= ?"
    recordList.clear()
    tree.delete(*tree.get_children())
    if (cat1.get()==""):
        c.execute(filtering, (date1.get(),date2.get()))
    elif (cat1.get()!=""):
        filtering += "AND CATEGORY_1=?"
        c.execute(filtering, (date1.get(), date2.get(), cat1.get()))
        if (cat2.get()!=""):
            filtering += "AND CATEGORY_2=?"
            c.execute(filtering, (date1.get(), date2.get(), cat1.get(), cat2.get()))
            if (cat3.get()!=""):
                filtering += "AND CATEGORY_3=?"
                c.execute(filtering, (date1.get(), date2.get(), cat1.get(), cat2.get(), cat3.get()))
    while True:
        row = c.fetchone()
        if (row == None):
            break
        else:
            recordList.append(row)

    if (len(recordList)==0):
        tm.showinfo("WARNING", "No Records Found Between Selected Dates")
    else:
        for item in recordList:
            tree.insert("",'end',values=(item))


def back():
    root.destroy()
    TOC_Main.setup(sysUser,sysPasser)


def exportCSV():
    try:
        if (len(recordList)==0):
            tm.showerror("ERROR", "No Records Found")
        else:
            file = open("TOC-Report.csv", 'w',newline='')
            writer = csv.writer(file)
            writer.writerow(headerList)
            for item in recordList:
                writer.writerow(item)
            file.close()
            tm.showinfo("SUCCESS", "Report Was Generated (C:\Python34\Lib\TOC-Report.csv)")

    except PermissionError:
        tm.showerror("ERROR", "TOC-Report Is Already Open")   


# Main window design     
def window(win):
    global date1, date2, tree, cat1, cat2, cat3, cat_1, cat_2, cat_3
       
    frame1 = Frame(win)
    frame1.config(relief=FLAT)

    date_1 = TOC_CalendarBox.StartFrame(win)
    date_1.pack()
    date1 = TOC_CalendarBox.StartDate()

    date_2 = TOC_CalendarBox.EndFrame(win)
    date_2.pack()
    date2 = TOC_CalendarBox.EndDate()

    Label(frame1, text="CATEGORY FILTERS ", font="TkFixedFont").grid(row=0, column=0, sticky=W, padx=(0,15))
              
    cat1 = StringVar()
    cat_1 = ttk.Combobox(frame1, textvariable=cat1, values=("","SLT Tx","Mobitel Tx","Other Tx"), state="readonly", width=10)
    cat_1.grid(row=0, column=1, sticky=W, padx=(0,2))
    cat_1.bind('<<ComboboxSelected>>', update_list2)
    
    cat2 = StringVar()
    cat_2 = ttk.Combobox(frame1, textvariable=cat2, state="readonly", width=16)
    cat_2.grid(row=0, column=2, sticky=W, padx=(0,2))
    cat_2.bind('<<ComboboxSelected>>', update_list3)
    
    cat3 = StringVar()
    cat_3 = ttk.Combobox(frame1, textvariable=cat3, state="readonly", width=10)
    cat_3.grid(row=0, column=3, sticky=W, padx=(0,20))
    
    b1 = Button(frame1, width=10, text="SHOW", command=show, font="TkFixedFont")
    b1.grid(row=0, column=4, sticky=W)
    frame1.pack(pady=10)

    frame2 = Frame(win)
    frame2.configure(background='light slate gray')
    tree = ttk.Treeview(frame2,height=24,columns=headerList)
    tree['show'] = 'headings'
    i=0
    for item in headerList:
        tree.heading(str(i), text=item)
        i+=1
        
    tree.column("#0", width=0)
    tree.column("#1", width=60)
    tree.column("#2", width=80, anchor=CENTER)
    tree.column("#3", width=120, anchor=CENTER)
    tree.column("#4", width=90, anchor=CENTER)
    tree.column("#5", width=300)
    tree.column("#6", width=100, anchor=CENTER)
    tree.column("#7", width=100, anchor=CENTER)
    tree.column("#8", width=100, anchor=CENTER)
    tree.column("#9", width=300)
    tree.column("#10", width=40)
    tree.column("#11", width=40)
    tree.column("#12", width=40)
    tree.column("#13", width=40)
    tree.column("#14", width=100, anchor=CENTER)
    tree.column("#15", width=100, anchor=CENTER)
    tree.column("#16", width=300)
    tree.column("#17", width=90, anchor=CENTER)
    tree.column("#18", width=165)
    
    for item in recordList:
        tree.insert("",'end',values=(item))

    scrollbar_y = Scrollbar(frame2, orient=VERTICAL)
    scrollbar_y.pack(side=RIGHT,fill=Y)  
    scrollbar_y.config(command=tree.yview)
    tree.configure(yscrollcommand=scrollbar_y.set)

    scrollbar_x = Scrollbar(frame2, orient=HORIZONTAL)
    scrollbar_x.pack(side=BOTTOM,fill=X)  
    scrollbar_x.config(command=tree.xview)
    tree.configure(xscrollcommand=scrollbar_x.set)
    
    tree.pack()
    frame2.pack(pady=10)

    frame3 = Frame(win)
    frame3.configure(background='light slate gray')
    b2 = Button(frame3, width=10, text="← BACK", command=back, font="TkFixedFont").pack(padx=(30,10),side=LEFT)
    b3 = Button(frame3, width=10, text="EXPORT", command=exportCSV, font="TkFixedFont").pack(padx=10,side=LEFT)
    frame3.pack(pady=15)

    recordList.clear()
    tree.delete(*tree.get_children())


def update_list2(event):
    if (cat1.get()=="SLT Tx"):
        cat_2['values'] = ["","Fiber Damage","Other"]
    elif (cat1.get()=="Mobitel Tx"):
        cat_2['values'] = ["","MW Link Failure","E1 Failure","Eth Path Failure","Other"]
    elif (cat1.get()=="Other Tx"):
        cat_2['values'] = ["","Etisalat","Dialog","Hutch","Airtel"]
    else:
        cat_2['values'] = [""]

    cat_3['values'] = [""]    
    cat_2.current(0)
    cat_3.current(0)


def update_list3(event):
    if (cat2.get()=="Fiber Damage"):
        cat_3['values'] = ["","Linear","Non-Linear"]
    elif (cat2.get()=="MW Link Failure"):
        cat_3['values'] = ["","Huawei","ZTE","NEC","Ericsson"]
    else:
        cat_3['values'] = [""]
    cat_3.current(0)

        
def setup(using, passing):
    global root,sysUser,sysPasser
    sysUser = using
    sysPasser = passing
    root = Tk()
    root.title("REPORTS")
    window(root)
    root.configure(background='light slate gray')
    TOC_Main.center_window(root)
    root.focus_force()
    root.mainloop()
