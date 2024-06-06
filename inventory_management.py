import csv
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sqlite3

class InventoryManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Inventory Management System")
        self.root.geometry("1200x800")
        
        # Predefined items with their costs
        self.predefined_items = {
            "Item A": 10.0,
            "Item B": 20.0,
            "Item C": 30.0,
            "Item D": 40.0
        }
        
        # Set up the SQLite database
        self.conn = sqlite3.connect('inventory.db')
        self.cursor = self.conn.cursor()
        self.create_table()

        # Set up UI components
        self.create_widgets()
        self.load_data_into_tree()
        
        # Bind Enter key to add item
        self.root.bind('<Return>', self.add_multiple_items)

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS inventory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                cost REAL NOT NULL,
                number INTEGER NOT NULL,
                remarks TEXT
            )
        ''')
        self.conn.commit()

    def create_widgets(self):
        # Entry form for multiple items
        self.items_frame = tk.Frame(self.root)
        self.items_frame.grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky='nsew')
        
        self.items_label = tk.Label(self.items_frame, text="Items")
        self.items_label.grid(row=0, column=0, padx=10, pady=10)

        self.add_item_button = tk.Button(self.items_frame, text="Add Another Item", command=self.add_item_row)
        self.add_item_button.grid(row=0, column=1, padx=10, pady=10)

        # Labels for the entry fields
        self.name_header = tk.Label(self.items_frame, text="Item Name")
        self.name_header.grid(row=1, column=0, padx=10, pady=10)
        
        self.cost_header = tk.Label(self.items_frame, text="Cost")
        self.cost_header.grid(row=1, column=1, padx=10, pady=10)
        
        self.number_header = tk.Label(self.items_frame, text="Number")
        self.number_header.grid(row=1, column=2, padx=10, pady=10)
        
        self.remarks_header = tk.Label(self.items_frame, text="Remarks")
        self.remarks_header.grid(row=1, column=3, padx=10, pady=10)
        
        self.items = []
        self.add_item_row()  # Add the first item row

        self.add_multiple_button = tk.Button(self.root, text="Add All Items", command=self.add_multiple_items)
        self.add_multiple_button.grid(row=2, column=0, padx=10, pady=10)

        self.update_button = tk.Button(self.root, text="Update Item", command=self.update_item)
        self.update_button.grid(row=2, column=1, padx=10, pady=10)
        
        self.delete_button = tk.Button(self.root, text="Delete Item", command=self.delete_item)
        self.delete_button.grid(row=2, column=2, padx=10, pady=10)
        
        self.download_button = tk.Button(self.root, text="Download CSV", command=self.download_csv)
        self.download_button.grid(row=2, column=3, padx=10, pady=10)
        
        # Inventory list
        self.tree = ttk.Treeview(self.root, columns=("id", "name", "cost", "number", "remarks", "Total Cost"), show='headings')
        self.tree.heading("id", text="ID")
        self.tree.heading("name", text="Item Name")
        self.tree.heading("cost", text="Cost")
        self.tree.heading("number", text="Number")
        self.tree.heading("remarks", text="Remarks")
        self.tree.heading("Total Cost", text="Total Cost")
        self.tree.grid(row=3, column=0, columnspan=4, padx=10, pady=10, sticky='nsew')
        
        # Hide the ID column
        self.tree.column("id", width=0, stretch=tk.NO)
        
        # Make the columns adjustable
        self.root.grid_rowconfigure(3, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_columnconfigure(2, weight=1)
        self.root.grid_columnconfigure(3, weight=1)
        
        self.tree.bind('<Delete>', self.delete_item)
        self.tree.bind('<ButtonRelease-1>', self.select_item)

    def fill_cost(self, event, cost_entry):
        selected_item = event.widget.get()
        if selected_item in self.predefined_items:
            cost_entry.delete(0, tk.END)
            cost_entry.insert(0, self.predefined_items[selected_item])

    def add_item_row(self):
        row = len(self.items) + 2  # Adjust row number for headers

        name_entry = ttk.Combobox(self.items_frame, values=list(self.predefined_items.keys()))
        name_entry.grid(row=row, column=0, padx=10, pady=10)
        cost_entry = tk.Entry(self.items_frame)
        cost_entry.grid(row=row, column=1, padx=10, pady=10)
        number_entry = tk.Entry(self.items_frame)
        number_entry.grid(row=row, column=2, padx=10, pady=10)
        remarks_entry = tk.Entry(self.items_frame)
        remarks_entry.grid(row=row, column=3, padx=10, pady=10)

        name_entry.bind("<<ComboboxSelected>>", lambda event, cost_entry=cost_entry: self.fill_cost(event, cost_entry))
        
        self.items.append((name_entry, cost_entry, number_entry, remarks_entry))

    def add_multiple_items(self, event=None):
        for name_entry, cost_entry, number_entry, remarks_entry in self.items:
            name = name_entry.get()
            cost = cost_entry.get()
            number = number_entry.get()
            remarks = remarks_entry.get()
            
            if name and cost and number:
                try:
                    cost = float(cost)
                    number = int(number)
                    self.cursor.execute('''
                        INSERT INTO inventory (name, cost, number, remarks) 
                        VALUES (?, ?, ?, ?)
                    ''', (name, cost, number, remarks))
                except ValueError:
                    messagebox.showerror("Invalid input", "Cost must be a number and Number must be an integer.")
            else:
                messagebox.showerror("Input Error", "Please fill all fields.")
        
        self.conn.commit()
        self.load_data_into_tree()
        self.clear_entries()
            
    def update_item(self):
        selected_item = self.tree.selection()
        if selected_item:
            try:
                item_id = self.tree.item(selected_item[0], "values")[0]
                name = self.name_entry.get()
                cost = float(self.cost_entry.get())
                number = int(self.number_entry.get())
                remarks = self.remarks_entry.get()
                
                self.cursor.execute('''
                    UPDATE inventory
                    SET name = ?, cost = ?, number = ?, remarks = ?
                    WHERE id = ?
                ''', (name, cost, number, remarks, item_id))
                self.conn.commit()
                self.load_data_into_tree()
                self.clear_entries()
            except ValueError:
                messagebox.showerror("Invalid input", "Cost must be a number and Number must be an integer.")
        else:
            messagebox.showerror("Selection Error", "No item selected to update.")
            
    def delete_item(self, event=None):
        selected_item = self.tree.selection()
        if selected_item:
            for item in selected_item:
                item_id = self.tree.item(item, "values")[0]
                self.cursor.execute('DELETE FROM inventory WHERE id = ?', (item_id,))
                self.conn.commit()
            self.load_data_into_tree()
        else:
            messagebox.showerror("Selection Error", "No item selected to delete.")
            
    def select_item(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            item_values = self.tree.item(selected_item[0], "values")
            self.name_entry.delete(0, tk.END)
            self.name_entry.insert(0, item_values[1])
            self.cost_entry.delete(0, tk.END)
            self.cost_entry.insert(0, item_values[2])
            self.number_entry.delete(0, tk.END)
            self.number_entry.insert(0, item_values[3])
            self.remarks_entry.delete(0, tk.END)
            self.remarks_entry.insert(0, item_values[4])
            
    def clear_entries(self):
        for name_entry, cost_entry, number_entry, remarks_entry in self.items:
            name_entry.delete(0, tk.END)
            cost_entry.delete(0, tk.END)
            number_entry.delete(0, tk.END)
            remarks_entry.delete(0, tk.END)
        
    def load_data_into_tree(self):
        # Clear existing data in the tree
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Load data from the database
        self.cursor.execute('SELECT * FROM inventory')
        rows = self.cursor.fetchall()
        for row in rows:
            total_cost=row[2]*row[3]
            self.tree.insert("", "end", values=(row[0], row[1], row[2], row[3], row[4], total_cost))
    
    def download_csv(self):
        self.cursor.execute('SELECT * FROM inventory')
        rows = self.cursor.fetchall()
        rows = [(x[1:]) for x in rows]
        if not rows:
            messagebox.showerror("No Data", "No inventory data to export.")
            return
        
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if file_path:
            try:
                with open(file_path, mode='w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(["Item Name", "Cost", "Number", "Remarks", "Total Cost"])
                    for row in rows:
                        total_cost=row[1]*row[2]
                        row=row+(total_cost,)
                        writer.writerow(row)
                messagebox.showinfo("Success", "Data exported successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export data: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = InventoryManagementSystem(root)
    root.mainloop()
