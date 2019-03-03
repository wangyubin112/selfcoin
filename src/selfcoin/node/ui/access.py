from tkinter import *
section = 2
x = 0.05
y = 0.15/6*section
x_col = 5
font_size = ('Arial')

def access(ui):
    ui.regist_frame = Frame(ui.tab_access)
    ui.login_frame = Frame(ui.tab_access)
    
    ui.regist_frame.place(relx = 0, rely = 0, relwidth=1.0, relheight=1.0/section)
    ui.login_frame.place(relx = 0, rely = 1.0/section, relwidth=1.0, relheight=1.0/section)


    # regist
    ui.regist_name_label = Label(ui.regist_frame, text = 'name:',font=font_size)
    ui.regist_name_label.place(relx=x, rely=y)
    ui.regist_name_entry = Entry(ui.regist_frame, show = None, width=50)
    ui.regist_name_entry.place(relx = x_col * x, rely=y)  

    ui.regist_ID_real_label = Label(ui.regist_frame, text = 'real ID:',font=font_size)
    ui.regist_ID_real_label.place(relx=x, rely=2*y)
    ui.regist_ID_real_entry = Entry(ui.regist_frame, show = None, width=50)
    ui.regist_ID_real_entry.place(relx = x_col * x, rely=2*y)  

    ui.regist_status = StringVar()
    ui.regist_status.set('regist')
    ui.regist_button = Button(ui.regist_frame, textvariable = ui.regist_status, 
                            command = lambda : ui.handler(ui.regist))
    ui.regist_button.place(relx = x_col* x, rely = 3*y)

    # login/logout
    ui.login_label = Label(ui.login_frame, text = 'name:',font=font_size)
    ui.login_label.place(relx=x,rely=y)
    ui.login_entry = Entry(ui.login_frame, show = None, width=50)
    ui.login_entry.place(relx = x_col* x, rely = y)

    ui.login_status = StringVar()
    ui.login_status.set('login')
    ui.login_button = Button(ui.login_frame, textvariable = ui.login_status, 
                            command = lambda : ui.handler(ui.login))
    ui.login_button.place(relx = x_col * x, rely = 2*y)

    ui.logout_status = StringVar()
    ui.logout_status.set('logout')
    ui.logout_button = Button(ui.login_frame, textvariable = ui.logout_status, 
                            command = lambda : ui.handler(ui.logout), state = 'disable')
    ui.logout_button.place(relx = x_col * x, rely = 4*y)

