from tkinter import *
from db import Database
from tkinter import messagebox
import os

db = Database('store.db')


def populate_list():
    record_list.delete(0, END)
    for row in db.fetch():
        record_list.insert(END, row)


def add_item():
    if title_text.get() == '' or artist_text.get() == '' or label_text.get() == '' or cat_number_text.get() == '' or barcode_text.get() == '' or supplier_text.get() == '' or unit_price_text.get() == '' or retail_price_text.get() == '' or stock_level_number.get() == '' or date_received_text.get() == '' or sold_today_number.get() == '':
        messagebox.showerror('Required Fields', 'Please include all fields')
        return

    db.insert(title_text.get(), artist_text.get(), label_text.get(), cat_number_text.get(), barcode_text.get(), supplier_text.get(), unit_price_text.get(), retail_price_text.get(), stock_level_number.get(), date_received_text.get(), sold_today_number.get())
    record_list.delete(0, END)
    record_list.insert(END, (title_text.get(), artist_text.get(), label_text.get(), cat_number_text.get(), barcode_text.get(), supplier_text.get(), unit_price_text.get(), retail_price_text.get(), stock_level_number.get(), date_received_text.get(), sold_today_number.get()))
    clear_text()
    populate_list()

def select_item(event):
    try:
        global selected_item
        index = record_list.curselection()[0]
        selected_item = record_list.get(index)

        title_entry.delete(0, END)
        title_entry.insert(END, selected_item[1])
        artist_entry.delete(0, END)
        artist_entry.insert(END, selected_item[2])
        label_entry.delete(0, END)
        label_entry.insert(END, selected_item[3])
        cat_number_entry.delete(0, END)
        cat_number_entry.insert(END, selected_item[4])
        barcode_entry.delete(0, END)
        barcode_entry.insert(END, selected_item[5])
        supplier_entry.delete(0, END)
        supplier_entry.insert(END, selected_item[6])
        unit_price_entry.delete(0, END)
        unit_price_entry.insert(END, selected_item[7])
        retail_price_entry.delete(0, END)
        retail_price_entry.insert(END, selected_item[8])
        stock_level_entry.delete(0, END)
        stock_level_entry.insert(END, selected_item[9])
        date_received_entry.delete(0, END)
        date_received_entry.insert(END, selected_item[10])
        sold_today_entry.delete(0, END)
        sold_today_entry.insert(END, selected_item[11])
    except IndexError:
        pass


def remove_item():
    db.remove(selected_item[0])
    clear_text()
    populate_list()

def update_item():
    if title_text.get() == '' or artist_text.get() == '' or label_text.get() == '' or cat_number_text.get() == '' or barcode_text.get() == '' or supplier_text.get() == '' or unit_price_text.get() == '' or retail_price_text.get() == '' or stock_level_number.get() == '' or date_received_text.get() == '' or sold_today_number.get() == '':
        messagebox.showerror('Required Fields', 'Please include all fields')
        return
    db.update(selected_item[0], title_text.get(), artist_text.get(), label_text.get(), cat_number_text.get(), barcode_text.get(), supplier_text.get(), unit_price_text.get(), retail_price_text.get(), stock_level_number.get(), date_received_text.get(), sold_today_number.get())
    populate_list()
    messagebox.showinfo('Item updated')

def clear_text():
    title_entry.delete(0, END)
    artist_entry.delete(0, END)
    label_entry.delete(0, END)
    cat_number_entry.delete(0, END)
    barcode_entry.delete(0, END)
    supplier_entry.delete(0, END)
    unit_price_entry.delete(0, END)
    retail_price_entry.delete(0, END)
    stock_level_entry.delete(0, END)
    date_received_entry.delete(0, END)
    sold_today_entry.delete(0, END)

    # item has to be selected first before it can be sold!
def sell_item():

    stock_int = stock_level_number.get()
    sold_today = sold_today_number.get()
    if stock_int < 1:
        messagebox.showerror('No stock left')
        return
    else:
        new_stock_level = stock_int - 1
        new_sold_today = sold_today + 1

    stock_level_number.set(new_stock_level)
    sold_today_number.set(new_sold_today)

    db.update(selected_item[0], title_text.get(), artist_text.get(), label_text.get(), cat_number_text.get(), barcode_text.get(), supplier_text.get(), unit_price_text.get(), retail_price_text.get(), stock_level_number.get(), date_received_text.get(), sold_today_number.get())

    # clear_text()
    populate_list()

    # populates list with db items
def create_report():
    report = []
    for row in db.fetch():
        sold_today_int = int(row[11])
        stock_level_int = int(row[9])
        if sold_today_int > 0 and stock_level_int > 0:
            report.append(row)
    # formats and converts row tuple to string and writes contents of report list to a report file
    report_out = open("restock_report.csv", "w")
    for item in report:
        formatted_output = (item[1], item[2], item[3], item[4], " stock level: ", item[9], " number sold today: ", item[11])
        string_row = str(formatted_output)
        stripped = string_row.replace("'", " ")
        formatted_string = stripped + "\n"
        report_out.write(formatted_string)

    report_out.close()
    messagebox.showinfo("Title", "Report Written to File restock_report.txt in app directory")

    # resets sold today value to 0
    for row in db.fetch():

        sold_today_int = int(row[11])
        id = row[0]
        if sold_today_int > 0:
            reset_value = 0
            db.remove(row[0])
            db.insert(row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], reset_value)
            populate_list()




# create window
app = Tk()

# artist

artist_text = StringVar()
artist_label = Label(app, text="Artist", font=('bold', 14), pady=20)
artist_label.grid(row=0, column=0, sticky=W)
artist_entry = Entry(app, textvariable=artist_text)
artist_entry.grid(row=0, column=1)


# title
title_text = StringVar()
title_label = Label(app, text="Title", font=('bold', 14))
title_label.grid(row=0, column=2, sticky=W)
title_entry = Entry(app, textvariable=title_text)
title_entry.grid(row=0, column=3)


# label
label_text = StringVar()
label_label = Label(app, text="Label", font=('bold', 14))
label_label.grid(row=1, column=0, sticky=W)
label_entry = Entry(app, textvariable=label_text)
label_entry.grid(row=1, column=1)


# cat_number
cat_number_text = StringVar()
cat_number_label = Label(app, text="Cat #", font=('bold', 14))
cat_number_label.grid(row=1, column=2, sticky=W)
cat_number_entry = Entry(app, textvariable=cat_number_text)
cat_number_entry.grid(row=1, column=3)

# barcode
barcode_text = StringVar()
barcode_label = Label(app, text="Barcode", font=('bold', 14))
barcode_label.grid(row=1, column=4, sticky=W)
barcode_entry = Entry(app, textvariable=barcode_text)
barcode_entry.grid(row=1, column=5)

# supplier
supplier_text = StringVar()
supplier_label = Label(app, text="Supplier", font=('bold', 14))
supplier_label.grid(row=2, column=0, sticky=W)
supplier_entry = Entry(app, textvariable=supplier_text)
supplier_entry.grid(row=2, column=1)

# unit_price
unit_price_text = StringVar()
unit_price_label = Label(app, text="Unit Price", font=('bold', 14))
unit_price_label.grid(row=2, column=2, sticky=W)
unit_price_entry = Entry(app, textvariable=unit_price_text)
unit_price_entry.grid(row=2, column=3)


# retail_price
retail_price_text = StringVar()
retail_price_label = Label(app, text="Retail Price", font=('bold', 14))
retail_price_label.grid(row=2, column=4, sticky=W)
retail_price_entry = Entry(app, textvariable=retail_price_text)
retail_price_entry.grid(row=2, column=5)


# stock_level
stock_level_number = IntVar()
stock_level_label = Label(app, text="Stock Level", font=('bold', 14))
stock_level_label.grid(row=3, column=0, sticky=W)
stock_level_entry = Entry(app, textvariable=stock_level_number)
stock_level_entry.grid(row=3, column=1)


# date_received
date_received_text = StringVar()
date_received_label = Label(app, text="Date Received", font=('bold', 14))
date_received_label.grid(row=3, column=2, sticky=W)
date_received_entry = Entry(app, textvariable=date_received_text)
date_received_entry.grid(row=3, column=3)

# sold_today
sold_today_number = IntVar()
sold_today_label = Label(app, text="Sold Today", font=('bold', 14))
sold_today_label.grid(row=3, column=4, sticky=W)
sold_today_entry = Entry(app, textvariable=sold_today_number)
sold_today_entry.grid(row=3, column=5)

# records list
record_list = Listbox(app, height=8, width=80, border=0)
record_list.grid(row=5, column=0, columnspan=5, rowspan=6, pady=20, padx=20)

# create scrollbar

scrollbar = Scrollbar(app)
scrollbar.grid(row=5, column=6)

# set scroll to Listbox
record_list.configure(yscrollcommand=scrollbar.set)
scrollbar.configure(command=record_list.yview)

record_list.bind('<<ListboxSelect>>', select_item)

#  buttons

add_btn = Button(app, text='Add Item', width=12, command=add_item)
add_btn.grid(row=4, column=0, pady=20)

remove_btn = Button(app, text='Remove Item', width=12, command=remove_item)
remove_btn.grid(row=4, column=1, pady=20)

update_btn = Button(app, text='Update Item', width=12, command=update_item)
update_btn.grid(row=4, column=2, pady=20)

clear_btn = Button(app, text='Clear Input', width=12, command=clear_text)
clear_btn.grid(row=4, column=3, pady=20)

sell_btn = Button(app, text='Sell Item', width=12, command=sell_item)
sell_btn.grid(row=4, column=4, pady=20)

create_report_btn = Button(app, text='Create Report', width=12, command=create_report)
create_report_btn.grid(row=4, column=5, pady=20)


app.title('Record Manager')
app.geometry('1000x400')


# populate data
populate_list()


# start program
app.mainloop()
