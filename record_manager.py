import tkinter as tk
import csv
from db import Database
from tkinter import messagebox
#new
from tkinter import filedialog
# import os

db = Database('store.db')

class Application(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        master.title('Record Manager')
        master.geometry("1000x400")
        master.configure(bg='lightyellow')
        self.create_widgets()
        self.selected_item = 0
        self.populate_list()

    def create_widgets(self):
        # artist
        self.artist_text = tk.StringVar()
        self.artist_label = tk.Label(self.master, text="Artist", font=('bold', 14), bg='lightyellow', pady=20)
        self.artist_label.grid(row=0, column=0, sticky=tk.W)
        self.artist_entry = tk.Entry(self.master, textvariable=self.artist_text)
        self.artist_entry.grid(row=0, column=1)
        # title
        self.title_text = tk.StringVar()
        self.title_label = tk.Label(self.master, text="Title", font=('bold', 14), bg='lightyellow')
        self.title_label.grid(row=0, column=2, sticky=tk.W)
        self.title_entry = tk.Entry(self.master, textvariable=self.title_text)
        self.title_entry.grid(row=0, column=3)
        # label
        self.label_text = tk.StringVar()
        self.label_label = tk.Label(self.master, text="Label", font=('bold', 14), bg='lightyellow')
        self.label_label.grid(row=1, column=0, sticky=tk.W)
        self.label_entry = tk.Entry(self.master, textvariable=self.label_text)
        self.label_entry.grid(row=1, column=1)
        # cat_number
        self.cat_number_text = tk.StringVar()
        self.cat_number_label = tk.Label(self.master, text="Cat #", font=('bold', 14), bg='lightyellow')
        self.cat_number_label.grid(row=1, column=2, sticky=tk.W)
        self.cat_number_entry = tk.Entry(self.master, textvariable=self.cat_number_text)
        self.cat_number_entry.grid(row=1, column=3)
        # barcode
        self.barcode_text = tk.StringVar()
        self.barcode_label = tk.Label(self.master, text="Barcode", font=('bold', 14), bg='lightyellow')
        self.barcode_label.grid(row=1, column=4, sticky=tk.W)
        self.barcode_entry = tk.Entry(self.master, textvariable=self.barcode_text)
        self.barcode_entry.grid(row=1, column=5)
        # supplier
        self.supplier_text = tk.StringVar()
        self.supplier_label = tk.Label(self.master, text="Supplier", font=('bold', 14), bg='lightyellow')
        self.supplier_label.grid(row=2, column=0, sticky=tk.W)
        self.supplier_entry = tk.Entry(self.master, textvariable=self.supplier_text)
        self.supplier_entry.grid(row=2, column=1)
        # unit_price
        self.unit_price_text = tk.StringVar()
        self.unit_price_label = tk.Label(self.master, text="Unit Price", font=('bold', 14), bg='lightyellow')
        self.unit_price_label.grid(row=2, column=2, sticky=tk.W)
        self.unit_price_entry = tk.Entry(self.master, textvariable=self.unit_price_text)
        self.unit_price_entry.grid(row=2, column=3)
        # retail_price
        self.retail_price_text = tk.StringVar()
        self.retail_price_label = tk.Label(self.master, text="Retail Price", font=('bold', 14), bg='lightyellow')
        self.retail_price_label.grid(row=2, column=4, sticky=tk.W)
        self.retail_price_entry = tk.Entry(self.master, textvariable=self.retail_price_text)
        self.retail_price_entry.grid(row=2, column=5)
        # stock_level
        self.stock_level_number = tk.IntVar()
        self.stock_level_label = tk.Label(self.master, text="Stock Level", font=('bold', 14), bg='lightyellow')
        self.stock_level_label.grid(row=3, column=0, sticky=tk.W)
        self.stock_level_entry = tk.Entry(self.master, textvariable=self.stock_level_number)
        self.stock_level_entry.grid(row=3, column=1)
        # date_received
        self.date_received_text = tk.StringVar()
        self.date_received_label = tk.Label(self.master, text="Date Received", font=('bold', 14), bg='lightyellow')
        self.date_received_label.grid(row=3, column=2, sticky=tk.W)
        self.date_received_entry = tk.Entry(self.master, textvariable=self.date_received_text)
        self.date_received_entry.grid(row=3, column=3)
        # sold_today
        self.sold_today_number = tk.IntVar()
        self.sold_today_label = tk.Label(self.master, text="Sold Today", font=('bold', 14), bg='lightyellow')
        self.sold_today_label.grid(row=3, column=4, sticky=tk.W)
        self.sold_today_entry = tk.Entry(self.master, textvariable=self.sold_today_number)
        self.sold_today_entry.grid(row=3, column=5)

        # records list
        self.record_list = tk.Listbox(self.master, height=8, width=80, border=0)
        self.record_list.grid(row=6, column=0, columnspan=5, rowspan=6, pady=20, padx=20)
        # create scrollbar
        self.scrollbar = tk.Scrollbar(self.master)
        self.scrollbar.grid(row=6, column=6)

        # set scroll to Listbox
        self.record_list.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.configure(command=self.record_list.yview)

        self.record_list.bind('<<ListboxSelect>>', self.select_item)


        # buttons
        self.add_btn = tk.Button(self.master, text='Add Item', width=12, command=self.add_item)
        self.add_btn.grid(row=4, column=0, pady=20)

        self.remove_btn = tk.Button(self.master, text='Remove Item', width=12, command=self.remove_item)
        self.remove_btn.grid(row=4, column=1, pady=20)

        self.update_btn = tk.Button(self.master, text='Update Item', width=12, command=self.update_item)
        self.update_btn.grid(row=4, column=2, pady=20)

        self.clear_btn = tk.Button(self.master, text='Clear Input', width=12, command=self.clear_text)
        self.clear_btn.grid(row=4, column=3, pady=20)

        self.sell_btn = tk.Button(self.master, text='Sell Item', width=12, command=self.sell_item)
        self.sell_btn.grid(row=4, column=4, pady=20)

        self.create_report_btn = tk.Button(self.master, text='Create Report', width=12, command=self.create_report)
        self.create_report_btn.grid(row=4, column=5, pady=20)

        self.upload_btn = tk.Button(self.master, text='Upload CSV', width=12, command=self.UploadAction)
        self.upload_btn.grid(row=5, column=0, pady=20)



    def populate_list(self):
        self.record_list.delete(0, tk.END)
        for row in db.fetch():
            self.record_list.insert(tk.END, row)

    # uploads CSV file to db
    # add error correction
    def UploadAction(self, event=None):
        root.update()
        filename = filedialog.askopenfilename()
        with open(filename) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                db.insert(row['artist'], row['title'], row['label'], row['catno'], "0123456789101", "MANUAL", 0.00, row['price'], 0, row['listed'], 0)
        csvfile.close()
        self.populate_list()


    def add_item(self):
        if self.title_text.get() == '' or self.artist_text.get() == '' or self.label_text.get() == '' or self.cat_number_text.get() == '' or self.barcode_text.get() == '' or self.supplier_text.get() == '' or self.unit_price_text.get() == '' or self.retail_price_text.get() == '' or self.stock_level_number.get() == '' or self.date_received_text.get() == '' or self.sold_today_number.get() == '':
            messagebox.showerror('Required Fields', 'Please include all fields')
            return

        db.insert(self.title_text.get(), self.artist_text.get(), self.label_text.get(), self.cat_number_text.get(), self.barcode_text.get(), self.supplier_text.get(), self.unit_price_text.get(), self.retail_price_text.get(), self.stock_level_number.get(), self.date_received_text.get(), self.sold_today_number.get())
        self.record_list.delete(0, tk.END)
        self.record_list.insert(tk.END, (self.title_text.get(), self.artist_text.get(), self.label_text.get(), self.cat_number_text.get(), self.barcode_text.get(), self.supplier_text.get(), self.unit_price_text.get(), self.retail_price_text.get(), self.stock_level_number.get(), self.date_received_text.get(), self.sold_today_number.get()))
        self.clear_text()
        self.populate_list()

    def select_item(self, event):
        try:
            # global selected_item
            index = self.record_list.curselection()[0]
            self.selected_item = self.record_list.get(index)

            self.title_entry.delete(0, tk.END)
            self.title_entry.insert(tk.END, self.selected_item[1])
            self.artist_entry.delete(0, tk.END)
            self.artist_entry.insert(tk.END, self.selected_item[2])
            self.label_entry.delete(0, tk.END)
            self.label_entry.insert(tk.END, self.selected_item[3])
            self.cat_number_entry.delete(0, tk.END)
            self.cat_number_entry.insert(tk.END, self.selected_item[4])
            self.barcode_entry.delete(0, tk.END)
            self.barcode_entry.insert(tk.END, self.selected_item[5])
            self.supplier_entry.delete(0, tk.END)
            self.supplier_entry.insert(tk.END, self.selected_item[6])
            self.unit_price_entry.delete(0, tk.END)
            self.unit_price_entry.insert(tk.END, self.selected_item[7])
            self.retail_price_entry.delete(0, tk.END)
            self.retail_price_entry.insert(tk.END, self.selected_item[8])
            self.stock_level_entry.delete(0, tk.END)
            self.stock_level_entry.insert(tk.END, self.selected_item[9])
            self.date_received_entry.delete(0, tk.END)
            self.date_received_entry.insert(tk.END, self.selected_item[10])
            self.sold_today_entry.delete(0, tk.END)
            self.sold_today_entry.insert(tk.END, self.selected_item[11])
        except IndexError:
            pass


    def remove_item(self):
        db.remove(self.selected_item[0])
        self.clear_text()
        self.populate_list()

    def update_item(self):
        if self.title_text.get() == '' or self.artist_text.get() == '' or self.label_text.get() == '' or self.cat_number_text.get() == '' or self.barcode_text.get() == '' or self.supplier_text.get() == '' or self.unit_price_text.get() == '' or self.retail_price_text.get() == '' or self.stock_level_number.get() == '' or self.date_received_text.get() == '' or self.sold_today_number.get() == '':
            messagebox.showerror('Required Fields', 'Please include all fields')
            return
        db.update(self.selected_item[0], self.title_text.get(), self.artist_text.get(), self.label_text.get(), self.cat_number_text.get(), self.barcode_text.get(), self.supplier_text.get(), self.unit_price_text.get(), self.retail_price_text.get(), self.stock_level_number.get(), self.date_received_text.get(), self.sold_today_number.get())
        self.populate_list()
        messagebox.showinfo('Information','Item updated')

    def clear_text(self):
        self.title_entry.delete(0, tk.END)
        self.artist_entry.delete(0, tk.END)
        self.label_entry.delete(0, tk.END)
        self.cat_number_entry.delete(0, tk.END)
        self.barcode_entry.delete(0, tk.END)
        self.supplier_entry.delete(0, tk.END)
        self.unit_price_entry.delete(0, tk.END)
        self.retail_price_entry.delete(0, tk.END)
        self.stock_level_entry.delete(0, tk.END)
        self.date_received_entry.delete(0, tk.END)
        self.sold_today_entry.delete(0, tk.END)

    # item has to be selected first before it can be sold!
    def sell_item(self):

        self.stock_int = self.stock_level_number.get()
        self.sold_today = self.sold_today_number.get()
        if self.stock_int < 1:
            messagebox.showerror('No stock left')
            return
        else:
            self.new_stock_level = self.stock_int - 1
            self.new_sold_today = self.sold_today + 1

        self.stock_level_number.set(self.new_stock_level)
        self.sold_today_number.set(self.new_sold_today)

        db.update(self.selected_item[0], self.title_text.get(), self.artist_text.get(), self.label_text.get(), self.cat_number_text.get(), self.barcode_text.get(), self.supplier_text.get(), self.unit_price_text.get(), self.retail_price_text.get(), self.stock_level_number.get(), self.date_received_text.get(), self.sold_today_number.get())

        # clear_text()
        self.populate_list()

    # populates list with db items
    def create_report(self):
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
        messagebox.showinfo("Title", "Report Written to File restock_report.csv in app directory")

        # resets sold today value to 0
        for row in db.fetch():

            sold_today_int = int(row[11])
            id = row[0]
            if sold_today_int > 0:
                reset_value = 0
                db.remove(row[0])
                db.insert(row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], reset_value)
                self.populate_list()



root = tk.Tk()
app = Application(master=root)
app.mainloop()
