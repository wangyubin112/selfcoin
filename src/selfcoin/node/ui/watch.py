from tkinter import *
section = 2
x = 0.05
y = 0.15/6*section
x_col = 5
# font_size = ('Arial')

def watch(ui):
    ui.watch_frame = Frame(ui.tab_watch) 

    ui.watch_frame.place(relx = 0, rely = 0, relwidth=1.0, relheight=1.0/section)

    # watch
    ui.watch_status = StringVar()
    ui.watch_status.set('watch trade')
    ui.watch_button = Button(ui.watch_frame, textvariable = ui.watch_status, 
                            command = lambda : ui.handler(ui.watch), state = 'disable')
    ui.watch_button.place(relx=x_col*x, rely=y)

    # watch demand
    ui.watch_demand_status = StringVar()
    ui.watch_demand_status.set('watch trade demand')
    ui.watch_demand_button = Button(ui.watch_frame, textvariable = ui.watch_demand_status, 
                            command = lambda : ui.handler(ui.watch_demand), state = 'disable')
    ui.watch_demand_button.place(relx=2*x_col*x, rely=y)



