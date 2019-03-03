from tkinter import *
section = 2
x = 0.05
y = 0.15/6*section
x_col = 5
font_size = ('Arial')
        
def post(ui):
    ui.post_frame = Frame(ui.tab_post)
    ui.post_demand_frame = Frame(ui.tab_post)

    ui.post_frame.place(relx = 0, rely = 0, relwidth=1.0, relheight=1.0/section)
    ui.post_demand_frame.place(relx = 0, rely = 1.0/section, relwidth=1.0, relheight=1.0/section)



    # post to god
    ui.post_label = Label(ui.post_frame, text = 'content hash:',font=font_size)
    ui.post_label.place(relx=x, rely=y)
    ui.post_entry = Entry(ui.post_frame, show = None, width=50)
    ui.post_entry.place(relx=x_col*x, rely=y)
    
    ui.post_imme_status = StringVar()
    ui.post_imme_status.set('post imme')
    ui.post_imme_button = Button(ui.post_frame, textvariable = ui.post_imme_status, 
                        command = lambda : ui.handler(ui.post_imme), state = 'disable')
    ui.post_imme_button.place(relx=x_col*x, rely=2*y)




    # post demand
    ui.post_demand_name_label = Label(ui.post_demand_frame, text = 'name:',font=font_size)
    ui.post_demand_name_label.place(relx=x, rely=y)
    ui.post_demand_name_entry = Entry(ui.post_demand_frame, show = None, width=50)
    ui.post_demand_name_entry.place(relx=x_col*x, rely=y)        

    ui.post_demand_index_f_label = Label(ui.post_demand_frame, text = 'file index:',font=font_size)
    ui.post_demand_index_f_label.place(relx=x, rely=2*y)
    ui.post_demand_index_f_entry = Entry(ui.post_demand_frame, show = None, width=50)
    ui.post_demand_index_f_entry.place(relx=x_col*x, rely=2*y)
    
    ui.post_demand_index_l_label = Label(ui.post_demand_frame, text = 'line index:',font=font_size)
    ui.post_demand_index_l_label.place(relx=x,rely=3*y)
    ui.post_demand_index_l_entry = Entry(ui.post_demand_frame, show = None, width=50)
    ui.post_demand_index_l_entry.place(relx=x_col*x,rely=3*y)
    

    ui.post_demand_status = StringVar()
    ui.post_demand_status.set('post demand')
    ui.post_demand_button = Button(ui.post_demand_frame, textvariable = ui.post_demand_status, 
                                command = lambda : ui.handler(ui.post_demand), state = 'disable')
    ui.post_demand_button.place(relx=x_col*x,rely=4*y)
