from tkinter import *
section = 2
x = 0.05
y = 0.15/6*section
x_col = 5
font_size = ('Arial')
        
def charge(ui):
    ui.charge_frame = Frame(ui.tab_charge)
    ui.charge_demand_frame = Frame(ui.tab_charge)

    ui.charge_frame.place(relx = 0, rely = 0, relwidth=1.0, relheight=1.0/section)
    ui.charge_demand_frame.place(relx = 0, rely = 1.0/section, relwidth=1.0, relheight=1.0/section)



    # charge launch
    ui.charge_label = Label(ui.charge_frame, text = 'content hash:',font=font_size)
    ui.charge_label.place(relx=x, rely=y)
    ui.charge_entry = Entry(ui.charge_frame, show = None, width=50)
    ui.charge_entry.place(relx=x_col*x, rely=y)
    
    ui.charge_imme_status = StringVar()
    ui.charge_imme_status.set('charge imme')
    ui.charge_imme_button = Button(ui.charge_frame, textvariable = ui.charge_imme_status, 
                        command = lambda : ui.handler(ui.charge_imme), state = 'disable')
    ui.charge_imme_button.place(relx=x_col*x, rely=2*y)


    # charge demand
    ui.charge_demand_name_label = Label(ui.charge_demand_frame, text = 'name:',font=font_size)
    ui.charge_demand_name_label.place(relx=x, rely=y)
    ui.charge_demand_name_entry = Entry(ui.charge_demand_frame, show = None, width=50)
    ui.charge_demand_name_entry.place(relx=x_col*x, rely=y)        

    ui.charge_demand_index_f_label = Label(ui.charge_demand_frame, text = 'file index:',font=font_size)
    ui.charge_demand_index_f_label.place(relx=x, rely=2*y)
    ui.charge_demand_index_f_entry = Entry(ui.charge_demand_frame, show = None, width=50)
    ui.charge_demand_index_f_entry.place(relx=x_col*x, rely=2*y)
    
    ui.charge_demand_index_l_label = Label(ui.charge_demand_frame, text = 'line index:',font=font_size)
    ui.charge_demand_index_l_label.place(relx=x,rely=3*y)
    ui.charge_demand_index_l_entry = Entry(ui.charge_demand_frame, show = None, width=50)
    ui.charge_demand_index_l_entry.place(relx=x_col*x,rely=3*y)
    

    ui.charge_demand_status = StringVar()
    ui.charge_demand_status.set('charge demand')
    ui.charge_demand_button = Button(ui.charge_demand_frame, textvariable = ui.charge_demand_status, 
                                command = lambda : ui.handler(ui.charge_demand), state = 'disable')
    ui.charge_demand_button.place(relx=x_col*x,rely=4*y)
