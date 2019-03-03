from tkinter import *
section = 2
x = 0.05
y = 0.15/6*section
x_col = 5
font_size = ('Arial')
        
def trade(ui):
    ui.earn_frame = Frame(ui.tab_trade)
    ui.pay_frame = Frame(ui.tab_trade)

    ui.earn_frame.place(relx = 0, rely = 0, relwidth=1.0, relheight=1.0/section)
    ui.pay_frame.place(relx = 0, rely = 1.0/section, relwidth=1.0, relheight=1.0/section)



    # earn 
    ui.earn_name_pay_label = Label(ui.earn_frame, text = 'pay name:',font=font_size)
    ui.earn_name_pay_label.place(relx=x, rely=y)
    ui.earn_name_pay_entry = Entry(ui.earn_frame, show = None, width=50)
    ui.earn_name_pay_entry.place(relx=x_col*x, rely=y)        

    # ui.earn_ID_pay_label = Label(ui.earn_frame, text = 'pay ID:',font=font_size)
    # ui.earn_ID_pay_label.place(relx=x,rely=2*y)
    # ui.earn_ID_pay_entry = Entry(ui.earn_frame, show = None, width=50)
    # ui.earn_ID_pay_entry.place(relx=x_col*x, rely=2*y)
    
    # ui.earn_i_m_label = Label(ui.earn_frame, text = 'mutual index:',font=font_size)
    # ui.earn_i_m_label.place(relx=x, rely=3*y)
    # ui.earn_i_m_entry = Entry(ui.earn_frame, show = None, width=50)
    # ui.earn_i_m_entry.insert(0,'default for the last mutual index')
    # ui.earn_i_m_entry.place(relx=x_col*x, rely=3*y)
    
    ui.earn_status = StringVar()
    ui.earn_status.set('earn')
    ui.earn_imme_button = Button(ui.earn_frame, textvariable = ui.earn_status, 
                                command = lambda : ui.handler(ui.earn_imme), state = 'disable')
    ui.earn_imme_button.place(relx=x_col*x, rely=4*y)


    # pay
    ui.pay_name_earn_label = Label(ui.pay_frame, text = 'earn name:',font=font_size)
    ui.pay_name_earn_label.place(relx=x, rely=y)
    ui.pay_name_earn_entry = Entry(ui.pay_frame, show = None, width=50)
    ui.pay_name_earn_entry.place(relx=x_col*x, rely=y)        

    ui.pay_coin_label = Label(ui.pay_frame, text = 'pay coin:',font=font_size)
    ui.pay_coin_label.place(relx=x, rely=2*y)
    ui.pay_coin_entry = Entry(ui.pay_frame, show = None, width=50)
    ui.pay_coin_entry.place(relx=x_col*x, rely=2*y)

    # ui.pay_i_m_label = Label(ui.pay_frame, text = 'mutual index:',font=font_size)
    # ui.pay_i_m_label.place(relx=x, rely=3*y)
    # ui.pay_i_m_entry = Entry(ui.pay_frame, show = None, width=50)
    # ui.pay_i_m_entry.insert(0,'default for the last mutual index')
    # ui.pay_i_m_entry.place(relx=x_col*x, rely=3*y)    


    ui.pay_status = StringVar()
    ui.pay_status.set('pay')
    ui.pay_imme_button = Button(ui.pay_frame, textvariable = ui.pay_status, 
                                command = lambda : ui.handler(ui.pay_imme), state = 'disable')
    ui.pay_imme_button.place(relx=x_col*x, rely=4*y)

