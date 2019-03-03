from tkinter import *
from tkinter.font import Font
from tkinter.ttk import *
from tkinter.messagebox import *
#import tkinter.filedialog as tkFileDialog
#import tkinter.simpledialog as tkSimpleDialog    #askstring()

from node.ui.access import access
from node.ui.trade import trade
from node.ui.post import post
from node.ui.charge import charge
from node.ui.watch import watch
from node.ui.show import show

class Ui(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master.title('Self-coin')
        self.master.geometry('1200x1000')
        self.createWidgets()

    def createWidgets(self):
        self.top = self.winfo_toplevel()

        # self.style = Style()

        ## info
        self.info_notebook = Notebook(self.top)
        self.info_notebook.place(relx=0.0, rely=0.0, relwidth=0.5, relheight=1.0)
        # self.info_notebook.grid(row = 0, column = 0, sticky=N+S+E+W)
        show(self)


        ## operate
        self.operate_notebook = Notebook(self.top)
        self.operate_notebook.place(relx=0.5, rely=0.0, relwidth=0.5, relheight=1.0)
        # self.operate_notebook.grid(row = 0, column = 1, sticky=N+S+E+W)

        # tab 0 (access)
        self.tab_access = Frame(self.operate_notebook)
        access(self)
        self.operate_notebook.add(self.tab_access, text='Access')

        # tab 1 (post) 
        self.tab_post = Frame(self.operate_notebook)
        post(self)
        self.operate_notebook.add(self.tab_post, text='Post')

        # tab 2 (charge) 
        self.tab_charge = Frame(self.operate_notebook)
        charge(self)
        self.operate_notebook.add(self.tab_charge, text='Charge')
                
        # tab 3 (trade)
        self.tab_trade = Frame(self.operate_notebook)
        trade(self)
        self.operate_notebook.add(self.tab_trade, text='Trade')

        # tab 4 (watch)
        self.tab_watch = Frame(self.operate_notebook)
        watch(self)
        self.operate_notebook.add(self.tab_watch, text='Watch')