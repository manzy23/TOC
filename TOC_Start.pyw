from tkinter import *
import tkinter.messagebox as tm
import TOC_Main


class LoginFrame(Frame):
    def __init__(self, master):
        super().__init__(master)
        global userName, passWord

        self.label_1 = Label(self, text="  USERNAME", font="TkFixedFont")
        self.entry_1 = Entry(self)
        userName = self.entry_1
        self.entry_1.focus()
        self.label_1.grid(row=0, column=0, sticky=W, pady=(10,0))
        self.entry_1.grid(row=0, column=1, padx=(0,10), pady=(10,0))
        
        self.label_2 = Label(self, text="  PASSWORD", font="TkFixedFont")
        self.entry_2 = Entry(self, show="*")
        passWord = self.entry_2
        self.label_2.grid(row=1, column=0, sticky=W)
        self.entry_2.grid(row=1, column=1, padx=(0,10), pady=(0,5))

        self.logbtn = Button(self, width=10, text="LOGIN", command = self.login_btn_clicked, font="TkFixedFont")
        self.logbtn.grid(row=2,column=0, padx=(20,0) ,pady=(10,15))
        self.exitbtn = Button(self, width=10, text="EXIT", command = self.system_exit, font="TkFixedFont")
        self.exitbtn.grid(row=2,column=1, pady=(10,15))
        self.pack(pady=10)

    def login_btn_clicked(self):
        username = self.entry_1.get()
        password = self.entry_2.get()

        if((password == "admin") or (password == "user")):
            root.destroy()
            TOC_Main.setup(username, password)  
        else:
            tm.showerror("ERROR", "Incorrect Username/Password")

    def system_exit(self):
        root.destroy()

        
def enter_pressed(event):
    username=userName.get()
    if(passWord.get() == "admin"):
        root.destroy()
        TOC_Main.setup(username,"admin") 
    elif(passWord.get() == "user"):
        root.destroy()
        TOC_Main.setup(username,"user") 
    else:
        tm.showerror("ERROR", "Incorrect Username/Password")


def center_window(window,width,height):
    width_screen = window.winfo_screenwidth() 
    height_screen = window.winfo_screenheight()
    x = (width_screen/2) - (width/2)
    y = (height_screen/2) - (height/2)
    window.geometry('%dx%d+%d+%d' % (width, height, x, y))
            
def setup():
    global root
    root = Tk()
    root.title("LOGIN")
    root.configure(background='light slate gray')
    root.resizable(width=False, height=False)
    center_window(root, 260, 130)
    LoginFrame(root)
    root.focus_force()
    root.bind('<Return>', enter_pressed)
    root.mainloop()

if __name__ == "__main__":
    setup()
