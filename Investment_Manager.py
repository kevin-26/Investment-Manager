from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter import scrolledtext
import os
import csv
import pymongo
import datetime
import webbrowser

client = pymongo.MongoClient('mongodb+srv://User:lfs37lfs37@cluster0-dwdr2.mongodb.net/test?retryWrites=true&w=majority')
db = client["PythonProject"]
data = db["info"]

usr=''

def homepage():
    root = Tk()
    root.title('Investment Manager')
    root.resizable(0, 0)

    cho1 = None #global variable that determines what we have chosen: Fixed Deposit or Mutual Fund or Assets
    choice_list = ['Fixed Deposit','Mutual Fund','Bank Account']

    now = datetime.datetime.now()
    today_date = now.strftime("%d-%m-%Y") #used in display function/mongoDDB to calculate elapsed time

    def new_button():
        new = Toplevel()
        new.title('New Investment')
        new.geometry('+250+250')

        choice = cho1.get() #VVIMP
        
        if choice == 'Fixed Deposit':

            l1 = Label(new,text='Bank')
            l2 = Label(new,text='Principal')
            l3 = Label(new,text='Rate') #Annual Rate
            l4 = Label(new,text='C.I. Interval(Months)') #In months
            l5 = Label(new,text='Start Date') # DD-MM-YYYY
            l6 = Label(new,text='Period(Years)') #Time in Years, minimum one year

            e1 = Entry(new)
            e2 = Entry(new)
            e3 = Entry(new)
            e4 = Entry(new)
            e5 = Entry(new)
            e6 = Entry(new)

            l1.grid(row=1,column=1,padx=5,pady=2)
            l2.grid(row=2,column=1)
            l3.grid(row=3,column=1)
            l4.grid(row=4,column=1)
            l5.grid(row=5,column=1)
            l6.grid(row=6,column=1)

            e1.grid(row=1,column=2,padx=5,pady=2)
            e2.grid(row=2,column=2)
            e3.grid(row=3,column=2)
            e4.grid(row=4,column=2)
            e5.grid(row=5,column=2)
            e6.grid(row=6,column=2)

            def save_changes():
                
                response = messagebox.askquestion('Save','Save Investment?',icon = 'warning')
                if response == 'yes':
                    bank = e1.get()
                    principal = int(float(e2.get()))
                    rate = float(e3.get())
                    interval = int(float(e4.get()))
                    start_date = e5.get()
                    period = int(float(e6.get()))

                    temp = int(float(start_date[6:10]))
                    new_year = temp+period
                    r=rate / 100
                    t = period
                    # A = (P)*((1+(r/n))**(n*t))
                    n = 12 / interval
                    amount = principal * pow(1 + r / n, n * t) #float
                    interest = amount - principal       #float
                    amount = round(amount, 2)
                    interest = round(interest, 2)
                    maturity_date = start_date[0:6]+str(new_year)
                    #All necessary calclulations are made and variables defined
                    #MongoDB query goes below:


                    messagebox.showinfo(title = None, message = 'Investment Saved')
                    #For testing purposes
                    # test_label1 = Label(new, text = 'Amount: ' + str(amount))
                    # test_label2 = Label(new,text = 'Maturity Date: ' + maturity_date)

                    # test_label1.grid(row = 8)
                    # test_label2.grid(row = 9)
                

            button_save = Button(new, text = 'Save',relief = GROOVE, command = save_changes)
            button_save.grid(row = 7, column = 1, padx = 30, pady = 15)
        
        elif choice == 'Mutual Fund':
            l1 = Label(new,text = 'Company')
            l2 = Label(new,text = 'Net Asset Value(Initial)')
            l3 = Label(new,text = 'Units Bought')
            l4 = Label(new,text = 'Net Asset Value(At maturity)')
            l5 = Label(new,text = 'Period(Years)') 

            e1 = Entry(new)
            e2 = Entry(new)
            e3 = Entry(new)
            e4 = Entry(new)
            e5 = Entry(new)

            l1.grid(row=1,column=1,padx=5,pady=2)
            l2.grid(row=2,column=1)
            l3.grid(row=3,column=1)
            l4.grid(row=4,column=1)
            l5.grid(row=5,column=1)

            e1.grid(row=1,column=2,padx=5,pady=2)
            e2.grid(row=2,column=2)
            e3.grid(row=3,column=2)
            e4.grid(row=4,column=2)
            e5.grid(row=5,column=2)

            def save_changes():
                
                response = messagebox.askquestion('Save','Save Investment?',icon='warning')
                if response == 'yes':
                    company = e1.get()
                    nav1 = int(float(e2.get()))
                    nou = int(float(e3.get()))
                    nav2 = int(float(e4.get()))
                    period = int(float(e5.get()))

                    #All necessary calclulations are made and variables defined
                    #MongoDB query goes below:


                    messagebox.showinfo(title=None,message='Investment Saved')
                

            button_save = Button(new, text = 'Save',relief = GROOVE, command = save_changes)
            button_save.grid(row=7,column=1,padx = 30,pady=15)

        
        elif choice == 'Bank Account':
            
            l1 = Label(new,text='Bank')
            l2 = Label(new,text='Current Balance')
            l3 = Label(new,text='Type') #Annual Rate
            l4 = Label(new,text='Rate') #In months
            l5 = Label(new,text='Compounding Interval(Months)') # DD-MM-YYYY

            e1 = Entry(new)
            e2 = Entry(new)
            e3 = Entry(new)
            e4 = Entry(new)
            e5 = Entry(new)

            l1.grid(row=1,column=1,padx=5,pady=2)
            l2.grid(row=2,column=1)
            l3.grid(row=3,column=1)
            l4.grid(row=4,column=1)
            l5.grid(row=5,column=1)

            e1.grid(row=1,column=2,padx=5,pady=2)
            e2.grid(row=2,column=2)
            e3.grid(row=3,column=2)
            e4.grid(row=4,column=2)
            e5.grid(row=5,column=2)

            def save_changes():
                
                response = messagebox.askquestion('Save','Save Investment?',icon='warning')
                if response == 'yes':
                    bank = e1.get()
                    current_balance = int(float(e2.get()))
                    type_account = e3.get()
                    rate = float(e4.get())
                    interval = int(float(e5.get()))
                    #All necessary calclulations are made and variables defined
                    #MongoDB query goes below:


                    messagebox.showinfo(title=None,message='Investment Saved')
                    
            button_save = Button(new, text = 'Save', relief = GROOVE, command = save_changes)
            button_save.grid(row = 7, column = 1, padx = 30, pady = 15)
        new.mainloop()


    def display_button():
    	return # Problems with integrating above classes into this function
    



    def about_button():
        about = Toplevel()
        about.title('About')
        info_label = Label(about, text = 'Made by:\n\nKevin Shah\nParth Shah\nBhuvnesh Solanki')
        info_label.grid(row = 0, column = 0, padx = (50,55), pady = (15,15))
        about.geometry('200x100+30+30')
    
    def version_button():
        version = Toplevel()
        version.title('Version')
        info_label = Label(version, text = 'Investment Manager\nVersion: 1.0.0')
        info_label.grid(row = 0, column = 0, padx = (50,50), pady = (10,10))
    
    def help_button():
        url = "https://github.com/KevinShahgit/Investment-Manager/blob/master/README.md"
        webbrowser.open(url,new=1)
    
    def callback(*args):
        button_new.config(state = "normal")
        button_display.config(state = "normal")

    label_home = Label(root, text = 'HOMEPAGE', font = ('Verdana', 13))
    label_home.grid(row = 1, column = 1, padx = 20, pady = 5)


    label_usr = Label(root,text='Hi '+str(usr))
    label_usr.grid(row=0,column=4)

    m1 = Menu(root)
    root.config(menu = m1)
    m1.add_command(label = "About", command = about_button)
    m1.add_command(label = "Version", command = version_button)
    m1.add_command(label = "Help", command = help_button)

    button_new = Button(root, text = 'NEW',relief = GROOVE , command = new_button, state = DISABLED)
    button_display = Button(root, text = 'DISPLAY',relief = GROOVE, command = display_button, state = DISABLED)

    button_new.grid(row=3,column=0,padx=10,pady=(30,10))
    button_display.grid(row=3,column=2,padx=10,pady=(30,10))

    cho1 = StringVar()  #VVIMP
    cho1.set('Choose an option')
    cho1.trace("w", callback)
    choice_menu = OptionMenu(root, cho1, *choice_list)
    choice_menu.grid(row = 2, column = 1, padx = 10, pady = (30,10))

    label_day = Label(root, text = 'Date: ' + today_date)
    label_day.grid(row = 7)

    root.mainloop()

def close(event):
    temp.destroy()
    return "break"


def add(event):
    global temp
    a = data.find_one({"_id": nameSign.get()})
    if(a is not None):
        temp = Toplevel(roots)
        temp.config(bg = "black")
        temp.title("Invalid SignUp")
        temp.resizable(0, 0)
        temp.geometry("300x100")
        msg = Label(temp, text = "Username already exists. Please try again.", bg = "black", fg = "white", font = ("Verdana", 8))
        msg.place(x = 35, y = 30)
        bt = Button(temp, text = "Ok", height = 1, width = 3, bg = "white", relief = "groove")#command = close,
        bt.place(x = 115, y = 55)
        bt.bind("<1>", close)
        bt.bind("<Return>", close)
    else:
        d = {
        "_id" : nameSign.get(),
        "password" : pwordSign.get()
        }
        data.insert_one(d)
        roots.destroy()
        login()


def signup(event):
    global pwordSign
    global nameSign
    global roots

    roots = Tk()
    roots.title('Signup')
    roots.resizable(0, 0)
    instruction = Label(roots,
                        text = 'Please Enter new Credentials',
                        bg = "black",
                        fg = "white",
                        font = ("Verdana", 13))
    instruction.place(x = 20, y = 5)
    roots.geometry("300x200")
    roots.config(background = "black", pady = 10)
    nameL = Label(roots, text = 'New Username: ', bg = "black", fg = "white")
    pwordL = Label(roots, text = 'New Password: ', bg = "black", fg = "white")
    nameL.place(x = 10, y = 40)
    pwordL.place(x = 10, y = 80)

    nameSign = Entry(roots)
    pwordSign = Entry(roots, show = '*')
    nameSign.place(x = 110, y = 40)
    pwordSign.place(x = 110, y = 80)

    dis = Label(roots, text = "", bg = "black", fg = "white")
    signupButton = Button(roots, text = 'Signup')#, command = add
    signupButton.bind("<1>", add)
    signupButton.bind("<Return>", add)
    signupButton.place(x = 110, y = 120)
    rootA.destroy()
    roots.mainloop()

def checklogin(event):
    a = data.find_one({"_id" : nameLog.get()})
    if a is not None and nameLog.get() == a.get("_id") and pwordLog.get() == a.get("password"):
        global usr
        usr = nameLog.get()
        rootA.destroy()
        homepage()
    else:
        r = Toplevel(rootA)
        r.title('D:')
        r.geometry('150x50')
        rlbl = Label(r, text='\nInvalid Login. Please try again.')
        rlbl.pack()
        r.mainloop()
    return "break"


def login():
    global nameLog
    global pwordLog
    global rootA
    rootA = Tk()
    rootA.title('Login')
    rootA.geometry("300x200")
    rootA.resizable(0, 0)
    rootA.config(background="black", pady = 10)
    instruction = Label(rootA,
                        text = 'Please Login\n',
                        bg = "black",
                        fg = "white",
                        font = 20)
    instruction.place(x = 110, y = 5)

    nameTemp = Label(rootA, text = 'Username: ', bg = "black", fg = "white")
    pwordTemp = Label(rootA, text = 'Password: ', bg = "black", fg = "white")
    nameTemp.place(x = 10, y = 40)
    pwordTemp.place(x = 10, y = 80)

    nameLog = Entry(rootA)
    pwordLog = Entry(rootA, show = '*')
    nameLog.place(x = 110, y = 40)
    pwordLog.place(x = 110, y = 80)

    loginB = Button(rootA, text = 'Login')
    loginB.place(x = 110, y = 120)
    loginB.bind("<1>", checklogin)
    loginB.bind("<Return>", checklogin)

    signUp = Button(rootA, text='Signup')
    signUp.place(x = 160, y = 120)
    signUp.bind("<1>", signup)
    signUp.bind("<Return>", signup)
    rootA.mainloop()



if __name__ == '__main__':
    login()