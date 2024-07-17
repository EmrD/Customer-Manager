import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3
import os
import subprocess

class CustomerTracker(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Müşteri Takip")
        self.configure(bg="#f0f0f0") 
        self.create_table()
        self.create_widgets()
        self.load_data()
        self.geometry("1100x570")
        self.resizable(width=False, height=False)

    def create_table(self):
        connection = sqlite3.connect("customers.db")
        cursor = connection.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS customers (id INTEGER PRIMARY KEY, first_name TEXT, last_name TEXT, birth_date TEXT, tc_no TEXT, plate_number TEXT, document_serial_no TEXT, contact_no TEXT)")
        connection.commit()
        connection.close()

    def load_data(self):
        if hasattr(self, 'table'):
            self.table.delete(*self.table.get_children())
        connection = sqlite3.connect("customers.db")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM customers ORDER BY first_name ASC") 
        customers = cursor.fetchall()
        connection.close()

        for customer in customers:
            self.table.insert("", "end", values=customer)

    def add_customer(self):
        first_name = self.first_name_entry.get()
        last_name = self.last_name_entry.get()
        birth_date = self.birth_date_entry.get()
        tc_no = self.tc_no_entry.get()
        plate_number = self.plate_number_entry.get()
        document_serial_no = self.document_serial_no_entry.get()
        contact_no = self.contact_no_entry.get()

        connection = sqlite3.connect("customers.db")
        cursor = connection.cursor()
        cursor.execute("INSERT INTO customers (first_name, last_name, birth_date, tc_no, plate_number, document_serial_no, contact_no) VALUES (?, ?, ?, ?,?,?,?)",
                       (first_name, last_name, birth_date, tc_no, plate_number, document_serial_no, contact_no))
        connection.commit()
        connection.close()

        self.load_data()
        self.add_window.destroy()

    def open_add_window(self):
        self.add_window = tk.Toplevel(self)
        self.add_window.title("Add Customer")
        self.add_window.geometry("300x280")
        self.add_window.resizable(width=False, height=False)
        self.add_window.configure(bg="#f0f0f0") 

        self.first_name_label = tk.Label(self.add_window, text="Name:", bg="#f0f0f0")
        self.first_name_label.grid(row=0, column=0, padx=5, pady=5)
        self.first_name_entry = tk.Entry(self.add_window, justify="center")
        self.first_name_entry.grid(row=0, column=1, padx=5, pady=5)

        self.last_name_label = tk.Label(self.add_window, text="Last Name:", bg="#f0f0f0")
        self.last_name_label.grid(row=1, column=0, padx=5, pady=5)
        self.last_name_entry = tk.Entry(self.add_window, justify="center")
        self.last_name_entry.grid(row=1, column=1, padx=5, pady=5)

        self.birth_date_label = tk.Label(self.add_window, text="Birtday:", bg="#f0f0f0")
        self.birth_date_label.grid(row=2, column=0, padx=5, pady=5)
        self.birth_date_entry = tk.Entry(self.add_window, justify="center")
        self.birth_date_entry.grid(row=2, column=1, padx=5, pady=5)

        self.tc_no_label = tk.Label(self.add_window, text="ID Number:", bg="#f0f0f0")
        self.tc_no_label.grid(row=3, column=0, padx=5, pady=5)
        self.tc_no_entry = tk.Entry(self.add_window, justify="center")
        self.tc_no_entry.grid(row=3, column=1, padx=5, pady=5)

        self.plate_number_label = tk.Label(self.add_window, text="Plate Number:", bg="#f0f0f0")
        self.plate_number_label.grid(row=4, column=0, padx=5, pady=5)
        self.plate_number_entry = tk.Entry(self.add_window, justify="center")
        self.plate_number_entry.grid(row=4, column=1, padx=5, pady=5)

        self.document_serial_no_label = tk.Label(self.add_window, text="Information:", bg="#f0f0f0")
        self.document_serial_no_label.grid(row=5, column=0, padx=5, pady=5)
        self.document_serial_no_entry = tk.Entry(self.add_window, justify="center")
        self.document_serial_no_entry.grid(row=5, column=1, padx=5, pady=5)

        self.contact_no_label = tk.Label(self.add_window, text="Phone Number:", bg="#f0f0f0")
        self.contact_no_label.grid(row=6, column=0, padx=5, pady=5)
        self.contact_no_entry = tk.Entry(self.add_window, justify="center")
        self.contact_no_entry.grid(row=6, column=1, padx=5, pady=5)

        self.add_button = tk.Button(self.add_window, text="Save", command=self.add_customer, bg="#007bff", fg="white") 
        self.add_button.grid(row=7, column=0, columnspan=2, padx=5, pady=5)

    def delete_customer(self):
        selected_item = self.table.selection()
        if len(selected_item) == 0:
            messagebox.showwarning("Warning", "Select customer!")
            return

        if messagebox.askyesno("Onay", "Are you sure to delete this customer?"):
            customer_id = self.table.item(selected_item)['values'][0]

            connection = sqlite3.connect("customers.db")
            cursor = connection.cursor()
            cursor.execute("DELETE FROM customers WHERE id=?", (customer_id,))
            connection.commit()
            connection.close()

            self.load_data()

    def open_edit_window(self):
        selected_item = self.table.selection()
        if len(selected_item) == 0:
            messagebox.showwarning("Warning", "Select customer first.")
            return

        customer_data = self.table.item(selected_item)['values']
        self.edit_window = tk.Toplevel(self)
        self.edit_window.title("Edit")
        self.edit_window.geometry("300x280")
        self.edit_window.resizable(width=False, height=False)
        self.edit_window.configure(bg="#f0f0f0")

        self.first_name_label = tk.Label(self.edit_window, text="Name:", bg="#f0f0f0")
        self.first_name_label.grid(row=0, column=0, padx=5, pady=5)
        self.first_name_entry = tk.Entry(self.edit_window, justify="center")
        self.first_name_entry.insert(0, customer_data[1])
        self.first_name_entry.grid(row=0, column=1, padx=5, pady=10)

        self.last_name_label = tk.Label(self.edit_window, text="Last name:", bg="#f0f0f0")
        self.last_name_label.grid(row=1, column=0, padx=5, pady=5)
        self.last_name_entry = tk.Entry(self.edit_window, justify="center")
        self.last_name_entry.insert(0, customer_data[2])
        self.last_name_entry.grid(row=1, column=1, padx=5, pady=5)

        self.birth_date_label = tk.Label(self.edit_window, text="Birtday:", bg="#f0f0f0")
        self.birth_date_label.grid(row=2, column=0, padx=5, pady=5)
        self.birth_date_entry = tk.Entry(self.edit_window, justify="center")
        self.birth_date_entry.insert(0, customer_data[3])
        self.birth_date_entry.grid(row=2, column=1, padx=5, pady=5)

        self.tc_no_label = tk.Label(self.edit_window, text="ID Number:", bg="#f0f0f0")
        self.tc_no_label.grid(row=3, column=0, padx=5, pady=5)
        self.tc_no_entry = tk.Entry(self.edit_window, justify="center")
        self.tc_no_entry.insert(0, customer_data[4])
        self.tc_no_entry.grid(row=3, column=1, padx=5, pady=5)

        self.plate_number_label = tk.Label(self.edit_window, text="Plate:", bg="#f0f0f0")
        self.plate_number_label.grid(row=4, column=0, padx=5, pady=5)
        self.plate_number_entry = tk.Entry(self.edit_window, justify="center")
        self.plate_number_entry.insert(0, customer_data[5])
        self.plate_number_entry.grid(row=4, column=1, padx=5, pady=5)

        self.document_serial_no_label = tk.Label(self.edit_window, text="Information:", bg="#f0f0f0")
        self.document_serial_no_label.grid(row=5, column=0, padx=5, pady=5)
        self.document_serial_no_entry = tk.Entry(self.edit_window, justify="center")
        self.document_serial_no_entry.insert(0, customer_data[6])
        self.document_serial_no_entry.grid(row=5, column=1, padx=5, pady=5)

        self.contact_no_label = tk.Label(self.edit_window, text="Phone Number:", bg="#f0f0f0")
        self.contact_no_label.grid(row=6, column=0, padx=5, pady=5)
        self.contact_no_entry = tk.Entry(self.edit_window, justify="center")
        self.contact_no_entry.insert(0, customer_data[7])
        self.contact_no_entry.grid(row=6, column=1, padx=5, pady=5)

        self.edit_button = tk.Button(self.edit_window, text="Save", command=self.edit_customer, bg="#007bff", fg="white")
        self.edit_button.grid(row=7, column=0, columnspan=2, padx=5, pady=10)

    def edit_customer(self):
        selected_item = self.table.selection()
        if len(selected_item) == 0:
            messagebox.showwarning("Warning", "Select customer.")
            return

        customer_id = self.table.item(selected_item)['values'][0]
        first_name = self.first_name_entry.get()
        last_name = self.last_name_entry.get()
        birth_date = self.birth_date_entry.get()
        tc_no = self.tc_no_entry.get()
        plate_number = self.plate_number_entry.get()
        document_serial_no = self.document_serial_no_entry.get()
        contact_no = self.contact_no_entry.get()

        connection = sqlite3.connect("customers.db")
        cursor = connection.cursor()
        cursor.execute("UPDATE customers SET first_name=?, last_name=?, birth_date=?, tc_no=?, plate_number=?, document_serial_no=?, contact_no=? WHERE id=?",
                       (first_name, last_name, birth_date, tc_no, plate_number, document_serial_no, contact_no, customer_id))
        connection.commit()
        connection.close()

        self.load_data()
        self.edit_window.destroy()

    def sort_customers(self, col_name):
        connection = sqlite3.connect("customers.db")
        cursor = connection.cursor()
        
        if col_name == "Ad":
            cursor.execute("SELECT * FROM customers ORDER BY first_name COLLATE NOCASE")
        elif col_name == "ID":
            cursor.execute("SELECT * FROM customers ORDER BY id ASC")
        elif col_name == "Soyad":
            cursor.execute("SELECT * FROM customers ORDER BY last_name COLLATE NOCASE")
        
        customers = cursor.fetchall()
        connection.close()

        self.table.delete(*self.table.get_children()) 

        for customer in customers:
            self.table.insert("", "end", values=customer)

    def search_customer(self):
        search_value = self.search_entry.get()
        search_criteria = self.search_criteria.get()

        connection = sqlite3.connect("customers.db")
        cursor = connection.cursor()

        if search_criteria == "Ad":
            cursor.execute("SELECT * FROM customers WHERE first_name LIKE ?", ('%' + search_value + '%',))
        elif search_criteria == "Soyad":
            cursor.execute("SELECT * FROM customers WHERE last_name LIKE ?", ('%' + search_value + '%',))
        elif search_criteria == "TC Kimlik No":
            cursor.execute("SELECT * FROM customers WHERE tc_no LIKE ?", ('%' + search_value + '%',))
        elif search_criteria == "Plaka":
            cursor.execute("SELECT * FROM customers WHERE plate_number LIKE ?", ('%' + search_value + '%',))
        elif search_criteria == "Belge Seri No":
            cursor.execute("SELECT * FROM customers WHERE document_serial_no LIKE ?", ('%' + search_value + '%',))
        elif search_criteria == "İletişim No":
            cursor.execute("SELECT * FROM customers WHERE contact_no LIKE ?", ('%' + search_value + '%',))

        customers = cursor.fetchall()
        connection.close()

        self.table.delete(*self.table.get_children())

        for customer in customers:
            self.table.insert("", "end", values=customer)

    def clear_placeholder(self, event):
        if self.search_entry.get() == "Type Here...":
            self.search_entry.delete(0, "end")

    def restore_placeholder(self, event):
        if not self.search_entry.get():
            self.search_entry.insert(0, "Type Here...")

    def create_widgets(self):
        self.table_frame = ttk.Frame(self)
        self.table_frame.pack(pady=10)

        self.table = ttk.Treeview(self.table_frame, columns=("ID", "Name", "Last Name", "Birtday", "ID Number", "Plate", "Information", "Phone Number"), show="headings")
        self.table.column("ID", width=50)
        self.table.column("Name", anchor="center", width=100)
        self.table.column("Last Name", anchor="center", width=100)
        self.table.column("Birtday", anchor="center", width=100)
        self.table.column("ID Number", anchor="center", width=150)
        self.table.column("Plate", anchor="center", width=100)
        self.table.column("Information", anchor="center", width=150)
        self.table.column("Phone Number", anchor="center", width=150)

        self.table.heading("ID", text="ID ↕", command=lambda: self.sort_customers("ID"))
        self.table.heading("Name", text="Name ↕", command=lambda: self.sort_customers("Name"))
        self.table.heading("Last Name", text="Last Name ↕" , command=lambda: self.sort_customers("Last Name"))
        self.table.heading("Birtday", text="Birtday")
        self.table.heading("ID Number", text="ID Number")
        self.table.heading("Plate", text="Plate")
        self.table.heading("Information", text="Information")
        self.table.heading("Phone Number", text="Phone Number")

        for col in self.table['columns']:
            self.table.column(col, anchor="center")

        style = ttk.Style()
        style.configure("Treeview.Heading", borderwidth=1, relief="solid", foreground="black")

        separator = ttk.Separator(self.table_frame, orient='horizontal')
        separator.pack(side='bottom', fill='x', padx=5, pady=5)

        self.table.pack()

        self.search_criteria_label = tk.Label(self, text="Search With:", bg="#f0f0f0")
        self.search_criteria_label.pack(pady=5)
        self.search_criteria = ttk.Combobox(self, values=("Name", "Last Name", "ID Number", "Plate", "Information", "Phone Number"), state="readonly")
        self.search_criteria.pack(pady=5)
        self.search_criteria.set("ID Number") 

        self.search_entry = tk.Entry(self , justify="center" , font="14")
        self.search_entry.pack(pady=5)
        self.search_entry.insert(0, "Type Here...")
        self.search_entry.bind("<FocusIn>", self.clear_placeholder)
        self.search_entry.bind("<FocusOut>", self.restore_placeholder)


        self.search_button = tk.Button(self, text="Search", command=self.search_customer, bg="#007bff", fg="white")
        self.search_button.pack(pady=5)

        self.add_button = tk.Button(self, text="Add", command=self.open_add_window, bg="green", fg="white")
        self.add_button.pack(pady=5) 

        self.edit_button = tk.Button(self, text="Edit", command=self.open_edit_window, bg="orange", fg="white")
        self.edit_button.pack(pady=5)

        self.delete_button = tk.Button(self, text="Delete", command=self.delete_customer, bg="#dc3545", fg="white")
        self.delete_button.pack(pady=5)

        self.path = tk.Label(self, text="Database Path: " + os.path.abspath("customers.db").replace("\\", " / "), bg="#f0f0f0", font="24")
        self.path.pack(pady=5)

        def open_dir():
            subprocess.Popen(r'explorer /select, "customers.db"')

        self.open_dir = tk.Button(self, text="Open Path", command=open_dir)
        self.open_dir.pack()

if __name__ == "__main__":
    app = CustomerTracker()
    app.mainloop()


