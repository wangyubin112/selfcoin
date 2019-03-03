from tkinter import *
from tkinter.ttk import *
x = 0.05
y = 0.15
x_col = 5
section = 6
font_size = ('Arial')
# font_size = ('Consolas')

def show(ui):
    ui.show_own_frame = Frame(ui.info_notebook)
    ui.show_add_frame = Frame(ui.info_notebook)
    ui.show_frame = Frame(ui.info_notebook)
    ui.show_db_notebook = Notebook(ui.info_notebook)

    ui.show_own_frame.place(relx = 0, rely = 0, relwidth=1.0, relheight=1.0/section)
    ui.show_add_frame.place(relx = 0, rely = 1.0/section, relwidth=1.0, relheight=1.0/section)
    ui.show_frame.place(relx = 0, rely = 2.0/section, relwidth=1.0, relheight=1.0/section)
    ui.show_db_notebook.place(relx = 0, rely = 3.0/section, relwidth = 1.0, relheight = 3.0/section)
    
    # own
    ui.show_own_name_label = Label(ui.show_own_frame, text = 'own name:',font=font_size)
    ui.show_own_name_label.place(relx = x, rely = y)
    ui.show_own_name_status = StringVar()
    ui.show_own_name_entry = Entry(ui.show_own_frame, textvariable = ui.show_own_name_status, 
                                    show = None, width=50)
    ui.show_own_name_entry.place(relx = x_col* x, rely = y)
    
    ui.show_own_ID_label = Label(ui.show_own_frame, text = 'own ID:',font=font_size)
    ui.show_own_ID_label.place(relx = x, rely = 2*y)
    ui.show_own_ID_status = StringVar()
    ui.show_own_ID_entry = Entry(ui.show_own_frame, textvariable = ui.show_own_ID_status, 
                                    show = None, width = 50)
    ui.show_own_ID_entry.place(relx = x_col* x, rely = 2*y)

    ui.show_own_coin_label = Label(ui.show_own_frame, text = 'own coin:',font=font_size)
    ui.show_own_coin_label.place(relx = x, rely = 3*y)
    ui.show_own_coin_status = StringVar()
    ui.show_own_coin_entry = Entry(ui.show_own_frame, textvariable = ui.show_own_coin_status, 
                                    show = None, width = 50)
    ui.show_own_coin_entry.place(relx = x_col* x, rely = 3*y)


    # add ID to DB_guide and DB_credit
    ui.show_name_add_label = Label(ui.show_add_frame, text = 'added name:',font=font_size)
    ui.show_name_add_label.place(relx = x, rely = y)
    ui.show_name_add_entry = Entry(ui.show_add_frame, show = None, width=50)
    ui.show_name_add_entry.place(relx = x_col* x, rely = y)

    ui.show_ID_add_label = Label(ui.show_add_frame, text = 'added ID:',font=font_size)
    ui.show_ID_add_label.place(relx = x, rely = 2*y)
    ui.show_ID_add_entry = Entry(ui.show_add_frame, show = None, width=50)
    ui.show_ID_add_entry.place(relx = x_col* x, rely = 2*y)

    # ui.show_friend_coin_label = Label(ui.show_add_frame, text = 'friend coin:',font=font_size)
    # ui.show_friend_coin_label.place(relx = x, rely = 3*y)
    # ui.show_friend_coin_entry = Entry(ui.show_add_frame, show = None, width=50)
    # ui.show_friend_coin_entry.place(relx = x_col* x, rely = 3*y)

    ui.show_credit_add_label = Label(ui.show_add_frame, text = 'credit:',font=font_size)
    ui.show_credit_add_label.place(relx = x, rely = 3*y)
    ui.show_credit_add_status = StringVar()
    ui.show_credit_add_combobox = Combobox(ui.show_add_frame,width=20, textvariable = ui.show_credit_add_status)
    ui.show_credit_add_combobox['values'] = ('friend', 'partner')
    ui.show_credit_add_combobox.current(1)
    ui.show_credit_add_combobox.place(relx = x_col* x, rely = 3*y)

    ui.show_add_status = StringVar()
    ui.show_add_status.set('add')
    ui.show_add_button = Button(ui.show_add_frame, textvariable = ui.show_add_status, 
                                command = lambda : ui.handler(ui.add))
    ui.show_add_button.place(relx=x_col*x, rely=4*y)

    # search based on name
    ui.show_name_label = Label(ui.show_frame, text = 'name:',font=font_size)
    ui.show_name_label.place(relx = x, rely = y)
    ui.show_name_entry = Entry(ui.show_frame, show = None, width=40)
    ui.show_name_entry.place(relx = x_col* x, rely = y)

    ui.show_search_status = StringVar()
    ui.show_search_status.set('search')
    ui.show_search_button = Button(ui.show_frame, textvariable = ui.show_search_status, 
                                command = lambda : ui.handler(ui.search), state = 'disable')
    ui.show_search_button.place(relx=3.2*x_col*x, rely=y)

    ui.show_ID_label = Label(ui.show_frame, text = 'ID:',font=font_size)
    ui.show_ID_label.place(relx = x, rely = 2*y)
    ui.show_ID_entry = Entry(ui.show_frame, show = None, width=50)
    ui.show_ID_entry.place(relx = x_col* x, rely = 2*y)

    ui.show_credit_label = Label(ui.show_frame, text = 'credit:',font=font_size)
    ui.show_credit_label.place(relx = x, rely = 3*y)
    ui.show_credit_entry = Entry(ui.show_frame, show = None, width=50)
    ui.show_credit_entry.place(relx = x_col* x, rely = 3*y)


    ## db    
    # db for friend
    ui.show_db_friend_frame = Frame(ui.show_db_notebook)
    ui.show_db_notebook.add(ui.show_db_friend_frame, text = 'DB_Friend')
    
    ui.show_db_friend_list_frame = Frame(ui.show_db_friend_frame)
    ui.show_db_friend_list_frame.place(relx = x, rely = 0.25*y)

    ui.show_db_friend_listbox = Listbox(ui.show_db_friend_list_frame, font=font_size, height = 21)
    ui.show_db_friend_listbox.grid(row = 0, column = 0)
    ui.show_db_friend_scrollbarX = Scrollbar(ui.show_db_friend_list_frame,command=ui.show_db_friend_listbox.xview,orient='horizontal')
    ui.show_db_friend_scrollbarX.grid(row = 1, column = 0, sticky=E+W)
    ui.show_db_friend_scrollbarY = Scrollbar(ui.show_db_friend_list_frame,command=ui.show_db_friend_listbox.yview)
    ui.show_db_friend_scrollbarY.grid(row = 0, column = 1,rowspan=2,sticky=N+S)
    ui.show_db_friend_listbox.config(xscrollcommand=ui.show_db_friend_scrollbarX.set,
                                       yscrollcommand=ui.show_db_friend_scrollbarY.set)
    
    for i in range(100):
        ui.show_db_friend_listbox.insert(END, 1000000000000000000+i)


    # ui.show_db_friend_label = Label(ui.show_db_friend_frame, text = 'friend search:',font=font_size)
    # ui.show_db_friend_label.place(relx = 1.75*x_col*x, rely = 2*y)
    # ui.show_db_friend_entry = Entry(ui.show_db_friend_frame, show = None, width=20)
    # ui.show_db_friend_entry.place(relx = 2.5*x_col* x, rely = 2*y)

    

    # db for partner
    ui.show_db_partner_frame = Frame(ui.show_db_notebook)
    ui.show_db_notebook.add(ui.show_db_partner_frame, text = 'DB_Partner')

    ui.show_db_partner_list_frame = Frame(ui.show_db_partner_frame)
    ui.show_db_partner_list_frame.place(relx = x, rely = 0.25*y)

    ui.show_db_partner_listbox = Listbox(ui.show_db_partner_list_frame, font=font_size, height = 21)
    ui.show_db_partner_listbox.grid(row = 0, column = 0)
    ui.show_db_partner_scrollbarX = Scrollbar(ui.show_db_partner_list_frame,command=ui.show_db_partner_listbox.xview,orient='horizontal')
    ui.show_db_partner_scrollbarX.grid(row = 1, column = 0, sticky=E+W)
    ui.show_db_partner_scrollbarY = Scrollbar(ui.show_db_partner_list_frame,command=ui.show_db_partner_listbox.yview)
    ui.show_db_partner_scrollbarY.grid(row = 0, column = 1,rowspan=2,sticky=N+S)
    ui.show_db_partner_listbox.config(xscrollcommand=ui.show_db_partner_scrollbarX.set,
                                       yscrollcommand=ui.show_db_partner_scrollbarY.set)
    
    for i in range(100):
        ui.show_db_partner_listbox.insert(END, 1000000000000000000+i)
