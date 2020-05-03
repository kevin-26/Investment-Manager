from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import os
import pymongo
from datetime import date, datetime
from dateutil.relativedelta import relativedelta  # pip install python-dateutil
import webbrowser

# Global Variables (add more if required)
nameLog = ''
pwordLog = ''
usr = ''


# End of globals


client = pymongo.MongoClient(
    'mongodb+srv://User:lfs37lfs37@cluster0-dwdr2.mongodb.net/test?retryWrites=true&w=majority')
db = client["PythonProject"]
data = db["info"]

class bank_account(Toplevel):

    def __init__(self, master):
        Toplevel.__init__(self, master)
        self.title('Bank account')
        self.data = dict()
        # Add to labelframe for select item and insert item.
        self.selectframe = ttk.LabelFrame(self, text='Select Item')
        self.selectframe.pack(side='left', anchor='n', fill='both')
        self.insertframe = ttk.LabelFrame(self, text='Ite')
        self.insertframe.pack(anchor='n',
                              fill='both'
                              )
        self.displayframe = ttk.LabelFrame(self, text='Details')
        self.displayframe.pack(side='bottom', expand=True, fill='both')

        # Add a ttk treeview for the display of transaction.
        self.display_tree = ttk.Treeview(self.displayframe)
        self.display_tree.pack(side='left', expand=True, fill='both')
        self.disyscroll = Scrollbar(self.displayframe,
                                    command=self.display_tree.yview)
        self.disyscroll.pack(side='left', fill='y')
        self.display_tree.config(yscrollcommand=self.disyscroll.set)
        self.column = ('bank',
                       'current balance',
                       'type',
                       'rate',
                       'compounding interval',
                       'interest',
                       'amount',
                       'remarks')
        self.heading = ('Bank',
                        'Current Balance',
                        'Type',
                        'Rate',
                        'Compounding Interval',
                        'Interest',
                        'Amount',
                        'Remarks')
        self.display_tree['columns'] = self.column
        for elem in self.column:
            if elem == 'compounding interval':
                col_width = 80
            elif elem == 'remarks':
                col_width = 135
            else:
                col_width = 100

            if elem == 'remarks':
                self.display_tree.column(elem, width=col_width)
            else:
                self.display_tree.column(elem, width=col_width, stretch=False)

        counter = 0
        self.display_tree.heading('#0', text='S. No.')
        self.display_tree.column('#0', width=50, stretch=False)
        for elem in self.column:
            self.display_tree.heading(elem, text=self.heading[counter])
            counter += 1
        # Create tags for treeview.
        self.display_tree.tag_configure('evenrow', background='#FFB586')
        self.display_tree.tag_configure('oddrow', background='#FDA46A')

        # Add a delete and edit button for under tree view for
        # database manipulation and editing.
        self.delete_btn = ttk.Button(self.displayframe, text='Delete')
        self.delete_btn.pack(padx=5, pady=5)
        # self.edit_btn = ttk.Button(self.displayframe, text='Edit')
        # self.edit_btn.pack(padx=5, pady=5)

        # Create and add a list box and a entry inside selectframe.
        self.searchitem_entry = ttk.Entry(self.selectframe)
        self.searchitem_entry.pack(fill='x')
        self.searchitem_entry.bind('<KeyPress>')
        self.itemlistbox = Listbox(self.selectframe)
        self.itemlistbox.pack(side='left', fill='both')
        self.yscroll = Scrollbar(self.selectframe,
                                 command=self.itemlistbox.yview)
        self.yscroll.pack(side='left', fill='y')
        self.itemlistbox.config(yscrollcommand=self.yscroll.set)
        self.itemlistbox.bind('<Double-Button-1>')

        # Create labels inside the insert frame.
        self.bank_label = ttk.Label(self.insertframe, text='Bank: ')
        self.bank_label.grid(row=0, column=0, sticky='e')
        self.balance_label = ttk.Label(self.insertframe, text='Current Balance: ')
        self.balance_label.grid(row=0, column=2, sticky='e')
        self.type_label = ttk.Label(self.insertframe, text='Type: ')
        self.type_label.grid(row=0, column=5, sticky='e')
        self.rate_label = ttk.Label(self.insertframe, text='Rate: ')
        self.rate_label.grid(row=2, column=0, sticky='e')
        self.ci_label = ttk.Label(self.insertframe, text='Compounding interval: ')
        self.ci_label.grid(row=2, column=2, sticky='e')

        # Create entries inside the insert frame.
        self.bank_entry = ttk.Entry(self.insertframe)
        self.bank_entry.grid(row=0, column=1, sticky='e')
        self.balance_entry = ttk.Entry(self.insertframe, width=20)
        self.balance_entry.grid(row=0, column=3, sticky='e')
        self.type_entry = ttk.Entry(self.insertframe, width=20)
        self.type_entry.grid(row=0, column=6, sticky='e')
        self.rate_entry = ttk.Entry(self.insertframe, width=20)
        self.rate_entry.grid(row=2, column=1, sticky='e')
        self.ci_entry = ttk.Entry(self.insertframe, width=20)
        self.ci_entry.grid(row=2, column=3, sticky='e')

        # Create cancel save button

        self.cancel_btn = ttk.Button(self.insertframe,
                                     text='Cancel', command=self.cancel_button)
        self.cancel_btn.grid(row=3, column=7, sticky='e')
        self.save_btn = ttk.Button(self.insertframe,
                                   text='Save', command = self.save_button)
        self.save_btn.grid(row=3, column=6, sticky='e')
        #Inserting values
        retrieve = data.find_one({"_id": usr})
        rows = retrieve.get("bank")
        if rows is not None:
          for r in range(len(rows)):  
            temp = rows[r]
            self.data[r+1] = temp
            self.display_tree.insert('', 'end', text = (r + 1), values = temp)


    def cancel_button(self):
      self.bank_entry.delete(0, 'end')
      self.balance_entry.delete(0, 'end')
      self.type_entry.delete(0, 'end')
      self.rate_entry.delete(0, 'end')
      self.ci_entry.delete(0, 'end')
    
    def save_button(self): # This is the edit function kevin
      num = int(float(self.searchitem_entry.get()))
      if num <= len(self.data):
        bank = self.bank_entry.get()
        current_balance = int(float(balance_entry.get()))
        type_account = type_entry.get()
        rate = float(rate_entry.get())
        interval = int(float(ci_entry.get()))

        r = rate / 100
        n = 12 / interval
        amount = current_balance * pow(1 + r / n, 1)  # float
        interest = amount - current_balance  # float
        amount = round(amount, 2)
        interest = round(interest, 2)
        


class fixed_deposit(Toplevel):

    def __init__(self, master):
        Toplevel.__init__(self, master)

        # Set the window title.
        self.title('Fixed deposit')
        self.data = dict() # This is the dictionary kevin
        # Add to labelframe for select item and insert item.
        self.selectframe = ttk.LabelFrame(self, text='Select Item')
        self.selectframe.pack(side='left', anchor='n', fill='both')
        self.insertframe = ttk.LabelFrame(self, text='Item details')
        self.insertframe.pack(anchor='n',
                              fill='both'
                              )
        self.displayframe = ttk.LabelFrame(self, text='Display')
        self.displayframe.pack(side='bottom', expand=True, fill='both')

        # Add a ttk treeview for the display of transaction.
        self.display_tree = ttk.Treeview(self.displayframe)
        self.display_tree.pack(side='left', expand=True, fill='both')
        self.disyscroll = ttk.Scrollbar(self.displayframe, command=self.display_tree.yview)
        self.disyscroll.pack(side='left', fill='y')
        self.display_tree.config(yscrollcommand=self.disyscroll.set)
        self.column = ('bank',
                       'principal',
                       'rate',
                       'c.i interval',
                       'investment date',
                       'maturity date',
                       'interest'
                       'amount',
                       'remarks')
        self.heading = ('Bank',
                        'Principal',
                        'Rate',
                        'C.I Interval',
                        'Investment Date',
                        'Maturity Date',
                        'Interest',
                        'Amount',
                        'Remarks')
        self.display_tree['columns'] = self.column
        for elem in self.column:
            if elem == 'maturity date':
                col_width = 150
            elif elem == 'investment date':
                col_width = 150
            elif elem == 'remarks':
                col_width = 175
            else:
                col_width = 100
            self.display_tree.column(elem, width=col_width)

        counter = 0
        self.display_tree.heading('#0', text='S. No.')
        self.display_tree.column('#0', width=35)
        for elem in self.column:
            self.display_tree.heading(elem, text=self.heading[counter])
            counter += 1

        self.display_tree.tag_configure('evenrow', background='#FFB586')
        self.display_tree.tag_configure('oddrow', background='#FDA46A')

        self.delete_btn = ttk.Button(self.displayframe, text='Delete')
        self.delete_btn.pack(padx=5, pady=5)

        self.searchitem_entry = ttk.Entry(self.selectframe)
        self.searchitem_entry.pack(fill='x')
        self.searchitem_entry.bind('<KeyPress>')
        self.itemlistbox = Listbox(self.selectframe)
        self.itemlistbox.pack(side='left', fill='both')
        self.yscroll = ttk.Scrollbar(self.selectframe, command=self.itemlistbox.yview)
        self.yscroll.pack(side='left', fill='y')
        self.itemlistbox.config(yscrollcommand=self.yscroll.set)
        self.itemlistbox.bind('<Double-Button-1>')

        self.bank_label = ttk.Label(self.insertframe, text='Bank:')
        self.bank_label.grid(row=0, column=0, sticky='e')
        self.principal_label = ttk.Label(self.insertframe, text='Principal:')
        self.principal_label.grid(row=0, column=2, sticky='e')
        self.rate_label = ttk.Label(self.insertframe, text='Rate:')
        self.rate_label.grid(row=0, column=4, sticky='e')
        self.interval_label = ttk.Label(self.insertframe, text='C.I. Interval:')
        self.interval_label.grid(row=1, column=0, sticky='e')
        self.start_label = ttk.Label(self.insertframe, text='Start Date:')
        self.start_label.grid(row=1, column=2, sticky='e')

        self.bank_entry = ttk.Entry(self.insertframe, width=20)
        self.bank_entry.grid(row=0, column=1, sticky='w')
        self.principal_entry = ttk.Entry(self.insertframe, width=20)
        self.principal_entry.grid(row=0, column=3, sticky='w')
        self.rate_entry = ttk.Entry(self.insertframe, width=20)
        self.rate_entry.grid(row=0, column=5, sticky='w')
        self.interval_entry = ttk.Entry(self.insertframe, width=20)
        self.interval_entry.grid(row=1, column=1, sticky='w')
        self.start_entry = ttk.Entry(self.insertframe, width=20)
        self.start_entry.grid(row=1, column=3, sticky='w')

        # Create cancel save button
        self.cancel_btn = ttk.Button(self.insertframe,
                                     text='Cancel', command=self.cancel_button)
        self.cancel_btn.grid(row=4, column=6, sticky='e')
        self.save_btn = ttk.Button(self.insertframe,
                                   text='Save', command = self.save_button)
        self.save_btn.grid(row=4, column=5, sticky='e')

        #Inserting values
        retrieve = data.find_one({"_id": usr})
        rows = retrieve.get("fixed")
        if rows is not None:
          for r in range(len(rows)):  
            temp = rows[r]
            self.data[r+1] = temp
            self.display_tree.insert('', 'end', text = (r + 1), values = temp)

    def cancel_button(self):
      self.bank_entry.delete(0, 'end')
      self.principal_entry.delete(0, 'end')
      self.rate_entry.delete(0, 'end')
      self.interval_entry.delete(0, 'end')
      self.start_entry.delete(0, 'end')
    
    def save_button(self):
      num = self.searchitem_entry.get()
      if num <= len(self.data):
        pass
          
          
        


class mutual_funds(Toplevel):

    def __init__(self, master):
        Toplevel.__init__(self, master)

        # Set the window title.
        self.title('Mutual Funds')
        self.data = dict()
        # Add to labelframe for select item and insert item.
        self.selectframe = ttk.LabelFrame(self, text='Select Item')
        self.selectframe.pack(side='left', anchor='n', fill='both')
        self.insertframe = ttk.LabelFrame(self, text='Item details')
        self.insertframe.pack(anchor='n',
                              fill='both'
                              )
        self.displayframe = ttk.LabelFrame(self, text='Display')
        self.displayframe.pack(side='bottom', expand=True, fill='both')

        # Add a ttk treeview for the display of transaction.
        self.display_tree = ttk.Treeview(self.displayframe)
        self.display_tree.pack(side='left', expand=True, fill='both')
        self.disyscroll = ttk.Scrollbar(self.displayframe, command=self.display_tree.yview)
        self.disyscroll.pack(side='left', fill='y')
        self.display_tree.config(yscrollcommand=self.disyscroll.set)
        self.column = ('company',
                       'nav-buying',
                       'units',
                       'investment',
                       'date of buying/investing',
                       'estimated nav',
                       'amount',
                       'Maturity date',
                       'remarks')
        self.heading = ('Company',
                        'NAV-Buying',
                        'Units',
                        'Investment',
                        'Date of Buying/Investing',
                        'Estimated NAV',
                        'Amount',
                        'Maturity date',
                        'Remarks')
        self.display_tree['columns'] = self.column
        for elem in self.column:
            if elem == 'date':
                col_width = 75
            elif elem == 'date of buying/investing':
                col_width = 200
            elif elem == 'units':
                col_width = 35
            elif elem == 'remarks':
                col_width = 175
            else:
                col_width = 100
            self.display_tree.column(elem, width=col_width)

        counter = 0
        self.display_tree.heading('#0', text='S. No.')
        self.display_tree.column('#0', width=35)
        for elem in self.column:
            self.display_tree.heading(elem, text=self.heading[counter])
            counter += 1
        # Create tags for treeview.
        self.display_tree.tag_configure('evenrow', background='#FFB586')
        self.display_tree.tag_configure('oddrow', background='#FDA46A')

        # Add a delete and edit button for under tree view for
        # database manipulation and editing.
        self.delete_btn = ttk.Button(self.displayframe, text='Delete')
        self.delete_btn.pack(padx=5, pady=5)

        # Create and add a list box and a entry inside selectframe.
        self.searchitem_entry = ttk.Entry(self.selectframe)
        self.searchitem_entry.pack(fill='x')
        self.searchitem_entry.bind('<KeyPress>')
        self.itemlistbox = Listbox(self.selectframe)
        self.itemlistbox.pack(side='left', fill='both')
        self.yscroll = ttk.Scrollbar(self.selectframe, command=self.itemlistbox.yview)
        self.yscroll.pack(side='left', fill='y')
        self.itemlistbox.config(yscrollcommand=self.yscroll.set)
        self.itemlistbox.bind('<Double-Button-1>')

        # Create labels inside the insert frame.
        self.company_name = ttk.Label(self.insertframe, text='Company: ')
        self.company_name.grid(row=0, column=0, sticky='e')
        self.navbuying_label = ttk.Label(self.insertframe, text='NAV-Buying: ')
        self.navbuying_label.grid(row=0, column=2, sticky='e')
        self.units_bought = ttk.Label(self.insertframe, text='Units Bought: ')
        self.units_bought.grid(row=0, column=4, sticky='e')
        self.navmd_label = ttk.Label(self.insertframe, text='NAV-Maturity date: ')
        self.navmd_label.grid(row=1, column=0, sticky='e')
        self.period_label = ttk.Label(self.insertframe, text='Period: ')
        self.period_label.grid(row=1, column=2, sticky='e')

        # # Create entries inside the insert frame.
        self.company_entry = ttk.Entry(self.insertframe, width=20)
        self.company_entry.grid(row=0, column=1, sticky='w')
        self.navbuying_entry = ttk.Entry(self.insertframe, width=20)
        self.navbuying_entry.grid(row=0, column=3, sticky='w')
        self.units_entry = ttk.Entry(self.insertframe, width=20)
        self.units_entry.grid(row=0, column=5, sticky='w')
        self.navmd_entry = ttk.Entry(self.insertframe, width=20)
        self.navmd_entry.grid(row=1, column=1, sticky='w')
        self.period_entry = ttk.Entry(self.insertframe, width=20)
        self.period_entry.grid(row=1, column=3, sticky='w')

        # Create cancel save button
        self.cancel_btn = ttk.Button(self.insertframe, text='Cancel', command=self.cancel_button)
        self.cancel_btn.grid(row=2, column=6, sticky='e')
        self.save_btn = ttk.Button(self.insertframe, text='Save')
        self.save_btn.grid(row=2, column=5, sticky='e')

        #Inserting values
        retrieve = data.find_one({"_id": usr})
        rows = retrieve.get("mutual")
        if rows is not None:
          for r in range(len(rows)):  
            temp = rows[r]
            self.display_tree.insert('', 'end', text = (r + 1), values = temp)

    def cancel_button(self):
        self.company_entry.delete(0, 'end')
        self.navbuying_entry.delete(0, 'end')
        self.units_entry.delete(0, 'end')
        self.navmd_entry.delete(0, 'end')
        self.period_entry.delete(0, 'end')


class Home:
    def __init__(self):
        self.homepage()

    def homepage(self):
        root = Tk()
        root.title("Investment Manager")
        root.resizable(0, 0)

        cho1 = None  # variable that determines what we have chosen: Fixed Deposit or Mutual Fund or Assets
        choice_list = ['Fixed Deposit', 'Mutual Fund', 'Bank Account']

        today = date.today()
        today_date = today.strftime("%d-%m-%Y")  # used in display function/mongoDDB to calculate elapsed time

        def new_button():
            new = Toplevel()
            new.title('New Investment')
            new.geometry('+250+250')

            choice = cho1.get()  # VVIMP

            if choice == 'Fixed Deposit':

                l1 = Label(new, text='Bank')
                l2 = Label(new, text='Principal')
                l3 = Label(new, text='Rate')  # Annual Rate
                l4 = Label(new, text='C.I. Interval(Months)')  # In months
                l5 = Label(new, text='Start Date(DD-MM-YYYY)')  # DD-MM-YYYY
                l6 = Label(new, text='Period(Years)')  # Time in Years, minimum one year
                l7 = Label(new, text='Remarks')

                e1 = Entry(new)
                e2 = Entry(new)
                e3 = Entry(new)
                e4 = Entry(new)
                e5 = Entry(new)
                e6 = Entry(new)
                e7 = Entry(new)

                l1.grid(row=1, column=1, padx=5, pady=2)
                l2.grid(row=2, column=1)
                l3.grid(row=3, column=1)
                l4.grid(row=4, column=1)
                l5.grid(row=5, column=1)
                l6.grid(row=6, column=1)
                l7.grid(row=7, column=1)

                e1.grid(row=1, column=2, padx=5, pady=2)
                e2.grid(row=2, column=2)
                e3.grid(row=3, column=2)
                e4.grid(row=4, column=2)
                e5.grid(row=5, column=2)
                e6.grid(row=6, column=2)
                e7.grid(row=7, column=2)

                def save_changes():

                    response = messagebox.askquestion('Save', 'Save Investment?', icon='warning')
                    if response == 'yes':
                        bank = e1.get()
                        principal = int(float(e2.get()))
                        rate = float(e3.get())
                        interval = int(float(e4.get()))
                        start_date = e5.get()
                        period = int(float(e6.get()))
                        remarks = e7.get()

                        temp = int(float(start_date[6:10]))
                        new_year = temp + period
                        r = rate / 100
                        t = period
                        # A = (P)*((1+(r/n))**(n*t))
                        n = 12 / interval
                        amount = principal * pow(1 + r / n, n * t)  # float
                        interest = amount - principal  # float
                        amount = round(amount, 2)
                        interest = round(interest, 2)
                        maturity_date = start_date[0:6] + str(new_year)
                        # All necessary calclulations are made and variables defined
                        # MongoDB query goes below:
                        li = [bank, principal, rate, interval, start_date, maturity_date, interest, amount, remarks]
                        original = data.find_one({"_id": usr})
                        if "fixed" in original:
                            fullList = original.get("fixed")
                            fullList.append(li)
                            data.update_one({"_id": usr}, {"$set": {"fixed": fullList}})
                        else:
                            l = [li]
                            data.update_one({"_id": usr}, {"$set": {"fixed": l}})

                        messagebox.showinfo(title=None, message='Investment Saved')
                        new.destroy()
                        # For testing purposes
                        # test_label1 = Label(new, text = 'Amount: ' + str(amount))
                        # test_label2 = Label(new,text = 'Maturity Date: ' + maturity_date)

                        # test_label1.grid(row = 8)
                        # test_label2.grid(row = 9)

                button_save = Button(new, text='Save', relief=GROOVE, command=save_changes)
                button_save.grid(row=8, column=1, padx=30, pady=15)

            elif choice == 'Mutual Fund':
                l1 = Label(new, text='Company')
                l2 = Label(new, text='Net Asset Value(Initial)')
                l3 = Label(new, text='Units Bought')
                l4 = Label(new, text='Net Asset Value(At maturity)')
                l5 = Label(new, text='Period(Years)')
                l6 = Label(new, text='Date of Buying(DD-MM-YYYY)')  # DD-MM-YYYY
                l7 = Label(new, text='Remarks')

                e1 = Entry(new)
                e2 = Entry(new)
                e3 = Entry(new)
                e4 = Entry(new)
                e5 = Entry(new)
                e6 = Entry(new)
                e7 = Entry(new)

                l1.grid(row=1, column=1, padx=5, pady=2)
                l2.grid(row=2, column=1)
                l3.grid(row=3, column=1)
                l4.grid(row=4, column=1)
                l5.grid(row=5, column=1)
                l6.grid(row=6, column=1)
                l7.grid(row=7, column=1)

                e1.grid(row=1, column=2, padx=5, pady=2)
                e2.grid(row=2, column=2)
                e3.grid(row=3, column=2)
                e4.grid(row=4, column=2)
                e5.grid(row=5, column=2)
                e6.grid(row=6, column=2)
                e7.grid(row=7, column=2)

                def save_changes():

                    response = messagebox.askquestion('Save', 'Save Investment?', icon='warning')
                    if response == 'yes':
                        company = e1.get()
                        nav1 = int(float(e2.get()))
                        units = int(float(e3.get()))
                        date_buy = e6.get()  # DD-MM-YYYY
                        nav2 = int(float(e4.get()))
                        period = int(float(e5.get()))
                        remarks = e7.get()

                        investment = nav1 * units
                        amount = nav2 * units
                        temp = int(float(date_buy[6:10]))
                        new_year = temp + period
                        date_maturity = date_buy[0:6] + str(new_year)

                        # Copied from other asset - DB
                        li = [company, nav1, units, investment, date_buy, nav2, amount, date_maturity, remarks]
                        original = data.find_one({"_id": usr})
                        if "mutual" in original:
                            fullList = original.get("mutual")
                            fullList.append(li)
                            data.update_one({"_id": usr}, {"$set": {"mutual": fullList}})
                        else:
                            l = [li]
                            data.update_one({"_id": usr}, {"$set": {"mutual": l}})

                        messagebox.showinfo(title=None, message='Investment Saved')
                        new.destroy()


                button_save = Button(new, text='Save', relief=GROOVE, command=save_changes)
                button_save.grid(row=8, column=1, padx=30, pady=15)


            elif choice == 'Bank Account':

                l1 = Label(new, text='Bank')
                l2 = Label(new, text='Current Balance')
                l3 = Label(new, text='Type')  # Bank account type
                l4 = Label(new, text='Rate')  # Annual Rate
                l5 = Label(new, text='Compounding Interval(Months)')
                l6 = Label(new, text='Remarks')

                e1 = Entry(new)
                e2 = Entry(new)
                e3 = Entry(new)
                e4 = Entry(new)
                e5 = Entry(new)
                e6 = Entry(new)

                l1.grid(row=1, column=1, padx=5, pady=2)
                l2.grid(row=2, column=1)
                l3.grid(row=3, column=1)
                l4.grid(row=4, column=1)
                l5.grid(row=5, column=1)
                l6.grid(row=6, column=1)

                e1.grid(row=1, column=2, padx=5, pady=2)
                e2.grid(row=2, column=2)
                e3.grid(row=3, column=2)
                e4.grid(row=4, column=2)
                e5.grid(row=5, column=2)
                e6.grid(row=6, column=2)

                def save_changes():

                    response = messagebox.askquestion('Save', 'Save Investment?', icon='warning')
                    if response == 'yes':
                        bank = e1.get()
                        current_balance = int(float(e2.get()))
                        type_account = e3.get()
                        rate = float(e4.get())
                        interval = int(float(e5.get()))
                        remarks = e6.get()

                        r = rate / 100
                        n = 12 / interval
                        amount = current_balance * pow(1 + r / n, 1)  # float
                        interest = amount - current_balance  # float
                        amount = round(amount, 2)
                        interest = round(interest, 2)
                        # All necessary calclulations are made and variables defined
                        # MongoDB query goes below:
                        li = [bank, current_balance, type_account, rate, interval, interest, amount, remarks]
                        original = data.find_one({"_id": usr})
                        if "bank" in original:
                            fullList = original.get("bank")
                            fullList.append(li)
                            data.update_one({"_id": usr}, {"$set": {"bank": fullList}})
                        else:
                            l = [li]
                            data.update_one({"_id": usr}, {"$set": {"bank": l}})

                        messagebox.showinfo(title=None, message='Investment Saved')
                        new.destroy()

                button_save = Button(new, text='Save', relief=GROOVE, command=save_changes)
                button_save.grid(row=7, column=1, padx=30, pady=15)
            new.mainloop()

        def display_button():
            choice = cho1.get()
            if choice == 'Fixed Deposit':
                fixed_deposit(root)
                root.mainloop()
            elif choice == 'Mutual Fund':
                mutual_funds(root)
                root.mainloop()
            elif choice == 'Bank Account':
                bank_account(root)
                root.mainloop()

        def about_button():
            about = Toplevel()
            about.title('About')
            info_label = Label(about, text='Made by:\n\nKevin Shah\nParth Shah\nBhuvnesh Solanki')
            info_label.grid(row=0, column=0, padx=(50, 55), pady=(15, 15))
            about.geometry('200x100+30+30')

        def version_button():
            version = Toplevel()
            version.title('Version')
            info_label = Label(version, text='Investment Manager\nVersion: 1.0.0')
            info_label.grid(row=0, column=0, padx=(50, 50), pady=(10, 10))

        def help_button():
            url = "https://docs.google.com/document/d/18ocAY8t8aSYzmVxzfiuSnHb6uqIoz_dHafuWWiFT5JE/edit?usp=sharing"
            webbrowser.open(url, new=1)

        def callback(*args):
            button_new.config(state="normal")
            button_display.config(state="normal")

        label_home = Label(root, text='Welcome To MyMoney', font=('Verdana', 13))
        label_home.grid(row=1, column=1, padx=20, pady=5)

        label_usr = Label(root, text='Hi ' + str(usr))
        label_usr.grid(row=0, column=4)

        m1 = Menu(root)
        root.config(menu=m1)
        m1.add_command(label="About", command=about_button)
        m1.add_command(label="Version", command=version_button)
        m1.add_command(label="Help", command=help_button)

        button_new = Button(root, text='NEW', relief=GROOVE, command=new_button, state=DISABLED)
        button_display = Button(root, text='DISPLAY', relief=GROOVE, command=display_button, state=DISABLED)

        button_new.grid(row=3, column=0, padx=10, pady=(30, 10))
        button_display.grid(row=3, column=2, padx=10, pady=(30, 10))

        cho1 = StringVar()  # VVIMP
        cho1.set('Choose an option')
        cho1.trace("w", callback)
        choice_menu = OptionMenu(root, cho1, *choice_list)
        choice_menu.grid(row=2, column=1, padx=10, pady=(30, 10))

        label_day = Label(root, text='Date: ' + today_date)
        label_day.grid(row=7)

        root.mainloop()


class Login:
    def __init__(self):
        self.log()

    def log(self):
        global nameLog
        global pwordLog
        global rootA
        rootA = Tk()
        rootA.title('Login')
        rootA.geometry("300x200")
        rootA.resizable(0, 0)
        rootA.config(background="black", pady=10)
        instruction = Label(rootA,
                            text='Please Login\n',
                            bg="black",
                            fg="white",
                            font=20)
        instruction.place(x=110, y=5)

        nameTemp = Label(rootA, text='Username: ', bg="black", fg="white")
        pwordTemp = Label(rootA, text='Password: ', bg="black", fg="white")
        nameTemp.place(x=10, y=40)
        pwordTemp.place(x=10, y=80)

        nameLog = Entry(rootA)
        pwordLog = Entry(rootA, show='*')
        nameLog.place(x=110, y=40)
        pwordLog.place(x=110, y=80)

        loginB = Button(rootA, text='Login')
        loginB.place(x=110, y=120)
        loginB.bind("<1>", self.checklogin)
        loginB.bind("<Return>", self.checklogin)

        signUp = Button(rootA, text='Signup')
        signUp.place(x=160, y=120)
        signUp.bind("<1>", self.signup)
        signUp.bind("<Return>", self.signup)
        rootA.mainloop()

    def checklogin(self, event):
        a = data.find_one({"_id": nameLog.get()})
        if a is not None and nameLog.get() == a.get("_id") and pwordLog.get() == a.get("password"):
            global usr
            usr = nameLog.get()
            rootA.destroy()
            b = Home()
        else:
            r = Toplevel(rootA)
            r.title('D:')
            r.config(bg="black")
            r.geometry("300x50")
            r.resizable(0, 0)
            rlbl = Label(r, text='\nInvalid Login. Please try again.', bg="black", fg="white", font=("Verdana", 10))
            rlbl.pack()
            r.mainloop()
        return "break"

    def close(self, event):
        temp.destroy()
        return "break"

    def add(self, event):
        global temp
        a = data.find_one({"_id": nameSign.get()})
        if (a is not None):
            temp = Toplevel(roots)
            temp.config(bg="black")
            temp.title("Invalid SignUp")
            temp.resizable(0, 0)
            temp.geometry("300x100")
            msg = Label(temp, text="Username already exists. Please try again.", bg="black", fg="white",
                        font=("Verdana", 8))
            msg.place(x=15, y=30)
            bt = Button(temp, text="Ok", height=1, width=3, bg="white", relief="groove")  # command = close,
            bt.place(x=140, y=55)
            bt.bind("<1>", self.close)
            bt.bind("<Return>", self.close)
        else:
            d = {
                "_id": nameSign.get(),
                "password": pwordSign.get()
            }
            data.insert_one(d)
            roots.destroy()
            self.log()

    def signup(self, event):
        global pwordSign
        global nameSign
        global roots
        roots = Tk()
        roots.title('Signup')
        roots.resizable(0, 0)
        instruction = Label(roots,
                            text='Please Enter new Credentials',
                            bg="black",
                            fg="white",
                            font=("Verdana", 13))
        instruction.place(x=20, y=5)
        roots.geometry("300x200")
        roots.config(background="black", pady=10)
        nameL = Label(roots, text='New Username: ', bg="black", fg="white")
        pwordL = Label(roots, text='New Password: ', bg="black", fg="white")
        nameL.place(x=10, y=40)
        pwordL.place(x=10, y=80)

        nameSign = Entry(roots)
        pwordSign = Entry(roots, show='*')
        nameSign.place(x=110, y=40)
        pwordSign.place(x=110, y=80)

        dis = Label(roots, text="", bg="black", fg="white")
        signupButton = Button(roots, text='Signup')  # , command = add
        signupButton.bind("<1>", self.add)
        signupButton.bind("<Return>", self.add)
        signupButton.place(x=110, y=120)
        rootA.destroy()
        roots.mainloop()


if __name__ == "__main__":
    a = Login()